# import csv
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import WordNetError
from math import log
# import numpy as np


def sim_wu_palmer(sense1, sense2):
    lcs = lowest_common_subsumer(sense1, sense2)
    if not lcs and sense1.pos() == 'v':
        return (2 * 1) / (depth(sense1) + depth(sense2) + 2)
    if not lcs:
        return None
    return (2 * depth(lcs)) / (depth(sense1) + depth(sense2))


def bck_lowest_common_subsumer(sense1, sense2):
    ancestors = extract_ancestors([sense1])
    ancestors.append(sense1)
    print('anc1: ', ancestors)
    ancestors2 = extract_ancestors([sense2])
    ancestors2.append(sense2)
    print('anc2: ', ancestors2)
    res = list(set(ancestors).intersection(ancestors2))
    print("res: ", res)
    if len(res) == 0:
        return None
    '''
    if sense1.lowest_common_hypernyms(sense2)[0] != ancestors[max([ancestors.index(i) for i in res])]:
        print("\n\n--------------- ERROR: lowest_common_subsumer is not the right one")
        print("right: ", sense1.lowest_common_hypernyms(sense2))
        print("mine : ", ancestors[max([ancestors.index(i) for i in res])])
        input("Press Enter to continue...")
    '''
    return ancestors[max([ancestors.index(i) for i in res])]


def bck2_lowest_common_subsumer(sense1, sense2):
    ancestors1 = get_all_ancestors(sense1)
    print('anc1: ', ancestors1)
    ancestors2 = get_all_ancestors(sense2)
    print('anc2: ', ancestors2)
    inters = [a for a in ancestors1.keys() if a in ancestors2.keys()]
    print("inters: ", inters)
    if len(inters) == 0:
        return None
    max = 0
    lcs = None
    for s in inters:
        path_len = 0
        k = [s]
        while str(k) != '':
            k = ancestors1[k[0]]
            path_len += 1
        if path_len > max:
            lcs = s
            max = path_len
    return lcs


def lowest_common_subsumer(sense1, sense2):
    ancestors1 = get_all_ancestors(sense1)
    # print('anc1: ', ancestors1)
    ancestors2 = get_all_ancestors(sense2)
    # print('anc2: ', ancestors2)
    inters = [a for a in ancestors1.keys() if a in ancestors2.keys()]
    # print("inters: ", inters)
    if len(inters) == 0:
        return None
    max = 0
    lcs = None
    for s in inters:
        path = get_path(s, search_max=True)
        path_len = len(path)
        if path_len > max:
            lcs = s
            max = path_len
    return lcs


def extract_ancestors(sense: list):
    ancestors = []
    while sense[0].hypernyms():
        # print("hyp: ", sense[0].hypernyms())
        ancestors.insert(0, sense[0].hypernyms()[0])
        sense = sense[0].hypernyms()
    return ancestors


def get_all_ancestors(s1):
    path = {}
    if not s1.hypernyms():
        path[s1] = ""
        return path
    path[s1] = s1.hypernyms()
    for s in s1.hypernyms():
        path.update(get_all_ancestors(s))
    return path


# trova il percorso minimo fra il nodo e la radice
def get_path(s1, search_max: bool = False):
    path = [s1]
    if not s1.hypernyms():
        return path
    count = 0
    ancestors = []
    for s in s1.hypernyms():
        tmp = get_path(s, search_max)
        if search_max:
            if len(tmp) > count or count == 0:
                count = len(tmp)
                ancestors = tmp
        else:
            if len(tmp) < count or count == 0:
                count = len(tmp)
                ancestors = tmp
    path += ancestors
    return path


def depth(sense):
    depth = 1
    while sense is not None and sense.hypernyms():
        depth += 1
        sense = sense.hypernyms()[0]
    return depth


# versione funzionante ma non sono mai verificate le condizioni a 92 e 95
# non usata
def find_short_path(s1, s2):
    path = [s1]
    hyponyms = s1.hyponyms()
    # print("hyponyms: ", hyponyms)
    if not hyponyms:
        # print("No hyponyms")
        return None
    if s2 in hyponyms:
        # print("Found")
        # path.append(s2)
        path += [s2]
        return path
    min_path = None
    for i in range(len(hyponyms)):
        ###################
        new_path = find_short_path(hyponyms[i], s2)
        # print("min path: ", min_path)
        # print("new path: ", new_path)
        try:
            if len(new_path) < len(min_path):
                min_path = new_path
            elif min_path is None and new_path:
                min_path = new_path
        except TypeError:
            pass
    try:
        path += min_path
    except TypeError:
        pass
    # print("path: ", path)
    if s2 not in path:
        return None
    return path


def find_path(s1, s2):
    path = []
    if s2 in s1:
        return path
    while s1[0].hypernyms() and s2:
        if s2 in s1[0].hypernyms():
            # path.insert(0, s2)
            path.append(s2)
            break
        # path.insert(0, s1[0].hypernyms()[0])
        path.append(s1[0].hypernyms()[0])
        s1 = s1[0].hypernyms()
    # print(path)
    # todo se s2 non viene trovato (risolgo fino ad "entity" ma non c'è) allora dovrei tornare None o [], questo non può accadere se s2==lcs
    return path


def sim_shortest_path(s1, s2):
    path_len = 0
    if s1.pos() == 'v':
        p1 = extract_ancestors([s1])
        # p1.append(syn1[i])
        p2 = extract_ancestors([s2])
        p2.append(s2)
        # print("p1: ", p1)
        # print("p2: ", p2)
        path = p1 + p2
        path_len = len(path) + 1
    lcs = lowest_common_subsumer(s1, s2)
    # print("lcs: ", lcs)
    if lcs:
        p1 = find_path([s1], lcs)
        p2 = find_path([s2], lcs)
        p2.insert(0, s2)
        p2.reverse()
        p2.remove(lcs)
        path = p1 + p2
        path_len = len(path)
    if path_len == 0:
        return None
    # return (2 * max_depth - path_len) / (2 * max_depth)
    return 1 / (1 + path_len)  # con questa formula esce lo stesso risultato della libreria


def sim_leakcock_chodorow(s1, s2):
    if s1.pos() != s2.pos():
        return None
    path = []
    lcs = lowest_common_subsumer(s1, s2)
    if lcs:
        p1 = find_path([s1], lcs)
        p2 = find_path([s2], lcs)
        p2.insert(0, s2)
        p2.reverse()
        p2.remove(lcs)
        path = p1 + p2
    # print("path: ", path)
    # return - log((1 + len(path)) / (1 + 2 * max_depth))
    if lcs is None and s1.pos() == 'v':
        p1 = extract_ancestors([s1])
        # p1.append(syn1[i])
        p2 = extract_ancestors([s2])
        p2.append(s2)
        # print("p1: ", p1)
        # print("p2: ", p2)
        path = p1 + p2
        return - log((1 + len(path) + 1) / (2 * (max_depth_v + 1)))
    if s1.pos() == 'v':
        return - log((1 + len(path)) / (2 * max_depth_v))
    return - log((1 + len(path)) / (2 * max_depth))  # con questa formula esce lo stesso risultato della libreria
    # return - log((1 + len(path)) / (1 + 2 * comp_max_depth(s1)))


def comp_max_depth(pos):
    depth = 0
    for ii in wn.all_synsets(pos):
        try:
            depth = max(depth, ii.max_depth())
        except RuntimeError:
            print(ii)
    return depth


def pearson_index():
    # np.cov()
    print("ancora da implementare")


# -----------------------------------
# -------------- TESTS --------------
# -----------------------------------

def check_depth(syn):
    for i in range(len(syn)):
        s1hp = syn[i]._shortest_hypernym_paths(True)
        real_depth = s1hp.get(list(s1hp)[len(s1hp) - 1])
        my_depth = depth(syn[i])
        # my_depth = get_path(syn[i])
        if real_depth != my_depth:
            print(syn[i])
            print("my_depth  : ", my_depth)
            print("real_depth: ", real_depth)
            input("ERROR: Press Enter to continue...")
    print("------ ok, depth")


def check_shortest_path(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            # print("\nc1[" + str(i) + "]: " + str(syn1[i]))
            # print("c2[" + str(j) + "]: " + str(syn2[j]))
            lcs = lowest_common_subsumer(syn1[i], syn2[j])
            if lcs:
                p1 = find_path([syn1[i]], lcs)
                p2 = find_path([syn2[j]], lcs)
                # p1.remove(syn1[i])
                p2.insert(0, syn2[j])
                p2.reverse()
                p2.remove(lcs)
                my_path = p1 + p2
                real_path = syn1[i].shortest_path_distance(syn2[j], simulate_root=True and syn1[i].pos() == 'v')
                if len(my_path) != real_path:
                    print("my_path len  : ", my_path)
                    print("real path len: ", real_path)
                    input("ERROR: Press Enter to continue...")
            else:
                p1 = extract_ancestors([syn1[i]])
                # p1.append(syn1[i])
                p2 = extract_ancestors([syn2[j]])
                p2.append(syn2[j])
                # print("p1: ", p1)
                # print("p2: ", p2)
                my_path = p1 + p2
                real_path = syn1[i].shortest_path_distance(syn2[j], simulate_root=True and syn1[i].pos() == 'v')
                if real_path and (len(my_path) + 1) != real_path:
                    print("lcs is None  : ", lcs)
                    print("path: ", my_path)
                    print("my_path len  : ", len(my_path))
                    print("real path len: ", real_path)
                    input("ERROR: Press Enter to continue...")
    print("------ ok, shortest_path")


def check_lowest_common_subsumer(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_lcs = lowest_common_subsumer(syn1[i], syn2[j])
            right_lcs = syn1[i].lowest_common_hypernyms(syn2[j])
            # print("my_lcs  : ", my_lcs)
            # print("real lcs: ", right_lcs)
            # if (my_lcs is [] and right_lcs) or (my_lcs not in right_lcs):
            if my_lcs and right_lcs and my_lcs not in right_lcs:
                print("\nc1[" + str(i) + "]: " + str(syn1[i]))
                print("c2[" + str(j) + "]: " + str(syn2[j]))
                print("my_lcs  : ", my_lcs)
                print("real lcs: ", right_lcs)
                input("ERROR: Press Enter to continue...")
            break
    print("------ ok, lowest_common_subsumer")


def list_replace(lst, old, new):
    i = -1
    try:
        while 1:
            i = lst.index(old, i + 1)
            lst[i] = new
    except ValueError:
        pass


def check_sim_wu_palmer(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_sim = sim_wu_palmer(syn1[i], syn2[j])
            right_sim = syn1[i].wup_similarity(syn2[j])
            if my_sim != right_sim:
                print("\nc1[" + str(i) + "]: " + str(syn1[i]))
                print("c2[" + str(j) + "]: " + str(syn2[j]))
                print("My sim_wu_palmer:    ", my_sim)
                print("Right sim_wu_palmer: ", right_sim)
                input("ERROR: Press Enter to continue...")
                # break
        # break
    print("------ ok, sim_wu_palmer")



def check_sim_shortest_path(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            right_sim = syn1[i].path_similarity(syn2[j])
            my_sim = sim_shortest_path(syn1[i], syn2[j])
            if right_sim != my_sim:
                print("\nc1[" + str(i) + "]: ", syn1[i])
                print("c2[" + str(j) + "]: ", syn2[j])
                print("Mine : ", my_sim)
                print("Right: ", right_sim)
                input("ERROR: Press Enter to continue...")
            # print("right path 1: ", syn1[i]._shortest_hypernym_paths(False))
            # print("right path 2: ", syn2[j]._shortest_hypernym_paths(False))
    print("------ ok, sim_shortest_path")


def check_leakcock_chodorow(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_sim = sim_leakcock_chodorow(syn1[i], syn2[j])
            try:
                right_sim = syn1[i].lch_similarity(syn2[j])
                if right_sim != my_sim:
                    print("\nc1[" + str(i) + "]: ", syn1[i])
                    print("c2[" + str(j) + "]: ", syn2[j])
                    print("Right: ", right_sim)
                    print("Mine : ", my_sim)
                    input("ERROR: Press Enter to continue...")
            except Exception:
                # print("\nc1[" + str(i) + "]: ", syn1[i])
                # print("c2[" + str(j) + "]: ", syn2[j])
                # print("right sim error")
                pass
    print("------ ok, sim_leakcock_chodorow")


#  Word 1 | Word 2 | Human (mean)
# --------|--------|--------------
#  love   |  sex   | 6.77
#  tiger  |  cat   | 7.35


# max_depth = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets('n'))
# max_depth_v = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets('v'))

max_depth = comp_max_depth('n')
# print("max_depth  : ", max_depth)
max_depth_v = comp_max_depth('v')
# print("max_depth_v: ", max_depth_v)


# w1 = 'love'
# w2 = 'sex'
w1 = 'tiger'
w2 = 'cat'
syn1 = wn.synsets(w1)
syn2 = wn.synsets(w2)
# s1 = syn1[0]
# s2 = syn2[0]




# check_depth(syn1)  # todo qui errore depth a Synset('beloved.n.01')
# check_depth(syn2)
# check_lowest_common_subsumer(syn1, syn2)
# check_shortest_path(syn1, syn2)
# check_sim_wu_palmer(syn1, syn2)
# check_leakcock_chodorow(syn1, syn2)
# check_sim_shortest_path(syn1, syn2) # da errore ma sim_shortest_path() funziona
# input("STOP HERE")

s1 = []
s2 = []
my_sim_wp = []
right_sim_wp = []
my_sim_sp = []
right_sim_sp = []
my_sim_lc = []
right_sim_lc = []
for i in range(len(syn1)):
    for j in range(len(syn2)):
        # print("\nc1[" + str(i) + "]: ", syn1[i])
        # print("c2[" + str(j) + "]: ", syn2[j])

        s1.append(syn1[i])
        s2.append(syn2[j])

        my_sim_wp.append(sim_wu_palmer(syn1[i], syn2[j]))
        right_sim_wp.append(syn1[i].wup_similarity(syn2[j]))

        my_sim_sp.append(sim_shortest_path(syn1[i], syn2[j]))
        right_sim_sp.append(syn1[i].path_similarity(syn2[j]))

        my_sim_lc.append(sim_leakcock_chodorow(syn1[i], syn2[j]))
        try:
            right_sim_lc.append(syn1[i].lch_similarity(syn2[j]))
        except WordNetError:
            right_sim_lc.append(None)

sim_df = pd.DataFrame({
    "synset 1": s1,
    "synset 2": s2,
    "my_sim_wp": my_sim_wp,
    "right_sim_wp": right_sim_wp,
    "my_sim_sp": my_sim_sp,
    "right_sim_sp": right_sim_sp,
    "my_sim_lc": my_sim_lc,
    "right_sim_lc": right_sim_lc
})

print(sim_df.to_string())
# trova i massimi per ogni colonna
print("\n--- massimi per ogni colonna ---\n")
print(sim_df[sim_df.columns.difference(['synset 1', 'synset 2'])].max(axis='rows'))
# trova gli indici di riga dei massimi per ogni colonna
indexes = sim_df[sim_df.columns.difference(['synset 1', 'synset 2'])].idxmax(axis='rows')
# print("\nindexes\n", indexes)
# stampa riga di ogni massimo per ogni colonna
print("\n--- riga di ogni massimo ---\n")
print(sim_df.loc[indexes].to_string())

max_df = pd.DataFrame(index=['my_sim_wp', 'right_sim_wp', 'my_sim_lc', 'right_sim_lc', 'my_sim_sp', 'right_sim_sp'],
                      columns=['synset 1', 'synset 2', 'sim'])

for i, v in indexes.items():
    max_df.loc[i, 'synset 1'] = sim_df.loc[v, 'synset 1']
    max_df.loc[i, 'synset 2'] = sim_df.loc[v, 'synset 2']
    max_df.loc[i, 'sim'] = sim_df.loc[v, i]
print(max_df.to_string())

# read the file
# dataset = pd.read_csv('WordSim353.csv', header=0)
# print(dataset.to_string())
