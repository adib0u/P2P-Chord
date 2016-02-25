# Script creating a peer and joining a network

import socket as ss
from Peer import Peer

# Récupération de l'ip de la machine actuel
ipClient = ss.gethostbyname(ss.gethostname())
print("> IP client : " + ipClient)

# Demande de hash au HashServer

print("Saisir ip du serveur de hash")
ipHashServeur = input()

sock = ss.socket()
sock.connect( (ipHashServeur, 8001) )
sock.send( str.encode(ipClient + "\n") )
hashClient = sock.recv( 1024 ).decode()
hashClient = hashClient[:-1]

sock.close()

print("> Hash client : " + hashClient)

# Création pair

peer1 = Peer( ipClient, hashClient)

print("Saisir ip du serveur d'acceuil")
ipWelcomeServeur = input()

sock = ss.socket()
sock.connect( (ipWelcomeServeur, 8000) )
print("yo:" + hashClient + ":" + ipClient + "\n")
sock.send( str.encode("yo:" + hashClient + ":" + ipClient + "\n") )
welcomeAnswer = sock.recv(1024).decode()
sock.close()

print(welcomeAnswer)
print("> Pair ajouté au réseau")
