# P2P-Chord

## Classe Pair

- Un Ip
- Un Hash
- Une table de routage étant un dictionnaire de tuple : ({hash->(hash->Ip)},...)

## Script : rejoindre un réseau

1. récupérer l'IP
2. demander le hach au hashServeur
3. créer le Pair
4. Demander le point d'entrée à WelcomeServeur
5. Ajouter le pair au réseau :
    - mettre à jour sa table de routage
    - mettre à jour celle de son prédesceceur et de son sucesseur
