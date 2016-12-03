import sys
import time
import itertools
import openpyxl as xl
import utils
from multiprocessing import Pool
from collections import Counter
from properties import Costanti
from giornata import Giornata
from calendario import Calendario


def main(filename="Calendario.xlsx"):
    """A partire dal nome del file excel scaricato:
    crea una lista di oggetti Giornata, inizializzati con i punti delle squadre nelle singole giornate;
    utilizza queste informazioni per calcolare la classifica di tutti i fattoriale(Costanti.NUM_SQUADRE) calendari;
    stampa la classifica dei calendari vinti dalle singole squadre, al variare dei punti in classifica"""
    
    starting_time = time.time()
    giornate = [Giornata(n) for n in xrange(1, Costanti.NUM_GIORNATE+1)]
    try:        
        calendario_xl = xl.load_workbook(filename)
    except Exception as e:
        print 'Errore in lettura del file {}'.format(filename)
        print e
        print sys.exc_info()[0]
    else:
        print 'Letto il file {}'.format(filename)
        calendario_sheet = calendario_xl.get_active_sheet()
        squadre = utils.get_squadre_calendario(calendario_sheet)
        utils.set_giornate_calendario(calendario_sheet, giornate, squadre)
        all_permutations = list(itertools.permutations(squadre))
        print '{} processi da lanciare per {} calendari'.format(Costanti.NUM_PROCESSES, len(all_permutations))
        print 'inizializzazione...'        
        calendari = [Calendario(perm, giornate) for perm in all_permutations]
        initialization_time = time.time()
        print 'Tempo impiegato per inizializzazione: {0:.2f} s'.format(initialization_time - starting_time)
        print 'in elaborazione...'
        pool = Pool(processes=Costanti.NUM_PROCESSES)
        print '\tmap...'
        classifiche = pool.map(calcola_classifica_distribuito_map, calendari)
        print '\treduce...'
        classifica_calendari = reduce(calcola_classifica_distribuito_reduce, classifiche)
        utils.esporta_classifica_csv(classifica_calendari)
        ending_time = time.time()
        print 'Tempo impiegato per elaborazione: {0:.2f} s'.format(ending_time - initialization_time)
        print 'Tempo impiegato totale: {0:.2f} s'.format(time.time() - starting_time)


def calcola_classifica_distribuito_map(calendario):
    calendario.calcola_classifica()
    classifica_attuale = dict(zip(calendario.get_squadre(), [0]*Costanti.NUM_SQUADRE))    
    squadre_campioni = calendario.get_squadra_campione()
    for sc in squadre_campioni:
        classifica_attuale[sc] = 1 
    return classifica_attuale


def calcola_classifica_distribuito_reduce(classifica_x, classifica_y):
    return dict(Counter(classifica_x) + Counter(classifica_y))


if __name__ == '__main__':
    
    main(sys.argv[1])
