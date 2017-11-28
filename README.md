# Algo de répartition des PIFE
## AURARD - GIORDANI - ROIG

/!\ Attention : notre algo ne fonctionne pas sur les préférences de la promotion (trop gourmand en RAM => fait crasher le PC) /!\

Pour exécuter ce programme, 2 possibilités s'offre à vous : 

' python algo.py '

Dans ce cas-là, le programme vous demandera de saisir un nombre d'élèves et génèrera une matrice de préférences aléatoire. 

' python algo.py fichier.csv '

L'algorithme sera appliqué sur le fichier .csv. Celui-ci doit avoir la forme suivante : 

Nom,x,y,z

x,-1,B,AB

y,P,-1,TB

z,B,AB,-1

Avec :
* x,y,z le nom des élèves.
* TB,B,AB,P,I,AR les mentions entre élèves.
* -1 pour la mention d'un élève envers lui-même.
