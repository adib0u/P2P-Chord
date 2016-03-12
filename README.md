# P2P-Chord

## Classe Pair

- Un Ip
- Un Hash
- Une table de routage étant un dictionnaire de tuple : ({hash->(hash->Ip)},...)

## Script : rejoindre un réseau

1. récupérer l'IP OK 
2. demander le hach au hashServeur OK 
3. créer le Pair OK
4. Demander le point d'entrée à WelcomeServeur OK 
5. Récupérer successeur et prédécesseur depuis le point d'entrée OK
6. Ajouter le pair au réseau : 
    - mettre à jour sa table de routage
    - mettre à jour celle de son prédesceceur et de son sucesseur

## Travail à faire  

1. Communication avec le Monitor Serveur
2. Table de routage plsu évolués comprenant plusieurs successeurs
3. Communication entre les pairs 
4. 
