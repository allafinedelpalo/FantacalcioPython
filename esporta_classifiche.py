import sys
import time
import itertools
import openpyxl as xl
from collections import Counter
import pandas as pd
import utils
from properties import Costanti
from giornata import Giornata
from calendario import Calendario


def main(filename="Calendario.xlsx"):
	"""A partire dal nome del file excel scaricato:
	crea una lista di oggetti Giornata, inizializzati con i punti delle squadre nelle singole giornate;
	utilizza queste informazioni per calcolare la classifica di tutti i fattoriale(Costanti.NUM_SQUADRE) calendari;
	stampa la classifica dei calendari vinti dalle singole squadre, al variare dei punti in classifica"""
	
	starting_time = time.time()
	squadre = []
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
		classifica_calendari = dict(zip(squadre, [0]*Costanti.NUM_SQUADRE))
		print 'in elaborazione...'
		for perm in all_permutations:
			calendario = Calendario(perm, giornate)
			calendario.calcola_classifica()
			squadre_campioni = calendario.get_squadra_campione()
			classifica_attuale = dict(zip(squadre, [0]*Costanti.NUM_SQUADRE))
			for sc in squadre_campioni:
				classifica_attuale[sc] = 1 
			classifica_calendari = dict(Counter(classifica_calendari) + Counter(classifica_attuale))
		utils.esporta_classifica_csv(classifica_calendari)
		print 'Tempo impiegato: {0:.2f} s'.format(time.time() - starting_time)

 
if __name__ == '__main__':
	
	main(sys.argv[1])
	