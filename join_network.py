# Script creating a peer and joining a network
import socket as ss

# Récupération de l'ip de la machine actuel
ipClient = ss.gethostbyname(ss.gethostname())
print(ipClient)

# demande de hash au HashServer

print("Saisir ip du serveur de hash")
ipHashServeur = input()

sock = ss.socket()
sock.connect( (ipHashServeur, 8001) )
sock.send( str.encode(ipClient + "\n") )
hashClient = sock.recv( 1024 ).decode()

sock.close()

print(hashClient)
