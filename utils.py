import pandas as pd
from properties import Costanti


def get_squadre_calendario(sheet):
    """Metodo per la ricerca dei nomi delle squadre partecipanti
    all'interno del blocco della prima giornata di campionato"""
    squadre = []
    for i in xrange(Costanti.NUM_SQUADRE/2):
        squadre.append(sheet[Costanti.FIRST_LETTER_EVN + str(Costanti.STARTING_NUMBER + i)].value)
        squadre.append(sheet[Costanti.LAST_LETTER_EVN + str(Costanti.STARTING_NUMBER + i)].value)
    return squadre   

def set_giornate_calendario(sheet, giornate, squadre):
    """Metodo per la completa inizializzazione delle giornate del calendario
    Legge dal foglio Excel 'sheet' nei blocchi delle giornate
    La posizione dei blocchi delle giornate nel calendario e' da verificare negli attributi della classe 'Costanti'"""
    offset_giornata = 0
    for g in giornate:
        g.squadre = squadre
        if g.n_giornata % 2 == 1:
            tl = Costanti.FIRST_LETTER_ODD + str(Costanti.STARTING_NUMBER + offset_giornata)
            br = Costanti.LAST_LETTER_ODD + str(Costanti.STARTING_NUMBER 
                + Costanti.NUM_SQUADRE/2 + offset_giornata - 1)
        else:
            tl = Costanti.FIRST_LETTER_EVN + str(Costanti.STARTING_NUMBER + offset_giornata)
            br = Costanti.LAST_LETTER_EVN + str(Costanti.STARTING_NUMBER 
                + Costanti.NUM_SQUADRE/2 + offset_giornata - 1)
            offset_giornata += Costanti.OFFSET_VERT_GIORNATE
        blocco_giornata = list(sheet[tl:br])
        if blocco_giornata[0][1].value > 0 and blocco_giornata[0][2].value > 0:
            g.giocata=True
            for row in blocco_giornata[0:]:
                g.squadre_pti[row[0].value] = row[1].value
                g.squadre_pti[row[3].value] = row[2].value

def esporta_classifica_csv(classifica_calendari):
    """Metodo che esporta la 'classifica delle classifiche' in un unico file .csv"""
    classifica_list = []
    location = 0
    df = pd.DataFrame(columns=Costanti.COLUMNS)
    for squadra, vittorie in classifica_calendari.iteritems():
        row = squadra + '@' + str(vittorie)
        df.loc[location] = row.split(Costanti.SEPARATOR)
        location = location + 1
    df[Costanti.NUM_CALENDARI_VINTI] = df[Costanti.NUM_CALENDARI_VINTI].astype(int)
    df = df.sort_values(by=Costanti.ORDER_BY_COLUMNS, ascending=False)
    df.to_csv(Costanti.FILENAME_OUTPUT, sep=';', index=False)
    print 'Generato il file {}'.format(Costanti.FILENAME_OUTPUT)
