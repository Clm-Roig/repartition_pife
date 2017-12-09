# Algo de répartition des PIFE
## AURARD - GIORDANI - ROIG

/!\ Attention : notre algo ne fonctionne pas sur les préférences de la promotion (trop gourmand en RAM => fait crasher le PC) /!\

Pour exécuter ce programme, 2 possibilités s'offre à vous :

> python algo.py

Dans ce cas-là, le programme vous demandera de saisir un nombre d'élèves et génèrera une matrice de préférences aléatoire.

> python algo.py fichier.csv

L'algorithme sera appliqué sur le fichier .csv. Celui-ci doit avoir la forme suivante :

Nom,x,y,z

x,-1,B,AB

y,P,-1,TB

z,B,AB,-1

Avec :
* x,y,z le nom des élèves.
* TB,B,AB,P,I,AR les mentions entre élèves.
* -1 pour la mention d'un élève envers lui-même.

**Exemple :** ici, y évalue x à P (Passable) et x évalue y à B (Bien).


La / les meilleure(s) répartition(s) (avec 372 points) est / sont :
 __________________________
['Yves-alain Agbodjogbe', 'Joris Granel', 'Justin Escalier']
['James Terrien', 'Cyril Pluche', 'Alexandre Bottero']
['Paul Contremoulin', 'Ophelie Piekarek', 'Megane Wintz']
['Assil El-Yahyaoui', 'Chloe Dalger', 'Mahe Spaenle']
['Kevin Hassan', 'Mehdi Delvaux', 'Godefroi Roussel']
['Achraf El-Mahmoudi', 'Jade Hennebert', 'Cyprien Legrand']
['Enzo Fabre', 'Vincent Herreros', 'Marion Rul']
['Clement Loubiere', 'Tristan Riviere', 'Clement Fournier']
['Kevin Giordani', 'Hugo Maitre', 'Toinon Georget']
['Maxime Soustelle', 'Alex Aufauvre', 'Johan Brunet']
['Romain Thevenon', 'Clement Roig', 'Loris Zirah']
['Fabien Turgut', 'Hamelina Ehamelo']
['Hugo Fazio', 'Thais Aurard']
['Soufiane Benchraa', 'Melvil Donnart']
['Florent Berland', 'Matthieu Dye']
['Elyess Doudech', 'Loic Combis']
['Hugo Lecler', 'Mohamed-Iheb Faiza']
['San-Wei Lee', 'Amin Bazaz']
 __________________________
['Yves-alain Agbodjogbe', 'Joris Granel', 'Justin Escalier']
['James Terrien', 'Cyril Pluche', 'Alexandre Bottero']
['Paul Contremoulin', 'Ophelie Piekarek', 'Megane Wintz']
['Assil El-Yahyaoui', 'Chloe Dalger', 'Mahe Spaenle']
['Kevin Hassan', 'Mehdi Delvaux', 'Godefroi Roussel']
['Marion Rul', 'Enzo Fabre', 'Hamelina Ehamelo']
['Achraf El-Mahmoudi', 'Jade Hennebert', 'Cyprien Legrand']
['Clement Loubiere', 'Tristan Riviere', 'Clement Fournier']
['Kevin Giordani', 'Hugo Maitre', 'Toinon Georget']
['Maxime Soustelle', 'Alex Aufauvre', 'Johan Brunet']
['Romain Thevenon', 'Clement Roig', 'Loris Zirah']
['Hugo Fazio', 'Thais Aurard']
['Fabien Turgut', 'Vincent Herreros']
['Soufiane Benchraa', 'Melvil Donnart']
['Florent Berland', 'Matthieu Dye']
['Elyess Doudech', 'Loic Combis']
['Hugo Lecler', 'Mohamed-Iheb Faiza']
['San-Wei Lee', 'Amin Bazaz']
 __________________________
['James Terrien', 'Cyril Pluche', 'Alexandre Bottero']
['Paul Contremoulin', 'Ophelie Piekarek', 'Megane Wintz']
['Assil El-Yahyaoui', 'Chloe Dalger', 'Mahe Spaenle']
['Joris Granel', 'Justin Escalier', 'Mehdi Delvaux']
['Thais Aurard', 'Fabien Turgut', 'Hamelina Ehamelo']
['Achraf El-Mahmoudi', 'Jade Hennebert', 'Cyprien Legrand']
['Enzo Fabre', 'Vincent Herreros', 'Marion Rul']
['Clement Loubiere', 'Tristan Riviere', 'Clement Fournier']
['Kevin Giordani', 'Hugo Maitre', 'Toinon Georget']
['Maxime Soustelle', 'Alex Aufauvre', 'Johan Brunet']
['Kevin Hassan', 'Romain Thevenon', 'Loris Zirah']
['Godefroi Roussel', 'Clement Roig']
['Hugo Fazio', 'Yves-alain Agbodjogbe']
['Soufiane Benchraa', 'Melvil Donnart']
['Florent Berland', 'Matthieu Dye']
['Elyess Doudech', 'Loic Combis']
['Hugo Lecler', 'Mohamed-Iheb Faiza']
['San-Wei Lee', 'Amin Bazaz']
