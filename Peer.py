# Classe Peer

import socket as ss
import time

class Peer :

	PORT = 4711

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
			self.addRoute(self.hash, self.hash, self.ip)

		else :
			sock = ss.socket()
			sock.connect( (partner, Peer.PORT) )
			# Le pair envoie son hash
			sock.send(str.encode(self.hash + "\n"))
			print("> envoi id")
			# Le pair demande son successeur
			sock.send( str.encode(Peer.REQUEST_SUCC + "\n") )
			print("> envoi requête")
			pred_hash, pred_ip, succ_hash, succ_ip = sock.recv(1024).decode().split("\t")
			print("> réponse reçue")
			sock.close()


	def run(self) :
		""" Permet d'écouter et traiter les requètes """
		sock = ss.socket()
		sock.bind( ('', Peer.PORT) )
		sock.listen(1)
		while True :
			conn, addr = sock.accept()
			print("> Connexion établie")
			# On reçoit l'identifiant du pair concerné
			idPair = conn.recv(1024).decode()
			# On reçoit la requète
			request = conn.recv(1024).decode()

			print("> requête à traiter : " + request)

			if request == Peer.REQUEST_SUCC :
				self.whoAreMyNeighbors(idPair, sock)
				print("> requête " + request + "traitée")

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
			sock2.connect( (self.getSuccesseur()[1], Peer.PORT) )
			sock2.send(str.encode(hashPeer + "\n"))
			sock2.send( str.encode(Peer.REQUEST_SUCC + "\n") )
			predecessor = sock.recv(1024).decode()
			sock2.close()
			sock.send(str.encode(predecessor + "\n"))


