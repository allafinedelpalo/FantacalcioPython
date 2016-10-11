import itertools
import openpyxl as xl
import bisect
from collections import Counter

class Costanti:
	"""Classe di utility con tutte le costanti per il progetto"""
	
	"""costanti dipendenti dal fantacampionato"""
	NUM_SQUADRE = 4
	NUM_GIRONI = 4
	NUM_GIORNATE = (NUM_SQUADRE - 1) * NUM_GIRONI
	
	"""costanti per leggere il file excel"""
	FIRST_LETTER_ODD = 'A'
	LAST_LETTER_ODD = 'D'
	FIRST_LETTER_EVN = 'G'
	LAST_LETTER_EVN = 'J'	
	STARTING_NUMBER = 5
	OFFSET_VERT_GIORNATE = (NUM_SQUADRE / 2) + 1
	
	"""calendario con segnaposto per un girone"""
	SEGNAPOSTI = ['A', 'B', 'C', 'D']
	CALENDARIO_SEGNAPOSTI = [SEGNAPOSTI
							,['A', 'C', 'B', 'D']
							,['D', 'A', 'C', 'B']
							 ]
	CALENDARIO_SEGNAPOSTI_COMPLETO = CALENDARIO_SEGNAPOSTI * NUM_GIRONI
	
	"""soglie punti-gol"""
	SOGLIE_PUNTI_GOL = range(66,186,6)
	
	"""costanti per la classifica"""
	PTI_V = 3
	PTI_P = 1
	PTI_S = 0
	PARIMERITO = True

	"""nome del file .csv di output"""
	FILENAME_OUTPUT = "ClassificaCalendari.csv"


class Giornata:
	"""Classe per gestire le giornate"""
	
	def __init__(self, n_giornata):
		self._squadre = []
		self._squadre_pti = {}
		self._squadre_pti_classifica = {}
		self._n_giornata = n_giornata
		self._giocata = False		
		self._nome_giornata = "Giornata " + str(self._n_giornata)
	
	def print_giornata(self):
		"""Stampa la giornata"""
		print self._nome_giornata
		for (squadra, pti) in zip(self._squadre_pti.keys(), self._squadre_pti.values()):
			print squadra + ' ' + str(pti)					  
	


class Calendario:
	"""Classe per gestire un calendario
	Comprende il calcolo della classifica per tutte le partite giocate"""
	
	
	def __init__(self, permutation, giornate):
		self._permutation = permutation
		self._giornate = giornate
		self._classifica = dict(zip(self._permutation, [0]*Costanti.NUM_SQUADRE))
		self._diz_segnaposti = dict(zip(Costanti.SEGNAPOSTI, self._permutation))
		self._calendario_custom = []
		self._pti_primo = 0
		self._squadre_campioni = []
		for segnaposti_giornata in Costanti.CALENDARIO_SEGNAPOSTI_COMPLETO:
			segnaposti_giornata_custom = ['SEGNAPOSTO']*Costanti.NUM_SQUADRE
			for ind, segnaposto in enumerate(segnaposti_giornata):
				segnaposti_giornata_custom[ind] = self._diz_segnaposti[segnaposto]
			self._calendario_custom.append(segnaposti_giornata_custom)
	
	
	def get_squadra_campione(self):
		"""Restituisce la lista delle squadre campioni
		Se Costanti.PARIMETRO = True restituisce una lista di un elemento (concatenazione delle squadre campioni)
		Altrimenti restituisce una lista con tutte le squadre alla prima posizione"""
		if Costanti.PARIMERITO:
			return [" / ".join(self._squadre_campioni) + "@" + str(self._pti_primo)]
		else:
			return [sc + "@" + str(self._pti_primo) for sc in self._squadre_campioni]

		
	def calcola_classifica(self, ultima_giornata=Costanti.NUM_GIORNATE):
		"""Calcola la classifica fino alla giornata numero 'ultima_giornata'
		per tutte le giornate con flag 'giocata'=True"""
		for g in self._giornate[:ultima_giornata]:
			if g._giocata:
				self.calcola_giornata(g)
				self._classifica = dict(Counter(g._squadre_pti_classifica) + Counter(self._classifica))
		self._pti_primo = max(self._classifica.values())
		self._squadre_campioni = [k for k,v in self._classifica.iteritems() if v==self._pti_primo]
		self._squadre_campioni.sort()
		

	def calcola_giornata(self, giornata):
		"""Calcola tutte le partite della giornata
		attribuendo i punti vittoria, pareggio o sconfitta alle squadre"""
		scontri_giornata = self._calendario_custom[giornata._n_giornata-1]
		for indx in range(0, len(scontri_giornata), 2):
			[pti_casa, pti_fuori] = self.calcola_partita(giornata._squadre_pti[scontri_giornata[indx]], giornata._squadre_pti[scontri_giornata[indx+1]])
			giornata._squadre_pti_classifica[scontri_giornata[indx]] = pti_casa
			giornata._squadre_pti_classifica[scontri_giornata[indx+1]] = pti_fuori	 
		  
		
	def calcola_partita(self, pti_casa, pti_fuori):
		"""Calcola i gol di una partita confrontando pti_casa e pti_fuori"""
		gol_casa = self.converti_punti_gol(pti_casa)
		gol_fuori = self.converti_punti_gol(pti_fuori)
		if gol_casa > gol_fuori:
			return [Costanti.PTI_V, Costanti.PTI_S]
		elif gol_casa < gol_fuori:
			return [Costanti.PTI_S, Costanti.PTI_V]
		else:
			return [Costanti.PTI_P, Costanti.PTI_P]
			
			
	def converti_punti_gol(self, pti):
		"""Restituisce il numero di gol a seconda dei punti e alle soglie gol stabilite"""
		if pti < Costanti.SOGLIE_PUNTI_GOL[0]:
			return 0
		else:
			return bisect.bisect_right(Costanti.SOGLIE_PUNTI_GOL,pti)

		
	def print_calendario(self):
		"""Stampa il calendario"""
		n_giornata = 1
		for giornata_custom in self._calendario_custom:
			print "Giornata " + str(n_giornata)
			for i in range(0, Costanti.NUM_SQUADRE, 2):
				print str(giornata_custom[i][:3]) + ' - ' + str(giornata_custom[i+1][:3])
			print
			n_giornata += 1
			
			
	def print_classifica(self):
		"""Stampa la classifica"""
		for squadra, punti in sorted(self._classifica.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			print squadra + '\t\t' + str(punti)



def get_squadre_calendario(sheet):
	"""Metodo per la ricerca dei nomi delle squadre partecipanti
	all'interno del blocco della prima giornata di campionato"""
	squadre = []
	for i in range(Costanti.NUM_SQUADRE/2):
		squadre.append(sheet[Costanti.FIRST_LETTER_EVN + str(Costanti.STARTING_NUMBER + i)].value)
		squadre.append(sheet[Costanti.LAST_LETTER_EVN + str(Costanti.STARTING_NUMBER + i)].value)
	return squadre   



def set_giornate_calendario(sheet, giornate, squadre):
	"""Metodo per la completa inizializzazione delle giornate del calendario
	Legge dal foglio Excel 'sheet' nei blocchi delle giornate
	La posizione dei blocchi delle giornate nel calendario e' da verificare negli attributi della classe 'Costanti'"""
	offset_giornata = 0
	for g in giornate:
		g._squadre = squadre
		if g._n_giornata % 2 == 1:
			tl = Costanti.FIRST_LETTER_ODD + str(Costanti.STARTING_NUMBER + offset_giornata)
			br = Costanti.LAST_LETTER_ODD + str(Costanti.STARTING_NUMBER + Costanti.NUM_SQUADRE/2 + offset_giornata - 1)
		else:
			tl = Costanti.FIRST_LETTER_EVN + str(Costanti.STARTING_NUMBER + offset_giornata)
			br = Costanti.LAST_LETTER_EVN + str(Costanti.STARTING_NUMBER + Costanti.NUM_SQUADRE/2 + offset_giornata - 1)
			offset_giornata += Costanti.OFFSET_VERT_GIORNATE
		blocco_giornata = list(sheet[tl:br])
		if blocco_giornata[0][1].value > 0 and blocco_giornata[0][2].value > 0:
			g._giocata=True
			for row in blocco_giornata[0:]:
				g._squadre_pti[row[0].value] = row[1].value
				g._squadre_pti[row[3].value] = row[2].value



def main(filename="Calendario.xlsx"):
	"""a partire dal nome del file excel scaricato:
	crea una lista di oggetti Giornata, inizializzati con i punti delle squadre nelle singole giornate;
	utilizza queste informazioni per calcolare la classifica di tutti i fattoriale(Costanti.NUM_SQUADRE) calendari;
	stampa la classifica dei calendari vinti dalle singole squadre, al variare dei punti in classifica"""
	
	squadre = []
	giornate = [Giornata(n) for n in range(1, Costanti.NUM_GIORNATE+1)]

	calendario_xl = xl.load_workbook(filename)
	calendario_sheet = calendario_xl.get_active_sheet()
	squadre = get_squadre_calendario(calendario_sheet)

	set_giornate_calendario(calendario_sheet, giornate, squadre)
	
	all_permutations = list(itertools.permutations(squadre))

	classifica_calendari = dict(zip(squadre, [0]*Costanti.NUM_SQUADRE))

	for perm in all_permutations:
		calendario = Calendario(perm, giornate)
		calendario.calcola_classifica()
		squadre_campioni = calendario.get_squadra_campione()
		classifica_attuale = dict(zip(squadre, [0]*Costanti.NUM_SQUADRE))
		for sc in squadre_campioni:
			classifica_attuale[sc] = 1 
		classifica_calendari = dict(Counter(classifica_calendari) + Counter(classifica_attuale))

	import pandas as pd
	classifica_list = []
	location = 0
	df = pd.DataFrame(columns=['SQUADRA', 'PUNTI IN CLASSIFICA', 'CALENDARI VINTI'])
	for squadra, vittorie in classifica_calendari.iteritems():
		row = squadra + '@' + str(vittorie)
		df.loc[location] = row.split('@')
		location = location + 1
	df = df.sort(columns=['CALENDARI VINTI'], ascending=False)
	df.to_csv(Costanti.FILENAME_OUTPUT, sep=';', index=False)
 
	
main("Calendario_Paperopoli.xlsx")
	
