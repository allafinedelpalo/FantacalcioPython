from properties import Costanti

class Giornata(object):
    """Classe per gestire le giornate"""
    

    def __init__(self, n_giornata=1):
        self.squadre = []
        self.squadre_pti = {}
        self.squadre_pti_classifica = {}
        self.n_giornata = n_giornata
        self.giocata = False        
        self.nome_giornata = "Giornata ".join(str(self.n_giornata))
    
    @property
    def squadre(self):
        """Lista con l'elenco delle squadre partecipanti"""
        return self.__squadre

    @squadre.setter
    def squadre(self, squadre):
        self.__squadre = squadre

    @property
    def squadre_pti(self):
        """Dizionario formato da
        key: nome squadra
        value: fantapunti giornata"""
        return self.__squadre_pti

    @squadre_pti.setter
    def squadre_pti(self, squadre_pti):
        self.__squadre_pti = squadre_pti

    @property
    def squadre_pti_classifica(self):
        """Dizionario formato da
        key: nome squadra
        value: punti giornata"""        
        return self.__squadre_pti_classifica

    @squadre_pti_classifica.setter
    def squadre_pti_classifica(self, squadre_pti_classifica):
        self.__squadre_pti_classifica = squadre_pti_classifica

    @property
    def n_giornata(self):
        """Numero d'ordine della gioranta"""
        return self.__n_giornata

    @n_giornata.setter
    def n_giornata(self, n_giornata):
        self.__n_giornata = n_giornata

    @property
    def nome_giornata(self):
        """Nome identificativo della gioranta"""
        return self.__nome_giornata

    @nome_giornata.setter
    def nome_giornata(self, nome_giornata):
        self.__nome_giornata = nome_giornata

    @property
    def giocata(self):
        """True se le squadre hanno punti nella giornata; False altrimenti"""
        return self.__giocata

    @giocata.setter
    def giocata(self, giocata):
        self.__giocata = giocata

    def __str__(self):
        """Restituisce una stringa composta dal nome della giornata
        e dai punti fatti dalle squadre"""
        return self.nome_giornata + '\n' + '\n'.join(['{} {}'.format(squadra,str(pti)) 
            for (squadra, pti) in zip(self.squadre_pti.keys(), self.squadre_pti.values())])
