# Classe Peer

import socket as ss


class Peer :

	PORT = 9000
	REQUEST_ROUTES = "Donne moi tes routes"

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


	def getAllRoutes(self) :
		return self.routing

	#-----------------------------------------------------------------------------------------------

	def addRoute(self, hash, hashSucc, ipSucc) :
		""" Méthode qui permet d'ajouter une route à la table de routage
			Route = hash:hash du successeur:ip du successeur """
		self.routing[hash] = (hashSucc, ipSucc)


	def enterNetwork(self, partner = "0.0.0.0") :
		if partner == "0.0.0.0" :
			addRoute(self.hash, self.hash, self.ip)

		else :
			sock = ss.socket()
			sock.connect( (partner, PORT) )
			sock.send( str.encode(REQUEST_ROUTES + "\n") )
			#routes = sock.recv(1024).decode()

	def run(self) :
		sock = ss.socket()
		sock.bind( ('', PORT) )
		sock.listen(1)
		while True :
			conn, addr = sock.accept()
			request = sock.recv(1024)

