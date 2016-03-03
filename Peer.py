# Classe Peer

import socket as ss


class Peer :

	PORT = 9000

	REQUEST_SUCC = "Qui est mon successeur ?"
	REQUEST_ROUTES = "Donne moi tes routes"

	RESPONSE_YES = "Yes"

	def __init__(self, ip, hash) :
		""" Constructeur de la classe Peer
			Prend en paramètres une ip et le hash associé à cette ip """
		self.ip = ip
		self.hash = hash
		self.routing = {} # Dictionnaire qui correspond à la table de routage
	
	#-----------------------------------------------------------------------------------------------

	def getIP(self) :
		return self.ip


	def getHash(self) :
		return self.hash


	def getRoute(self, hash) :
		return self.routing[hash]


	def getAllRoutes(self) :
		return self.routing

	def getSuccesseur(self) :
		return self.routing[self.hash]

	#-----------------------------------------------------------------------------------------------

	def addRoute(self, hash, hashSucc, ipSucc) :
		""" Permet d'ajouter une route à la table de routage
			Route = hash:hash du successeur:ip du successeur """
		self.routing[hash] = (hashSucc, ipSucc)

	def enterNetwork(self, partner = "0.0.0.0") :
		""" Permet d'ajouter un pair dans le réseau """
		if partner == "0.0.0.0" :
			addRoute(self.hash, self.hash, self.ip)

		else :
			sock = ss.socket()
			sock.connect( (partner, PORT) )
			# Le pair envoie son hash
			sock.send(str.encode(self.hash + "\n"))
			# Le pair demande son successeur
			sock.send( str.encode(REQUEST_SUCC + "\n") )
			pred_hash, pred_ip = sock.recv(1024).decode().split("\t")


	def run(self) :
		""" Permet d'écouter et traiter les requètes """
		sock = ss.socket()
		sock.bind( ('', PORT) )
		sock.listen(1)
		while True :
			conn, addr = sock.accept()
			# On reçoit l'identifiant du pair concerné
			idPair = sock.recv(1024)
			# On reçoit la requète
			request = sock.recv(1024)

			if request == REQUEST_SUCC :
				self.whoAreMyNeighbors(idPair, sock)

			sock.close()


	def whoAreMyNeighbors(self, hashPeer, sock) :
		""" """
		if self.hash < hashPeer and self.getSuccesseur() > hashPeer :
			sock.send(str.encode(
				self.hash + "\t" + 
				self.ip + "\t" + 
				self.getSuccesseur()[0] + "\t" + 
				self.getSuccesseur()[1] + "\n"
			))
		else :
			sock2 = ss.socket()
			sock2.connect( (self.getSuccesseur()[1], PORT) )
			sock2.send(str.encode(hashPeer + "\n"))
			sock2.send( str.encode(REQUEST_SUCC + "\n") )
			predecessor = sock.recv(1024).decode()
			sock2.close()
			sock.send(str.encode(predecessor + "\n"))


