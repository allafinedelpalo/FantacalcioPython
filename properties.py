import string


class Costanti:
    """Classe che mantiene tutte le proprieta' invariabili del progetto.
    Le variabili costanti devono essere opportunamente impostate prima di
    eseguire il programma."""

    @staticmethod
    def genera_girone_segnaposti(squadre):
        """Implementazione python dell'algoritmo 'round-robin tournament'
        http://stackoverflow.com/questions/11245746/league-fixture-generator-in-python
        https://en.wikipedia.org/wiki/Round-robin_tournament"""

        rotation = list(squadre)
        giornate = []
        for i in xrange(0, len(squadre)-1):
            giornate.append(rotation)
            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
        return giornate

    # costanti dipendenti dal fantacampionato
    NUM_SQUADRE = 4
    NUM_GIRONI = 4
    NUM_GIORNATE = (NUM_SQUADRE - 1) * NUM_GIRONI
    ULTIMA_GIORNATA = NUM_GIORNATE
    
    # costanti per leggere il file excel
    FIRST_LETTER_ODD = 'A'
    LAST_LETTER_ODD = 'D'
    FIRST_LETTER_EVN = 'G'
    LAST_LETTER_EVN = 'J'    
    STARTING_NUMBER = 5
    OFFSET_VERT_GIORNATE = (NUM_SQUADRE / 2) + 1
    
    # calendario con segnaposto per un girone
    SEGNAPOSTO = 'SEGNAPOSTO'
    SEGNAPOSTI = list(string.ascii_uppercase)[:NUM_SQUADRE]
    CALENDARIO_SEGNAPOSTI = genera_girone_segnaposti(SEGNAPOSTI)
    CALENDARIO_SEGNAPOSTI_COMPLETO = CALENDARIO_SEGNAPOSTI * NUM_GIRONI
    
    # soglie punti-gol"""
    SOGLIE_PUNTI_GOL = xrange(66, 186, 6)
    
    # costanti per la classifica
    PTI_V = 3
    PTI_P = 1
    PTI_S = 0
    PARIMERITO = True

    # numero di processi da lanciare
    NUM_PROCESSES = 2

    # nome del file .csv di output
    COLUMNS = ['SQUADRA', 'PUNTI IN CLASSIFICA', 'CALENDARI VINTI']
    SEPARATOR = '@'
    NUM_CALENDARI_VINTI = 'CALENDARI VINTI'
    ORDER_BY_COLUMNS = ['CALENDARI VINTI']
    FILENAME_OUTPUT = 'ClassificaCalendari.csv'
