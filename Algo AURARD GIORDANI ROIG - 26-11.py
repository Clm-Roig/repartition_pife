#!/usr/bin/env python
# coding: utf-8

import numpy as np
import time as time
import random as random
from threading import Thread
import collections
import sys
import csv

global repartition
global tFini
global nbThread

nbThread = 0
tFini = 0
stopPrinter = False
repartition = []


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
    Renvoie une liste:
        Premier argument = matrice de preferences
        Second argument = liste des eleves
'''
def parseCSV(file):
    tmp = []
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            tmp.append(','.join(row).split(','))
    matrice = np.array(tmp)
    return matrice[1:matrice.shape[0],1:matrice.shape[0]],matrice[0][1:matrice.shape[0]]

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
    (Les chiffres representent les eleves)
'''
def writeCsv(file,repartition):
    with open(file, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for x in xrange(0,len(repartition)):
            repartition[x].insert(0,x+1)
            spamwriter.writerow(repartition[x])


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
        toPrint = "Thread %d Fini NbThread fini : %d/%d" % (self.id, tFini,nbThread)
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

def checkRepartition(repartition, nbEleve):
    tmp = []
    for group in repartition:
        for eleve in group:
            if eleve not in tmp:
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
              tmp = createTrinome(binomes[i],binomes[j],binomes[z])
              if len(tmp) != 0:
                  res.append(tmp)
                  nbOccurences[tmp[0]] += 1
                  nbOccurences[tmp[1]] += 1
                  nbOccurences[tmp[2]] += 1
    return res

def combinaison(k,group,ranges,repartition,i,result):
    for x in range(ranges[0],ranges[1]+1):
        temp = sontBloquants(repartition,group[x])
        if not(temp):
            repartition.append(group[x])
            if i == k - 1:
                result.append(list(repartition))
            else:
                combinaison(k,group,[x+1 , i+1 + len(group) - k],repartition,i+1,result)
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

def combinaisonBis(nbEleves,k,group,ranges,repartition,i,trinomes,result):
    for x in range(ranges[0],ranges[1]+1):
        if not(sontBloquants(repartition,group[x])):
            repartition.append(group[x])
            if i == k - 1:
                for t in trinomes:
                    if checkRepartition((t+repartition),nbEleves):
                        #print "Repartition trouvé !"
                        result.append(repartition + t)
            else:
                combinaisonBis(nbEleves,k,group,[x+1 , i+1 + len(group) - k],repartition,i+1,trinomes,result)
            if len(repartition) != 0:
                repartition.pop()
    return True

def extractGroupWith(group,eleve):
    res = []
    for value in group:
        for x in value:
            if x == eleve:
                res.append(value)
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

listeEleves = []
try:
    res = parseCSV(sys.argv[1])
    matrice = res[0]
    listeEleves = res[1]
    nbEleve = len(listeEleves)
    matrice = convertToInt(matrice)
except IndexError:
    print "Nombre d'eleves : "
    nbEleve = input()
    matrice = matriceAleatoire(nbEleve)
    for x in range(0,nbEleve):
        listeEleves.append(x)

listOccurencesElevesBinomes = [0]*nbEleve
listOccurencesElevesTrinomes = [0]*nbEleve

nbBinomesNeeded = 0
nbTrinomeNeeded = 0

if nbEleve > 35:
    nbTrinomeNeeded = nbEleve - 36
    nbBinomesNeeded = 54 - nbEleve
else:
    if not(nbEleve % 2 == 0):
        nbTrinomeNeeded = 1
    nbBinomesNeeded = (nbEleve - 3) / 2

tFini = 0
binomes = []
trinomes = []
repartitionTotal = []

mentionsClassee = [[5,5],[5,4],[4,4],[5,3],[4,3],[3,3],[5,2]]
level = 0
end = False
repartTrouvee = False

print 'Matrice des préférences :'
for i in range(nbEleve):
    for j in range(nbEleve):
        print int(matrice[i][j]),
        if(matrice[i][j] == -1):
            print ' ',
        else:
            print '  ',
    print

while not(end) and not(repartTrouvee):

    ajoutBinome(mentionsClassee[level][0],mentionsClassee[level][1],matrice,binomes,listOccurencesElevesBinomes)

    print "________________________________________________\n"
    print "Seuil de mentions courant : ", level
    print "Nombre de binomes recherché : ",nbBinomesNeeded
    print "Nombre de trinomes recherché : ",nbTrinomeNeeded,"\n"
    print "Nombre de binomes retenu : ",len(binomes)

    if checkRepartition(binomes,nbEleve):
        #print sortListGroupByOccEleves(binomes,listOccurencesElevesBinomes,nbEleve)
        #print "____________________"
        #print sortListGroupByOccEleves(trinomes,listOccurencesElevesTrinomes,nbEleve)
        if nbTrinomeNeeded == 0:
            print "NB d'occurences de chaque eleve dans les binomes retenus : ", listOccurencesElevesBinomes
            repartitionTrinomes = []

            temps = time.time()
            #combinaisonBis(nbBinomesNeeded,binomes,[0,len(binomes) - nbBinomesNeeded],[],0,repartitionTrinomes,repartitionTotal)
            t = []
            for x in range(0,(len(binomes)-nbBinomesNeeded+1)):
                for y in range(x+1,(len(binomes)-nbBinomesNeeded+2)):
                    nbThread = nbThread + 1
                    tmp = combinaisonT(nbEleve,nbThread-1,nbBinomesNeeded,binomes,[y,y],[binomes[x]],1,repartitionTrinomes,repartitionTotal)
                    t.append(tmp)
                    tmp.start()

            for value in t:
                value.join()

            temps = time.time() - temps

            #print "\n",len(repartitionTotal)," répartition trouvé pour les trinomes et binomes en : ",temps
            toPrint = "%d répartition(s) trouvée(s) pour les binomes en : %fs\n" % (len(repartitionTotal),temps)
            Printer(toPrint)
            if len(repartitionTotal) > 0:
                repartTrouvee = True


        else:
            trinomes = getAvailableTrinomes(binomes,listOccurencesElevesTrinomes)

            if len(trinomes) >= nbTrinomeNeeded:
                print "Nombre de trinomes retenu : ",len(trinomes)

                print "Nb d'occurrences de chaque eleve dans binomes : ", listOccurencesElevesBinomes
                print "Nb d'occurrences de chaque eleve dans trinomes : ", listOccurencesElevesTrinomes

                combiTri = combin(len(trinomes),nbTrinomeNeeded)
                combiBin = combin(len(binomes),nbBinomesNeeded)
                print "Combinaison de trinomes : " , combiTri
                print "Combinaison de binomes : " , combiBin
                if combiTri <= combiBin:
                    print "Nb de combinaison de trinomes inferieur au nb requis."
                    repartitionTrinomes = []
                    temps = time.time()
                    combinaison(nbTrinomeNeeded,trinomes,[0,len(trinomes) - nbTrinomeNeeded],[],0,repartitionTrinomes)
                    temps = time.time() - temps

                    print "\n",len(repartitionTrinomes),"répartition(s) trouvée(s) pour les trinomes en : ",temps

                    if len(repartitionTrinomes) > 0:
                        repartitionTotal = []
                        temps = time.time()
                        #combinaisonBis(nbBinomesNeeded,binomes,[0,len(binomes) - nbBinomesNeeded],[],0,repartitionTrinomes,repartitionTotal)
                        t = []
                        for x in range(0,(len(binomes)-nbBinomesNeeded+1)):
                            for y in range(x+1,(len(binomes)-nbBinomesNeeded+2)):
                                nbThread = nbThread + 1
                                tmp = combinaisonT(nbEleve,nbThread-1,nbBinomesNeeded,binomes,[y,y],[binomes[x]],1,repartitionTrinomes,repartitionTotal)
                                t.append(tmp)
                                tmp.start()

                        for value in t:
                            value.join()

                        temps = time.time() - temps

                        #print "\n",len(repartitionTotal)," répartition trouvé pour les trinomes et binomes en : ",temps
                        toPrint = "%d répartition(s) trouvées(s) pour les trinomes et binomes en : %fs\n" % (len(repartitionTotal),temps)
                        Printer(toPrint)
                        if len(repartitionTotal) > 0:
                            repartTrouvee = True
                    else:
                        print "Aucune répartition de trinomes trouvée !"
                else:
                    print "Nb de combinaisons de binome inferieur au nb requis."
                    repartitionBinomes = []
                    temps = time.time()
                    combinaison(nbBinomesNeeded,binomes,[0,len(binomes) - nbBinomesNeeded],[],0,repartitionBinomes)
                    temps = time.time() - temps

                    print "\n",len(repartitionBinomes)," répartition(s) trouvée(s) pour les binomes en : ",temps,'s'

                    if len(repartitionBinomes) > 0:
                        repartitionTotal = []
                        temps = time.time()
                        #combinaisonBis(nbBinomesNeeded,binomes,[0,len(binomes) - nbBinomesNeeded],[],0,repartitionTrinomes,repartitionTotal)
                        t = []
                        for x in range(0,(len(trinomes)-nbTrinomeNeeded+1)):
                            for y in range(x+1,(len(trinomes)-nbTrinomeNeeded+2)):
                                nbThread = nbThread + 1
                                tmp = combinaisonT(nbEleve,nbThread-1,nbTrinomeNeeded,trinomes,[y,y],[trinomes[x]],1,repartitionBinomes,repartitionTotal)
                                t.append(tmp)
                                tmp.start()

                        for value in t:
                            value.join()

                        temps = time.time() - temps

                        #print "\n",len(repartitionTotal)," répartition trouvé pour les trinomes et binomes en : ",temps
                        toPrint = "%d répartitions trouvées pour les trinomes et binomes en : %fs\n" % (len(repartitionTotal),temps)
                        Printer(toPrint)
                        if len(repartitionTotal) > 0:
                            repartTrouvee = True

                    else:
                        print "Aucune repartition de trinomes trouvée !"
            else:
                print "Pas assez de trinomes retenus."
    else:
        print "Il manque un élève !"
    level += 1
    if level == len(mentionsClassee):
        end = True
    if not(repartTrouvee):
        print "Pas de repartition trouvée !"

    # end while

if(repartTrouvee):
    # On cherche désormais la meilleure répartition parmi celles possibles
    # Méthode : assigner une valeur à chaque mentionsClassee et les additionner
    meilleuresReparts = []
    valeurMeilleureRepart = 0
    for repart in repartitionTotal:
        valeurRepart = 0
        for groupe in repart:
            # Binome
            if(len(groupe) == 2):
                valeurRepart = matrice[groupe[0]][groupe[1]] + matrice[groupe[1]][groupe[0]]
            # Trinome
            else:
                valeurRepart = matrice[groupe[0]][groupe[1]] + matrice[groupe[1]][groupe[0]]
                valeurRepart += matrice[groupe[0]][groupe[2]] + matrice[groupe[2]][groupe[0]]
                valeurRepart += matrice[groupe[1]][groupe[2]] + matrice[groupe[2]][groupe[1]]

        print repart,
        print "= %d points" %valeurRepart

        if valeurRepart > valeurMeilleureRepart:
            valeurMeilleureRepart = valeurRepart
            meilleuresReparts = []
            meilleuresReparts.append(repart)
        elif valeurRepart == valeurMeilleureRepart:
            meilleuresReparts.append(repart)

    print("------------------------------------------------")
    print("La / les meilleure(s) répartition(s) (avec %d points) est / sont :" % valeurMeilleureRepart)
    for repart in meilleuresReparts:
        print repart