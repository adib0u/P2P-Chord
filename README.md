# P2P-Chord

## Utilisation

	python3 join_network.py

## Classe Pair

- Un Ip
- Un Hash
- Une table de routage étant un dictionnaire de tuple : ({hash->(hash->Ip)},...)
- Les données gérée par le pair

## Requêtes

	REQUEST_SUCC
	REQUEST_ROUTES
	REQUEST_UPDATE_SUCC
	REQUEST_DATA_RELOCATE

	DATA_MSG
	DATA_ADD_CHECK
	DATA_ADD
	DATA_GET_CHECK
	DATA_GET
