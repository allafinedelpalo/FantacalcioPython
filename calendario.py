from properties import Costanti
import bisect
from collections import Counter


class Calendario(object):
	"""Classe per gestire un calendario
	Comprende il calcolo della classifica per tutte le partite giocate"""
	
	
	def __init__(self, permutation, giornate):
		self.permutation = permutation
		self.giornate = giornate
		self.classifica = dict(zip(self.permutation, [0]*Costanti.NUM_SQUADRE))
		self.diz_segnaposti = dict(zip(Costanti.SEGNAPOSTI, self.permutation))
		self.calendario_custom = []
		self.pti_primo = 0
		self.squadre_campioni = []
		for segnaposti_giornata in Costanti.CALENDARIO_SEGNAPOSTI_COMPLETO:
			segnaposti_giornata_custom = [Costanti.SEGNAPOSTO]*Costanti.NUM_SQUADRE
			for ind, segnaposto in enumerate(segnaposti_giornata):
				segnaposti_giornata_custom[ind] = self.diz_segnaposti[segnaposto]
			self.calendario_custom.append(segnaposti_giornata_custom)

	@property
	def permutation(self):
		"""Una permutazione (lista) delle squadre partecipanti"""
		return self.__permutation

	@permutation.setter
	def permutation(self, permutation):
		self.__permutation = permutation
	
	@property
	def giornate(self):
		"""Lista di oggeti Giornata che compongono il Calendario"""
		return self.__giornate

	@giornate.setter
	def giornate(self, giornate):
		self.__giornate = giornate

	@property
	def classifica(self):
		"""Dizionario che mantiene la classifica per il Calendario
		key: nome squadra
		value: punti in classifica"""
		return self.__classifica

	@classifica.setter
	def classifica(self, classifica):
		self.__classifica = classifica

	@property
	def diz_segnaposti(self):
		"""Dizionario formato da:
		key: lettera segnaposto
		value: nome squadra"""
		return self.__diz_segnaposti

	@diz_segnaposti.setter
	def diz_segnaposti(self, diz_segnaposti):
		self.__diz_segnaposti = diz_segnaposti					

	@property
	def calendario_custom(self):
		"""Lista di liste. Ogni lista-elemento rappresenta una giornata.
		La lista-elemento contiene l'elenco	delle squadre partecipanti 
		in 'ordine di match':
		es. TeamA vs TeamB, TeamC vs TeamD
		    [TeamA, TeamB, TeamC, TeamD]"""		
		return self.__calendario_custom

	@calendario_custom.setter
	def calendario_custom(self, calendario_custom):
		self.__calendario_custom = calendario_custom

	@property
	def pti_primo(self):
		"""Punti in classifica dei primi"""
		return self.__pti_primo

	@pti_primo.setter
	def pti_primo(self, pti_primo):
		self.__pti_primo = pti_primo

	@property
	def squadre_campioni(self):
		"""Lista con i nomi delle squadre prime in classifica"""
		return self.__squadre_campioni

	@squadre_campioni.setter
	def squadre_campioni(self, squadre_campioni):
		self.__squadre_campioni = squadre_campioni

	def get_squadra_campione(self):
		"""Restituisce la lista delle squadre campioni
		Se Costanti.PARIMETRO = True restituisce una lista di un elemento (concatenazione delle squadre campioni)
		Altrimenti restituisce una lista con tutte le squadre alla prima posizione"""
		if Costanti.PARIMERITO:
			return [' / '.join(self.squadre_campioni) + Costanti.SEPARATOR + str(self.pti_primo)]
		else:
			return [sc + Costanti.SEPARATOR + str(self.pti_primo) for sc in self.squadre_campioni]
	
	def calcola_classifica(self, ultima_giornata=Costanti.ULTIMA_GIORNATA):
		"""Calcola la classifica fino alla giornata numero 'ultima_giornata'
		per tutte le giornate con flag 'giocata'=True"""
		for g in self.giornate[:ultima_giornata]:
			if g.giocata:
				self.calcola_giornata(g)
				self.classifica = dict(Counter(g.squadre_pti_classifica) + Counter(self.classifica))
		self.pti_primo = max(self.classifica.values())
		self.squadre_campioni = [k for k,v in self.classifica.iteritems() if v==self.pti_primo]
		self.squadre_campioni.sort()
		
	def calcola_giornata(self, giornata):
		"""Calcola tutte le partite della giornata
		attribuendo i punti vittoria, pareggio o sconfitta alle squadre"""
		scontri_giornata = self.calendario_custom[giornata.n_giornata-1]
		for indx in xrange(0, len(scontri_giornata), 2):
			[pti_casa, pti_fuori] = self.calcola_partita(giornata.squadre_pti[scontri_giornata[indx]], 
				giornata.squadre_pti[scontri_giornata[indx+1]])
			giornata.squadre_pti_classifica[scontri_giornata[indx]] = pti_casa
			giornata.squadre_pti_classifica[scontri_giornata[indx+1]] = pti_fuori	 
		  	
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
		for giornata_custom in self.calendario_custom:
			print 'Giornata {}'.format(str(n_giornata))
			for i in xrange(0, Costanti.NUM_SQUADRE, 2):
				print '{} - {}'.format(str(giornata_custom[i][:3]), str(giornata_custom[i+1][:3]))
			print
			n_giornata += 1
				
	def print_classifica(self):
		"""Stampa la classifica"""
		for squadra, punti in sorted(self._classifica.iteritems(), key=lambda (k,v): (v,k), reverse=True):
			print '{} \t\t {}'.format(squadra, str(punti))
