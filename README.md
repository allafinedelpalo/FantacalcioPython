# FantacalcioPython

Script per il calcolo del numero di tutte le classifiche generate da ogni possibile calendario estratto per un campionato di Fantacalcio a gironi.

Il programma prende in ingresso il file excel Calendario.xlsx scaricabile dalla pagina della propria Lega iscritta al sito leghe.fantagazzetta.com


# Usage

python esporta_classifiche.py Calendario.xlsx


# Proprietà

Nel file properties.py è necessario impostare manualmente:
* NUM_SQUADRE: numero di squadre partecipanti
* NUM_GIRONI: numero di gironi che compongo il calendario da calcolare
* ULTIMA_GIORNATA: ultima giornata da considerare per il calcolo delle classifiche
* NUM_PROCESSES: numero di processi da utilizzare per il calcolo

Per maggiori informazioni sullo script:
* Introduzione - http://www.allafinedelpalo.it/statistiche-sui-calendari-del-fantacalcio-python
* Refactoring - http://www.allafinedelpalo.it/python-programmazione-object-oriented
* Multiprocessing - http://wwww.allafinedelpalo.it/python-multiprocessing
* Gestione degli argomenti - coming soon..
* Visualizzazione grafica delle statistiche - coming soon...


# Modifiche del refactoring

* esporta_classifiche.py: contiene la funzione principale del progetto;
* properties.py: contiene le proprietà specifiche del progetto;
* utils.py: metodi di utilià vari;
* giornata.py: modulo che contiene la classe di gestione della Giornata;
* calendario.py: modulo che contiene la classe di gestione del Calendario;
