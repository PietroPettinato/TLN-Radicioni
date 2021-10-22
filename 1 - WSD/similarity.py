import csv
#import numpy as np
from nltk.corpus import wordnet as wn


def findMaxSimilarity(syn1, syn2):
    simWup = 0
    simLch = 0
    simPth = 0
    sense = [0, 0, 0, 0, 0, 0]
    for s1 in syn1:
        for s2 in syn2:
            newSimWup = s1.wup_similarity(s2)
            newSimPth = s1.path_similarity(s2)
            if s1.pos() == s2.pos(): # ci sono problemi se gli passo due termini con PoS diverso, gli altri due ritornano None, questo lancia un'eccezione (o la catturo o uso l'if)
                newSimLch = s1.lch_similarity(s2)
            #print(f's1 = {s1}')
            #print(f's2 = {s2}')
            #print(f'newSimWup = {newSimWup}, newSimLch = {newSimLch}, newSimPth = {newSimPth}')
            if (newSimWup != None and simWup < newSimWup):
                simWup = newSimWup
                sense[0] = s1
                sense[1] = s2
            if (newSimLch != None and simLch < newSimLch):
                simLch = newSimLch
                sense[2] = s1
                sense[3] = s2
            if (newSimPth != None and simPth < newSimPth):
                simPth = newSimPth
                sense[4] = s1
                sense[5] = s2
    return sense


#    print(f'WUP_similarity({s1},{s2}): {s1.wup_similarity(s2)}\n')
#    print(f'LCH_similarity({s1},{s2}): {s1.lch_similarity(s2)}\n')
#    print(f'PTH_similarity({s1},{s2}): {s1.path_similarity(s2)}\n')

# with open('WordSim353.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         #print(f'\t{row[0]} | {row[1]} | {row[2]}.')
#         else:
#             s1 = wn.synsets(row[0])[0]
#             s2 = wn.synsets(row[1])[0]
#             print(f'{row[0]} | {s1}')
#             print(f'{row[1]} | {s2}')
#
#             # ecco alcune misure di similarità
#             print(f'WUP_similarity({s1},{s2}): {s1.wup_similarity(s2)}\n')
#             print(f'LCH_similarity({s1},{s2}): {s1.lch_similarity(s2)}\n')
#             print(f'PTH_similarity({s1},{s2}): {s1.path_similarity(s2)}\n')
#             print("\n-----------------------------------------------------------------------------------\n")
#         line_count += 1
#     print(f'Processed {line_count} lines.')


# Word 1 | Word 2 | Human (mean)
#  love  |  sex   | 6.77


s1 = 'love'
s2 = 'sex'

print(wn.synsets(s1))
print(wn.synsets(s1)[0])
print(wn.synsets(s2))
print(wn.synsets(s2)[0])
print("\n---------------------------------------\n")

syn = findMaxSimilarity(wn.synsets(s1), wn.synsets(s2))
print(f'\nsyn = {syn}')
print(f'\nWUP_similarity({syn[0]},{syn[1]}): {syn[0].wup_similarity(syn[1])}')
print(f'\nLCH_similarity({syn[2]},{syn[3]}): {syn[2].lch_similarity(syn[3])}')
print(f'\nPTH_similarity({syn[4]},{syn[5]}): {syn[4].path_similarity(syn[5])}')


# per ogni elemento del synset1 devo calcolare la similarità con tutti gli altri elementi del synset2
# FATTO cercare come creare funzioni in python ed operare li solo per due termini
# cercare modo efficiente per evitare cicli for annidati

# organizzare i valori in un vettore X: prendo il max della similarità di ogni coppia di termini e metto ogni max in X (X è un vettore con i valori massimi dei termini)
# X = array con valori della similarità
# Y = array con valori target dal file
# NumPy installata, usare la funzione numpy.cov(X,Y)