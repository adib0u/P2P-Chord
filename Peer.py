# Classe Peer


class Peer :

	def __init__(self, ip, hash) :
		""" Constructeur de la classe Peer
			Prend en paramètres une ip et le hash associé à cette ip """
		self.ip = ip
		self.hash = hash
		self.routing = {} # Dictionnaire qui correspondond à la table de routage
	
	#-----------------------------------------------------------------------------------------------

	def getIP(self) :
		return self.ip


	def getHash(self) :
		return self.hash


	def getRoute(self, hash) :
		return hash, self.routing[hash]

	#-----------------------------------------------------------------------------------------------

	def addRoute(self, hash, hashSucc, ipSucc) :
		""" Méthode qui permet d'ajouter une route à la table de routage
			Route = hash:hash du successeur:ip du successeur """
		self.routing[hash] = (hashSucc, ipSucc)

