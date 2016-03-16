# Script creating a peer and joining a network

import socket as ss
from Peer import Peer
from User_interaction import User_interaction

# Récupération de l'ip de la machine actuel
ipClient = ss.gethostbyname(ss.gethostname())
print("> Votre IP : " + ipClient)

# Demande de hash au HashServer

ipServeur = input("Saisir ip du serveur de hash et d'accueil #!> ")

sock = ss.socket()
sock.connect( (ipServeur, 8001) )
sock.send( str.encode(ipClient + "\n") )
hashClient = sock.recv( 1024 ).decode()
hashClient = hashClient[:-1]

sock.close()

print("\u001B[31m" + "> Votre identifiant : " + hashClient + "\u001B[0m")

# Création pair

peer1 = Peer( ipClient, hashClient)

sock = ss.socket()
sock.connect( (ipServeur, 8000) )
# print("yo:" + hashClient + ":" + ipClient + "\n")
sock.send( str.encode("yo:" + hashClient + ":" + ipClient + "\n") )
welcomeAnswer = sock.recv(1024).decode()
sock.close()

# print(welcomeAnswer)

if welcomeAnswer == "yaf\n" :
	peer1.enterNetwork()
else :
	peer1.enterNetwork(welcomeAnswer)

print("=== YOU'RE IN DA PLACE")

# on donne la main au pair
peer1_user = User_interaction(peer1)
try:
   peer1.start()
   peer1_user.start()
except:
   print("Erreur: impossible de démarer les threads")
