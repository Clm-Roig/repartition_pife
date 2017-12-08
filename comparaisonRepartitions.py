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
def meilleuresRepartsParPoints(listeReparts, matrice):
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


'''
    Retourne la meilleure répartition parmi celles fournies grâce
    à l'algorithme de comparaison 2 à 2.
'''
def meilleuresRepartsParComp(tabReparts, matrice):
    scoresTotaux = [0] * len(tabReparts)
    scoreRepart1 = 0
    scoreRepart2 = 0
    indexRepart1 = 0
    indexRepart2 = 0

    # On compare une répartition avec toutes celles après
    for repart in tabReparts:
        listeMentions1 = []
        indexRepart1 = tabReparts.index(repart)

        # get Mentions repart 1
        for group in repart:
            for eleve in group:
                for otherEleve in group:
                    mention = matrice[eleve][otherEleve]
                    if(mention != -1):
                        listeMentions1.append(mention)
                        listeMentions1.sort()

        for repart2 in tabReparts[indexRepart1+1:]:
            listeMentions2 = []
            indexRepart2 = tabReparts.index(repart2)

            scoreRepart1 = 0
            scoreRepart2 = 0

            # get Mentions repart 2
            for group2 in repart2:
                for eleve2 in group2:
                    for otherEleve2 in group2:
                        mention = matrice[eleve2][otherEleve2]
                        if(mention != -1):
                            listeMentions2.append(mention)
                            listeMentions2.sort()

            # Compare both mentions lists
            i = 0
            for mention1 in listeMentions1:
                if(mention1 > listeMentions2[i]):
                    scoreRepart1 = scoreRepart1 + 1
                if(mention1 < listeMentions2[i]):
                    scoreRepart2 = scoreRepart2 + 1
                i += 1

            if(scoreRepart1 > scoreRepart2):
                scoresTotaux[indexRepart1] += 1
            if(scoreRepart2 > scoreRepart1):
                scoresTotaux[indexRepart2] += 1
    # end comp

    meilleuresReparts = []
    m = max(scoresTotaux)
    i=0
    for score in scoresTotaux:
        print i," : ", score
        i+=1
        if(score == m):
            meilleuresReparts.append(tabReparts[scoresTotaux.index(score)])
    return meilleuresReparts
