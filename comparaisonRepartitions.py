#!/usr/bin/env python
# coding: utf-8

'''
    Retourne la valeur d'une répartition en additionant les mentions données par chaque élève.
'''
def pointsRepart(repart, matrice):
    valeurRepart = 0
    for groupe in repart:
        # Valeur du binome
        if(len(groupe) == 2):
            valeurRepart += matrice[groupe[0]][groupe[1]] + matrice[groupe[1]][groupe[0]]
        # Valeur du trinome
        else:
            valeurRepart += matrice[groupe[0]][groupe[1]] + matrice[groupe[1]][groupe[0]]
            valeurRepart += matrice[groupe[0]][groupe[2]] + matrice[groupe[2]][groupe[0]]
            valeurRepart += matrice[groupe[1]][groupe[2]] + matrice[groupe[2]][groupe[1]]
    return valeurRepart

'''
    Retourne la liste des meilleurs répartitions parmi celles fournies.
    Basée sur la méthode des "points" de chaque répartition
'''
def meilleuresReparts(listeReparts, matrice):
    meilleuresReparts = []
    valeurMeilleureRepart = 0
    valeurRepart = 0

    for repart in listeReparts:
        valeurRepart = pointsRepart(repart, matrice)
        if valeurRepart > valeurMeilleureRepart:
            valeurMeilleureRepart = valeurRepart
            meilleuresReparts = []
            meilleuresReparts.append(repart)
        elif valeurRepart == valeurMeilleureRepart:
            meilleuresReparts.append(repart)

    return meilleuresReparts


#def compReparts(tabReparts):
