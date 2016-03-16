# Classe Peer

import socket as ss
import threading as th

class Peer (th.Thread) :

	PORT = 4711

	REQUEST_SUCC = "Qui est mon successeur ?"
	REQUEST_ROUTES = "rt?"
	REQUEST_UPDATE_SUCC = "Je suis ton nouveau successeur"

	DATA_MSG = "msg"
	DATA_ADD_CHECK = "est-ce que les données appartiennent à ton successeur"
	DATA_ADD = "tiens ce sont tes données"
	DATA_GET_CHECK = "je cherche telles données, tu les as ?"
	DATA_GET = "t'as ce truc file le moi"

	def __init__(self, ip, hash) :
		""" Constructeur de la classe Peer
			Prend en paramètres une ip et le hash associé à cette ip 
		"""
		th.Thread.__init__(self)
		self.ip = ip
		self.hash = hash
		self.routing = {} # Dictionnaire qui correspond à la table de routage
		self.datas = {} # Données gérées par le pair
	
	#- getter & setter -----------------------------------------------------------------------------

	def getIP(self) :
		return self.ip

	def getHash(self) :
		return self.hash

	def getRoute(self, hash) :
		return self.routing[hash]

	def getAllRoutes(self) :
		return self.routing

	def addRoute(self, hash, hashSucc, ipSucc) :
		""" Permet d'ajouter ou remplacer une route dans la table de routage
			Route = hash:hash du successeur:ip du successeur """
		self.routing[hash] = (hashSucc, ipSucc)

	def getSuccesseur(self) :
		return self.routing[self.hash]

	def addData(self, hashData, data) :
		print("je prends en charge " + hashData + " : " + data )
		self.datas[hashData] = data

	#- network entry -------------------------------------------------------------------------------

	def enterNetwork(self, partner = "0.0.0.0") :
		""" Permet d'ajouter un pair dans le réseau """
		if partner == "0.0.0.0" :
			self.addRoute(self.hash, self.hash, self.ip)

		else :
			sock = ss.socket()
			sock.connect( (partner, Peer.PORT) )
			# Le pair envoie son hash et demande son successeur
			sock.sendall(str.encode(self.hash + "\t" + Peer.REQUEST_SUCC + "\n"))
			print("> envoi id + requête : " + Peer.REQUEST_SUCC)
			pred_hash, pred_ip, succ_hash, succ_ip = sock.recv(1024).decode().rstrip().split("\t")
			print("> réponse reçue")
			print("- " + pred_hash)
			print("- " + pred_ip)
			print("- " + succ_hash)
			print("- " + succ_ip )
			sock.close()
			# Il ajoute la route vers son successeur
			self.addRoute(self.hash, succ_hash, succ_ip)
			print("> successeur ajouté")
			# Il informe son prédécesseur qu'il est son nouveau successeur
			sock = ss.socket()
			sock.connect( (pred_ip, Peer.PORT) )
			sock.sendall(str.encode(self.hash + "\t" + Peer.REQUEST_UPDATE_SUCC + "\n"))
			sock.close()
			print("> prédécesseur notifié ")

	#- thread --------------------------------------------------------------------------------------

	def run(self) :
		""" Permet d'écouter et traiter les requètes """
		sock = ss.socket()
		sock.bind( ('', Peer.PORT) )
		sock.listen(1)
		while True :
			conn, addr = sock.accept()
			print("> Connexion établie")
			# 1- On reçoit l'identifiant du pair concerné et sa requête
			request = conn.recv(1024).decode().rstrip()

			# 2- si la requête viens d'un pair (et pas du moniteur)
			if "\t" in request :
				request_part = request.split("\t")
				idPair, request = request_part[0], request_part[1]
				if len(request_part) > 2 :
					params = request_part[2:]
				print("> requête de " + idPair + " à traiter : " + request)

			# 3- switch sur les requêtes
			if request == Peer.REQUEST_SUCC:
				self.whoAreMyNeighbors(idPair, conn)

			elif request == Peer.REQUEST_UPDATE_SUCC :
				self.addRoute(self.hash, idPair, addr[0])

			elif request == Peer.REQUEST_ROUTES :
				self.sendRoutes(conn)

			elif request == Peer.DATA_MSG :
				self.receiveMsg(idPair, params[0], params[1])

			elif request == Peer.DATA_ADD_CHECK :
				self.dataCheckAuto(params[0], params[1])

			elif request == Peer.DATA_ADD :
				self.addData(params[0], params[1])

			elif request == Peer.DATA_GET_CHECK :
				self.getDataAuto(idPair, params[0])

			elif request == Peer.DATA_GET :
				self.sendData(idPair, params[0])
			
			print("> requête " + request + " traitée\n")

		sock.close()

	#- request treatment ---------------------------------------------------------------------------

	#-----------------------#
	# Entrée dans le réseau #
	#-----------------------#

	def whoAreMyNeighbors(self, hashPeer, conn) :
		hashSucc =  self.getSuccesseur()[0]
		print( self.hash + " < " + hashPeer + " and " + hashSucc + " > " + hashPeer )

		if ((self.hash < hashPeer and hashSucc > hashPeer )
		 or (hashSucc < self.hash and (hashPeer > self.hash or hashPeer < hashSucc)) 
		 or (self.hash == hashSucc)) :
			conn.sendall(str.encode(
				self.hash + "\t" + 
				self.ip + "\t" + 
				hashSucc + "\t" + 
				self.getSuccesseur()[1] + "\n"
			))
		else :
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT) )
			sock2.sendall(str.encode(hashPeer + "\t" + Peer.REQUEST_SUCC + "\n"))
			predecessor = sock2.recv(1024).decode()
			sock2.close()
			conn.sendall(str.encode(predecessor + "\n"))

	def sendRoutes(self, conn) :
		routes = ""
		for k in self.routing :
			routes += k + ":" + str(self.routing[k][0]) + ":" + str(self.routing[k][1]) + "\n"
		routes += "end"
		conn.sendall(str.encode(routes + "\n"))

	#------------------#
	# Envoi de message #
	#------------------#

	def sendMsg(self):
		dest = input("destinataire #!> ")
		msg = input("message #!> ")

		sock2 = ss.socket()
		sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
		sock2.sendall(str.encode(self.hash + "\t" + Peer.DATA_MSG + "\t" + dest + "\t" + msg + "\n"))
		sock2.close()

	def sendMsgAuto(self, dest, msg):
		sock2 = ss.socket()
		sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
		sock2.sendall(str.encode(self.hash + "\t" + Peer.DATA_MSG + "\t" + dest + "\t" + msg + "\n"))
		sock2.close()

	#-----------------------#
	# Tansmition de message #
	#-----------------------#

	def receiveMsg(self, exp, dest, msg):
		# si le message nous est destiné on l'affiche
		if dest == self.hash:
			print("> msg from " + exp + " : " + msg)
			# if msg != "~ roger that ~" and msg != "~ contact failed ~" :
			# 	self.sendMsgAuto(exp, "~ roger that ~")

		# si le message est déstiné à un pair entre nous et notre successeur on ne le transmet pas
		elif ((self.hash < dest and self.getSuccesseur()[0] > dest )
		 or (self.getSuccesseur()[0] < self.hash and (dest > self.hash or dest < self.getSuccesseur()[0])) 
		 or (self.hash == self.getSuccesseur()[0])):
			print("> msg destroyed")
			self.sendMsgAuto(exp, "~ contact failed ~")
		# sinon on le transmet
		else:
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
			sock2.sendall(str.encode(exp + "\t" + Peer.DATA_MSG + "\t" + dest + "\t" + msg + "\n"))
			sock2.close()

	#------------------#
	# Ajout de données #
	#------------------#

	def dataCheck(self) :
		data = input("donnée #!> ")

		# On demande le hash de la donnée au HashServer
		ipHashServeur = input("Saisir ip du serveur de hash #!> ")
		sock = ss.socket()
		sock.connect( (ipHashServeur, 8001) )
		sock.send( str.encode(data + "\n") )
		hashData = sock.recv( 1024 ).decode().rstrip()
		sock.close()

		self.dataCheckAuto(hashData, data)


	def dataCheckAuto(self, hashData, data):
		# On regarde si la donnée doit appartenir à notre successeur
		# Si oui on lui dit de la prendre en charge
		if ((self.hash < hashData and self.getSuccesseur()[0] > hashData )
		 or (self.getSuccesseur()[0] < self.hash and (hashData > self.hash or hashData < self.getSuccesseur()[0])) 
		 or (self.hash == self.getSuccesseur()[0])):
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
			sock2.sendall(str.encode(self.hash + "\t" + Peer.DATA_ADD + "\t" + hashData + "\t" + data + "\n"))
			sock2.close()
		# Sinon on transmet la demande
		else :
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
			sock2.sendall(str.encode(self.hash + "\t" + Peer.DATA_ADD_CHECK + "\t" + hashData + "\t" + data + "\n"))
			sock2.close()

	#-------------------#
	# Accès aux données #
	#-------------------#

	def getData(self):
		hashData = input("id de la donnée #!> ")
		self.getDataAuto(self.hash, hashData)

	def getDataAuto(self, exp, hashData):
		# On regarde si la donnée appartient à notre successeur
		# Si oui on lui dit de l'envoyer au demandeur
		if ((self.hash < hashData and self.getSuccesseur()[0] > hashData )
		 or (self.getSuccesseur()[0] < self.hash and (hashData > self.hash or hashData < self.getSuccesseur()[0])) 
		 or (self.hash == self.getSuccesseur()[0])):
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
			sock2.sendall(str.encode(exp + "\t" + Peer.DATA_GET + "\t" + hashData + "\n"))
			sock2.close()
		# Sinon on transmet la demande
		else :
			sock2 = ss.socket()
			sock2.connect( (str(self.getSuccesseur()[1]), Peer.PORT ) )
			sock2.sendall(str.encode(exp + "\t" + Peer.DATA_GET_CHECK + "\t" + hashData + "\n"))
			sock2.close()

	def sendData(self, exp, hashData):
		""" Envoi d'une donnée que le pair gère ou info 404 """
		if hashData in self.datas:
			self.sendMsgAuto(exp, "> donnée " + hashData + " : " + self.datas[hashData])

		else :
			self.sendMsgAuto(exp, "> donnée " + hashData + " inexistante ")
