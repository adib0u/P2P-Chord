# Script creating a peer and joining a network
import socket

# Récupération de l'ip de la machine actuel
ipClient = socket.gethostbyname(socket.gethostname())
print(ipClient)

# demande de hash au HashServer
sock = socket()
print("Saisir ip du serveur de hash")
ipHashServeur = input()
sock.connect( ipHashServeur, 8001 )
sock.send( ipClient )
hashClient = sock.recv( 4096 )
sock.close()

print(hashClient)




