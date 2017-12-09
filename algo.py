#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time as time
import random as random
from threading import Thread
import collections
import sys
import csv
import comparaisonRepartitions as compR

global repartition
global tFini
global nbThread
global mentionsClassee

mentionsClassee = [[5,5],[5,4],[4,4],[5,3],[4,3],[3,3],[5,2],[4,2],[3,2],[2,2],
[5,1],[4,1],[3,1],[2,1],[1,1],[5,0],[4,0],[3,0],[2,0],[1,0],[0,0],[-1,-1]]

'''
    File = String pointant sur le fichier csv de la forme :
        -1,B,AB
        TB,-1,AR
        TB,AB,-1
    Les valeurs du fichier sont :
        Tres bien = TB
        ...
        A rejeter = AR
        Diagonale = -1
    nbLignes = nombre de lignes que l'on souhaite lire depuis le CSV
    Renvoie une liste:
        Premier argument = matrice de preferences
        Second argument = liste des eleves
'''
def parseCSV(file, nbLignes):
    tmp = []
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            tmp.append(','.join(row).split(','))
            nbLignes = int(nbLignes) - 1
            if(nbLignes == -1):
                break
    matrice = np.array(tmp)
    return matrice[1:matrice.shape[0],1:matrice.shape[0]],matrice[0][1:matrice.shape[0]]

'''
    Retourne la liste des nbEleves premiers élèves
'''
def getNames(file, nbEleves):
    with open(file) as csvFile:
        reader = csv.reader(csvFile)
        field_names_list = reader.next()
    return field_names_list[1:int(nbEleves)+1]

'''
    Convertie une matrice de la forme :
            [[-1,B,AB]
             [TB,-1,AR]
             [TB,AB,-1]]
    En une matrice de la forme :
            [[-1  3  2]
             [ 4 -1  0]
             [ 4  2 -1]]
    Les valeurs sont :
        5 = TB
        ...
        0 = AR
        -1 = -1
'''
def convertToInt(matrice):
    res = []
    for x in range(0,np.shape(matrice)[0]):
        tmp = []
        for y in range(0,np.shape(matrice)[0]):
            if(matrice[x][y] == "-1"):
                tmp.append(-1)
            elif(matrice[x][y] == "TB"):
                tmp.append(5)
            elif(matrice[x][y] == "B"):
                tmp.append(4)
            elif(matrice[x][y] == "AB"):
                tmp.append(3)
            elif(matrice[x][y] == "P"):
                tmp.append(2)
            elif(matrice[x][y] == "I"):
                tmp.append(1)
            elif(matrice[x][y] == "AR"):
                tmp.append(0)
            else:
                print "error",matrice[x][y]
        res.append(tmp)
    return np.array(res)

'''
    Ecrit dans un fichier csv pointant sur fichier la matrice repartition de la forme :
        [[1,2],
         [3,4,5],
         [6,7],
         [8,9,10]]
    (Les chiffres étant des élèves)
'''
def writeCsv(file,repartition):
    with open(file, 'wb') as csvfile:
        print repartition[0]
        for group in repartition[0]:
            firstEleve = True
            for eleve in group:
                if(not(firstEleve)):
                    csvfile.write(',')
                firstEleve = False
                csvfile.write(eleve)
            csvfile.write('\n')



class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

class combinaisonT(Thread):

    def __init__(self,nbEleves, id, k,group,ranges,repartition,i,trinomes,result):
        Thread.__init__(self)
        self.id = id
        self.k = k
        self.group = group
        self.ranges = ranges
        self.repartition = repartition
        self.i = i
        self.trinomes = trinomes
        self.result = result
        self.nbEleves = nbEleves

    def run(self):
        global tFini
        global nbThread
        tmp = combinaisonBis(self.nbEleves,self.k,self.group,self.ranges,self.repartition,self.i,self.trinomes,self.result)
        tFini = tFini + 1
        toPrint = "Thread n°%d fini. Nb Threads finis : %d/%d" % (self.id, tFini,nbThread)
        Printer(toPrint)

class combinaisonT2(Thread):

    def __init__(self,nbEleves, id, k,group,ranges,repartition,i,result):
        Thread.__init__(self)
        self.id = id
        self.k = k
        self.group = group
        self.ranges = ranges
        self.repartition = repartition
        self.i = i
        self.trinomes = trinomes
        self.result = result
        self.nbEleves = nbEleves

    def run(self):
        global tFini
        global nbThread
        tmp = combinaison(self.k,self.group,self.ranges,self.repartition,self.i,self.result)
        tFini = tFini + 1
        toPrint = "Thread n°%d fini. Nb de Threads finis : %d/%d" % (self.id, tFini,nbThread)
        Printer(toPrint)

def matriceAleatoire(size):
    matrice = np.random.rand(size,size)
    for x in xrange(0,np.shape(matrice)[0]):
        for y in xrange(0,np.shape(matrice)[0]):
            matrice[x][y] = (int)(matrice[x][y] * 6)
    for x in xrange(0,np.shape(matrice)[0]):
        matrice[x][x] = -1
    return matrice

def sontBloquants(group1,group2):
    if len(group1) == 0:
        return False
    for groupInGroup1 in group1:
        for eleveInGroup1 in groupInGroup1:
            for eleveInGroup2 in group2:
                if eleveInGroup1 == eleveInGroup2:
                    return True
    return False

'''
    Vérifie si tous les élèves sont présents dans une liste de binômes.
'''
def canHaveRepartition(binomes, nbEleve):
    tmp = []
    for group in binomes:
        for eleve in group:
            if eleve not in tmp:
                tmp.append(eleve)
    return len(tmp) == nbEleve

def isRepartition(repartition,nbEleve):
    tmp = []
    for group in repartition:
        for eleve in group:
            if eleve in tmp:
                return False
            else:
                tmp.append(eleve)
    return len(tmp) == nbEleve

def ajoutBinome(valueMax,valueMin,matrice,binomes,nboccurences):
    cpt = 0
    for x in range(0,np.shape(matrice)[0]):
        cpt = cpt + 1
        for y in range(cpt,np.shape(matrice)[0]):
            if( ((matrice[x][y] == valueMax) and (matrice[y][x] == valueMax or matrice[y][x] == valueMin)) or ((matrice[y][x] == valueMax) and (matrice[x][y] == valueMax or matrice[x][y] == valueMin)) ):
                existe = False
                for value in binomes:
                    if binomeEqual(value,[x,y]):
                        existe = True
                if not(existe):
                    binomes.append([x,y])
                    nboccurences[x] += 1
                    nboccurences[y] += 1

def binomeEqual(first,second):
    if (first[0] == second[0] or first[0] == second[1]) and (first[1] == second[0] or first[1] == second[1]):
        return True
    return False

def createTrinome(first,second,third):
    listeEleve = []
    for value in first:
        listeEleve.append(value)
    for value in second:
        listeEleve.append(value)
    for value in third:
        listeEleve.append(value)
    a = np.array(listeEleve)
    count = collections.Counter(a)
    if len(count) == 3:
        res = []
        for value in count:
            res.append(value)
        return res
    return ()

def getAvailableTrinomes(binomes,nbOccurences):
    res = []
    for i in xrange(0,len(binomes)):
      for j in xrange(i + 1, len(binomes)):
          for z in xrange(j + 1, len(binomes)):
              if not(binomeEqual(binomes[i],binomes[j])) and not(binomeEqual(binomes[i],binomes[z])) and not(binomeEqual(binomes[j],binomes[z])):
                  tmp = createTrinome(binomes[i],binomes[j],binomes[z])
                  if len(tmp) != 0 and tmp not in res:
                      res.append(tmp)
                      nbOccurences[tmp[0]] += 1
                      nbOccurences[tmp[1]] += 1
                      nbOccurences[tmp[2]] += 1
    return res

'''
    nbEleves : nombre d'élèves considérés dans le group
    group :
    ranges :
    repartition :
    i :
    result : le tableau dans lequel on veut stocker le résultat de la fonction ?
'''
def combinaison(nbEleves,group,ranges,repartition,i,result):
    for x in range(ranges[0],ranges[1]+1):
        if not(sontBloquants(repartition,group[x])):
            repartition.append(group[x])
            if i == nbEleves - 1:
                result.append(list(repartition))
            else:
                combinaison(nbEleves,group,[x+1 , i+1 + len(group) - nbEleves],repartition,len(repartition),result)
            if len(repartition) != 0:
                repartition.pop()
    return True

def combinaisonBis(nbEleves,k,group,ranges,repartition,i,trinomes,result):
    for x in range(ranges[0],ranges[1]+1):
        if not(sontBloquants(repartition,group[x])):
            repartition.append(group[x])
            if i == nbEleves - 1:
                if len(trinomes) != 0:
                    for t in trinomes:
                        if isRepartition((t+repartition),nbEleves):
                            #print "Repartition trouvé !"
                            result.append(repartition + t)
                else:
                    result.append(repartition)
            else:
                combinaisonBis(nbEleves,k,group,[x+1 , i+1 + len(group) - k],repartition,i+1,trinomes,result)
            if len(repartition) != 0:
                repartition.pop()
    return True

def threadedSearch(k,group):
    t = []
    result = []
    for x in range(0,(len(group)-k+1)):
        tmp = combinaisonT(x,k,group,[x,x],[],0,result)
        t.append(tmp)
        tmp.start()

    for value in t:
        value.join()
    return result

def extractGroupWith(group,eleve):
    res = []
    for value in group:
        for x in value:
            if x == eleve:
                res.append(value)
    return res


def deleteElevesFromGroups(groups,repartition):
    res = list(groups)
    for group in repartition:
        for eleve in group:
            for grou in groups:
                for ele in grou:
                    if ele == eleve:
                        try:
                            res.remove(grou)
                        except ValueError:
                            i = 1
    return res

def sortListGroupByOccEleves(group,listOccurencesEleves,nbEleve):
    indexesEleves = []
    for y in range(0,nbEleve):
        indexesEleves.append(y)
    indexesEleves = [x for _,x in sorted(zip(listOccurencesEleves,indexesEleves))]

    sortedBinomes = []
    for value in indexesEleves:
        temp = extractGroupWith(group,value)
        for val in temp:
            if val not in sortedBinomes:
                sortedBinomes.append(val)
    return sortedBinomes

def convertToNames(liste,listeEleves):
    res = []
    for value in liste:
        tmp = []
        for val in value:
            tmp.append(listeEleves[val])
        res.append(tmp)
    return res

def combin(n, k):
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x

def isBetter(mention,ment):
    return mentionsClassee.index(mention) < mentionsClassee.index(ment)

def extractSortedMentions(matrice,eleve):
    listMentions = []
    for otherEleve in range(0,np.shape(matrice)[0]):
        mention = sorted([matrice[eleve][otherEleve],matrice[otherEleve][eleve]],reverse=True)
        if mention not in listMentions:
            if len(listMentions) == 0:
                listMentions.append(mention)
            else:
                idx = 0
                inserted = False
                while not(inserted) and  idx != len(listMentions):
                    if isBetter(mention,listMentions[idx]):
                        listMentions.insert(idx,mention)
                        inserted = True
                    idx = idx + 1
                if not(inserted):
                    listMentions.append(mention)

    return listMentions

def extractBinomesWithEleveAndMention(matrice,eleve,mention):
    listBinomes = []
    for otherEleve in range(0,np.shape(matrice)[0]):
        ment = sorted([matrice[eleve][otherEleve],matrice[otherEleve][eleve]],reverse=True)
        if ment == mention:
            listBinomes.append([eleve,otherEleve])
    return listBinomes


def printEcranAndCSV(repart, i):
    repartNoms = []
    print ' ____________________________ '
    for group in repart:
        groupNom = []
        for eleve in group:
            groupNom.append(listeNoms[eleve])
        repartNoms.append(groupNom)
    for groupe in repartNoms:
        print groupe
    nomFile = "Répartition " + str(i)

    writeCsv(nomFile,[repartNoms])


''' ------------------------------------------ '''
''' --------------- DEBUT ALGO --------------- '''
''' ------------------------------------------ '''

listeEleves = []
listeNoms = []
# Cas 1 : algo.py nbEleves fichier.csv
# => on veut lire les mentions des premiers nbEleves du fichier csv
try:
    res = parseCSV(sys.argv[2], sys.argv[1])
    listeNoms = getNames(sys.argv[2], sys.argv[1])
    matrice = res[0]
    listeEleves = res[1]
    nbEleve = len(listeEleves)
    matrice = convertToInt(matrice)
# Cas 1 : algo.py nbEleves
# => on veut générer une matrice aléatoire de mentions avec nbEleves
except IndexError:
    nbEleve = int(sys.argv[1])
    matrice = matriceAleatoire(nbEleve)
    for x in range(0,nbEleve):
        listeEleves.append(x)

# Variables utilisées
listOccurencesElevesBinomes = [0]*nbEleve
listOccurencesElevesTrinomes = [0]*nbEleve
tFini = 0
binomes = []
trinomes = []
repartitionTotal = []
nbThread = 0
tFini = 0
stopPrinter = False
repartition = []
level = 0
end = False
repartTrouvee = False
nbBinomesNeeded = 0
nbTrinomeNeeded = 0

# Détermination du nb de binomes et nb de trinomes
if nbEleve > 35:
    nbTrinomeNeeded = nbEleve - 36
    nbBinomesNeeded = 54 - nbEleve
else:
    if not(nbEleve % 2 == 0):
        nbTrinomeNeeded = 1
        nbBinomesNeeded = (nbEleve - 3) / 2
    else:
        nbBinomesNeeded = nbEleve / 2

# Print des informations générales avant lancement de l'algo
print 'Matrice des préférences :'
for i in range(nbEleve):
    for j in range(nbEleve):
        print int(matrice[i][j]),
        if(matrice[i][j] == -1):
            print ' ',
        else:
            print '  ',
    print
print "Nombre de binomes recherché : ",nbBinomesNeeded
print "Nombre de trinomes recherché : ",nbTrinomeNeeded,"\n"

while not(end) and not(repartTrouvee):

    # Choix des binômes au-dessus du seuil courant.
    ajoutBinome(mentionsClassee[level][0],mentionsClassee[level][1],matrice,binomes,listOccurencesElevesBinomes)

    print "________________________________________________\n"
    print "Seuil de mentions courant : ", level
    print "Nombre de binomes retenu : ",len(binomes)
    print "Occurrences eleves binomes : ", listOccurencesElevesBinomes
    listeElevesCritiques = [i for i, x in enumerate(listOccurencesElevesBinomes) if x == 0]

    if canHaveRepartition(binomes,nbEleve):
        #print sortListGroupByOccEleves(binomes,listOccurencesElevesBinomes,nbEleve)
        #print "____________________"
        #print sortListGroupByOccEleves(trinomes,listOccurencesElevesTrinomes,nbEleve)

        # Si on n'a pas besoin de trinômes, on va chercher les binômes critiques.
        if nbTrinomeNeeded < 2:
            print "Nb d'occurrences de chaque élève dans les binomes retenus : ", listOccurencesElevesBinomes

            repartitionTotalBinomes = []
            listIndexes = []
            for x in xrange(0,nbEleve):
                listIndexes.append(x)

            sortedElevesByOcc = [x for _,x in sorted(zip(listOccurencesElevesBinomes,listIndexes))]

            print "Elèves triés par nb d'occurrences : ", sortedElevesByOcc

            # On cherche les élèves apparaissant nbOccurencesMin
            listeElevesCritiques = [i for i, x in enumerate(listOccurencesElevesBinomes) if x == min(listOccurencesElevesBinomes)]


            binomesCritiques = []

            for binome in binomes:
                for eleveDuBin in binome:
                    if eleveDuBin in listeElevesCritiques:
                        if binome not in binomesCritiques:
                            binomesCritiques.append(binome)

            print len(binomesCritiques),"Binome(s) critique(s) : " , binomesCritiques
            print "Eleve(s) critique(s) : ",listeElevesCritiques
            # On vérifie d'abord si les binômes critiques sont bloquants ou pas.
            if(min(listOccurencesElevesBinomes) == 1):
                if canHaveRepartition(binomesCritiques,len(listeElevesCritiques)*2):
                    repartitionCritique = binomesCritiques
                    repartitionBinomesNonCrit = []

                    t = []

                    validBinomes = deleteElevesFromGroups(binomes,binomesCritiques)
                    nbBinomesRestantNeeded = nbBinomesNeeded - len(repartitionCritique)
                    if validBinomes >= nbBinomesNeeded:
                        # On va tester toutes les combinaisons possibles avec chaque binome critique.
                        for x in range(0,(len(validBinomes)-nbBinomesRestantNeeded+1)):
                            nbThread = nbThread + 1

                            tmp = combinaisonT2(nbBinomesNeeded*2,nbThread-1,nbBinomesRestantNeeded,validBinomes,[x,x],[],0,repartitionBinomesNonCrit)

                            t.append(tmp)
                            tmp.start()

                    for value in t:
                        value.join()

                    if len(repartitionBinomesNonCrit) > 0:
                        for repartNonCrit in repartitionBinomesNonCrit:
                            if isRepartition(repartNonCrit+binomesCritiques,nbBinomesNeeded*2):
                                repartitionTotalBinomes.append(repartNonCrit+binomesCritiques)
                else:
                    "Pas de repartition possibles car les élèves critiques ne peuvent être associés dans des binomes distincts !"
            else:

                repartitionBinomesCritique = []
                temps = time.time()

                combinaison(len(listeElevesCritiques),binomesCritiques,[0,len(binomesCritiques)-len(listeElevesCritiques)*2+1],[],0,repartitionBinomesCritique)

                temps = time.time() - temps

                toPrint = "%d répartition(s) trouvée(s) pour les binomes critique en : %fs\n" % (len(repartitionBinomesCritique),temps)
                Printer(toPrint)

                if repartitionBinomesCritique > 0:
                    t = []
                    repartitionTotal = []
                    for idx,repartitionCritique in enumerate(repartitionBinomesCritique):
                        validBinomes = deleteElevesFromGroups(binomes,repartitionCritique)
                        nbBinomesRestantNeeded = nbBinomesNeeded - len(repartitionCritique)
                        if len(validBinomes) >= nbBinomesRestantNeeded:
                            toPrint = "Checking for : %s -> %d/%d\n" %(repartitionCritique,idx,len(repartitionBinomesCritique)-1)
                            Printer(toPrint)
                            repartitionBinomesNonCrit = []
                            #combinaison(nbBinomesRestantNeeded,validBinomes,[0,len(validBinomes)-nbBinomesRestantNeeded],[],0,repartitionBinomesNonCrit)
                            t = []

                            for x in range(0,(len(validBinomes)-nbBinomesRestantNeeded+1)):
                                nbThread = nbThread + 1
                                tmp = combinaisonT2(nbBinomesNeeded*2,nbThread-1,nbBinomesRestantNeeded,validBinomes,[x,x],[],0,repartitionBinomesNonCrit)
                                t.append(tmp)
                                tmp.start()

                            for value in t:
                                value.join()


                            if len(repartitionBinomesNonCrit) > 0:
                                for repartNonCrit in repartitionBinomesNonCrit:
                                    if isRepartition(repartNonCrit+repartitionCritique,nbBinomesNeeded*2):
                                        repartitionTotalBinomes.append(repartNonCrit+repartitionCritique)
                        else:
                            print "Ne peut pas repartir les binômes critiques."
                else:
                    "Pas de repartition car on n'as pas pu mettre les élèves critiques ensemble."
            if len(repartitionTotalBinomes) > 0:
                if nbTrinomeNeeded != 0:
                    trinomes = getAvailableTrinomes(binomes,listOccurencesElevesTrinomes)
                    if len(trinomes) != 0:
                        for repartition in repartitionTotalBinomes:
                            for trinome in trinomes:
                                if isRepartition(repartition+[trinome],nbEleve):
                                    repartitionTotal.append(repartition+[trinome])
                else:
                    repartitionTotal = repartitionTotalBinomes

        # On a besoin de trinômes.
        else:
            dataEleves = []
            for eleve in range(0,nbEleve):
                dataEleve = []
                mentions = extractSortedMentions(matrice,eleve)
                dataEleve.append(mentions)
                binomeEleve = []
                for mention in mentions:
                    binomeWithMention = extractBinomesWithEleveAndMention(matrice,eleve,mention)
                    binomeEleve.append(binomeWithMention)
                dataEleve.append(binomeEleve)
                dataEleves.append(dataEleve)

            seuil = -1

            binomes = []
            trinomes = []
            repartitionTotalBinomes = []

            while seuil != 10 and not(repartTrouvee):
                seuil = seuil + 1

                print "Le seuil est a : ",seuil

                if len(repartitionTotalBinomes) == 0:
                    if len(binomes) == 0:
                        for x in range(0,nbEleve):
                            for binome in dataEleves[x][1][seuil]:
                                if sorted(binome,reverse=True) not in binomes:
                                    binomes.append(sorted(binome,reverse=True))
                            listOccurencesElevesBinomes[x] = listOccurencesElevesBinomes[x] + len(dataEleves[x][1][seuil])
                    else:
                        for eleveCrit in listeElevesCritiques:
                            for binome in dataEleves[eleveCrit][1][seuil]:
                                if sorted(binome,reverse=True) not in binomes:
                                    binomes.append(sorted(binome,reverse=True))
                            listOccurencesElevesBinomes[eleveCrit] = listOccurencesElevesBinomes[eleveCrit] + len(dataEleves[eleveCrit][1][seuil])
                else:
                    binomes = []
                    for y in range(0,seuil):
                        for x in range(0,nbEleve):
                            for binome in dataEleves[x][1][y]:
                                if sorted(binome,reverse=True) not in binomes:
                                    binomes.append(sorted(binome,reverse=True))
                            listOccurencesElevesBinomes[x] = listOccurencesElevesBinomes[x] + len(dataEleves[x][1][y])

                print binomes
                print len(binomes), " binomes gardés ! "
                print "Occurrences des élèves dans binomes : ",listOccurencesElevesBinomes

                trinomes = getAvailableTrinomes(binomes,listOccurencesElevesTrinomes)

                print len(trinomes), " trinomes gardés ! "
                print trinomes
                print "Occurrences des élèves dans trinomes : ",listOccurencesElevesTrinomes
                if len(repartitionTotalBinomes) == 0:
                    listeElevesCritiques = [i for i, x in enumerate(listOccurencesElevesTrinomes) if x == 0]

                    print "Liste des élève(s) critique(s) : ", listeElevesCritiques

                    binomesCritiques = []

                    for elevesCrit in listeElevesCritiques:
                        for binome in dataEleves[elevesCrit][1][seuil]:
                            add = True
                            for binomeCritique in binomesCritiques:
                                if sorted(binome) == sorted(binomeCritique):
                                    add = False
                            if add:
                                binomesCritiques.append(binome)

                    print "Liste des binome(s) critique(s) : ", binomesCritiques

                    repartitionCritiques = []

                    combinaison(len(listeElevesCritiques),binomesCritiques,[0,len(binomesCritiques)-len(listeElevesCritiques)],[],0,repartitionCritiques)

                    if len(repartitionCritiques) != 0:
                        for repartitionCritique in repartitionCritiques:
                            print repartitionCritique

                        repartitionBinomesNonCrit = []

                        t = []

                        validBinomes = deleteElevesFromGroups(binomes,binomesCritiques)
                        nbBinomesRestantNeeded = nbBinomesNeeded - len(listeElevesCritiques)
                        if validBinomes >= nbBinomesNeeded:
                            # On va tester toutes les combinaisons possibles avec chaque binome critique.
                            for x in range(0,(len(validBinomes)-nbBinomesRestantNeeded+1)):
                                nbThread = nbThread + 1

                                tmp = combinaisonT2(nbBinomesNeeded*2,nbThread-1,nbBinomesRestantNeeded,validBinomes,[x,x],[],0,repartitionBinomesNonCrit)

                                t.append(tmp)
                                tmp.start()

                        for value in t:
                            value.join()

                        if len(repartitionBinomesNonCrit) > 0:
                            for repartNonCrit in repartitionBinomesNonCrit:
                                for repartitionCritique in repartitionCritiques:
                                    print repartNonCrit,repartitionCritique, isRepartition(repartNonCrit+repartitionCritique,nbBinomesNeeded*2)
                                    if isRepartition(repartNonCrit+repartitionCritique,nbBinomesNeeded*2):
                                        repartitionTotalBinomes.append(repartNonCrit+repartitionCritique)

                if len(repartitionTotalBinomes) != 0:
                    print "\n%d repartition trouvee pour les binomes !"% (len(repartitionTotalBinomes))
                    #On regarde les repartition de trinomes qui marche avec les repartition de binomes
                    for idx,repartitionTotalBinome in enumerate(repartitionTotalBinomes):
                        validBinomes = deleteElevesFromGroups(trinomes,repartitionTotalBinome)
                        if len(validBinomes) >= nbTrinomeNeeded and canHaveRepartition(validBinomes+repartitionTotalBinome,nbEleve):
                            toPrint = "Checking for : %s -> %d/%d\n" %(repartitionTotalBinome,idx,len(repartitionTotalBinomes)-1)
                            Printer(toPrint)
                            repartition = []
                            #combinaison(nbBinomesRestantNeeded,validBinomes,[0,len(validBinomes)-nbBinomesRestantNeeded],[],0,repartitionBinomesNonCrit)

                            t = []

                            for x in range(0,(len(validBinomes)-nbTrinomeNeeded)):
                                nbThread = nbThread + 1

                                tmp = combinaisonT2(nbTrinomeNeeded*2,nbThread-1,nbTrinomeNeeded,validBinomes,[x,x],[],0,repartition)

                                t.append(tmp)
                                tmp.start()

                            for value in t:
                                value.join()


                            if len(repartition) > 0:
                                for repart in repartition:
                                    if isRepartition(repart+repartitionTotalBinome,nbEleve):
                                        repartitionTotal.append(repart+repartitionTotalBinome)
                                        repartTrouvee = True

                    else:
                        print "Pas de repartition non-critique !"


    else:
        print "Il manque un élève !"
    if len(repartitionTotal) != 0:
        for repartition in repartitionTotal:
            if not(isRepartition(repartition,nbEleve)):
                repartitionTotal.remove(repartition)
        if len(repartitionTotal) != 0:
            repartTrouvee = True
            print "\n________________________________________________"
            print "\n%d répartitions ont été trouvées ! " % len(repartitionTotal)

    level += 1
    if level == len(mentionsClassee):
        end = True
    if not(repartTrouvee):
        print "\nPas de Répartition trouvée !"
    else:
        end = True

    # end while (répart trouvée)
print("------------------------------------------------")

if(repartTrouvee):
    # On cherche désormais la meilleure répartition parmi celles possibles
    # Méthode : assigner une valeur à chaque mentionsClassees et les additionner

    meilleuresRepartsParPoints = []
    meilleuresRepartsParPoints = compR.meilleuresRepartsParPoints(repartitionTotal, matrice)

    print("\nLa / les meilleure(s) répartition(s) (avec %d points) est / sont :" % compR.pointsRepart(meilleuresRepartsParPoints[0], matrice))
    i = 1
    for repart in meilleuresRepartsParPoints:
        printEcranAndCSV(repart,i)
        i += 1


    # La méthode suivante est très longue : elle compare toutes les répartitions 2 à 2 pour savoir
    # laquelle en bat le plus.
'''
    meilleuresRepartsParComp = []
    meilleuresRepartsParComp = compR.meilleuresRepartsParComp(repartitionTotal, matrice)

    print("\nLa / les meilleure(s) répartition(s) par comparaison est / sont :")
    for repart in meilleuresRepartsParComp:
        printEcranAndCSV(repart)
'''
