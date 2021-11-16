import pandas as pd
import math
from nltk.corpus import wordnet as wn
from math import log
from math import isnan


def bck_sim_wu_palmer(sense1, sense2):
    lcs = lowest_common_subsumer(sense1, sense2)
    if not lcs and sense1.pos() == 'v':
        return (2 * 1) / (bck_depth(sense1) + bck_depth(sense2) + 2)
    if not lcs:
        return None
    return (2 * bck_depth(lcs)) / (bck_depth(sense1) + bck_depth(sense2))


def sim_wu_palmer(sense1, sense2):
    lcs = lowest_common_subsumer(sense1, sense2)
    if not lcs and sense1.pos() == 'v':
        # print('NO lcs, verbo _______________________')
        return (2 * 1) / (depth(sense1) + depth(sense2) + 2)
    if not lcs:
        return None
    path_lcs = get_path_to_root(lcs, search_max=True)
    # print('LCS: ', path_lcs)
    depthLCS = len(path_lcs)
    path_s1 = get_path_to_root(sense1)
    # print(path_s1)
    depth1 = len(path_s1)
    path_s2 = get_path_to_root(sense2)
    # print(path_s2)
    depth2 = len(path_s2)

    # print('SI lcs _________________________')
    return (2 * depthLCS) / (depth1 + depth2)


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
        path = get_path_to_root(s, search_max=True)
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
def get_path_to_root(s1, search_max: bool = False):
    path = [s1]
    if not s1.hypernyms():
        return path
    count = 0
    ancestors = []
    for s in s1.hypernyms():
        tmp = get_path_to_root(s, search_max)
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


def get_path(s1, s2, search_max: bool = False):
    path = [s1]
    if s1 == s2:
        return [s1]
    if not s1.hypernyms():
        return []
    elif s2 in s1.hypernyms():
        return [s1, s2]
    count = 0
    ancestors = []
    for s in s1.hypernyms():
        tmp = get_path(s, s2, search_max)
        if search_max:
            if (len(tmp) > count or count == 0) and len(tmp) != 0:
                count = len(tmp)
                ancestors = tmp
        else:
            if (len(tmp) < count or count == 0) and len(tmp) != 0:
                count = len(tmp)
                ancestors = tmp
    if len(ancestors) == 0:
        return []
    path += ancestors
    return path


def bck_depth(sense):
    depth = 1
    while sense is not None and sense.hypernyms():
        depth += 1
        sense = sense.hypernyms()[0]
    return depth

def depth(sense):
    path_to_root = get_path_to_root(sense, search_max=True)
    depth = len(path_to_root)
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


def bck_find_path(s1, s2):
    path = []
    if s2 in s1:
        return path
    for x in s1[0].hypernyms():
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
    if s1 == s2:
        return 1.0
    if s1.pos() == 'v':
        # p1 = extract_ancestors([s1])
        p1 = get_path_to_root(s1)
        p1.remove(s1)

        # p2 = extract_ancestors([s2])
        # p2.append(s2)

        p2 = get_path_to_root(s2)

        path = p1 + p2
        path_len = len(path) + 1

    lcs = lowest_common_subsumer(s1, s2)
    if lcs:
        p1 = get_path(s1, lcs)
        p1.remove(s1)
        p2 = get_path(s2, lcs)
        p2.reverse()
        p2.remove(lcs)
        path = p1 + p2
        path_len = len(path)
    if path_len == 0:
        return None
    return (2 * max_depth - path_len) / (2 * max_depth)  # normalizziamo i risultati


def sim_shortest_path_lib(s1, s2):
    path_len = 0
    if s1 == s2:
        return 1.0
    if s1.pos() == 'v':
        # p1 = extract_ancestors([s1])
        p1 = get_path_to_root(s1)
        p1.remove(s1)

        # p2 = extract_ancestors([s2])
        # p2.append(s2)

        p2 = get_path_to_root(s2)

        path = p1 + p2
        path_len = len(path) + 1

    lcs = lowest_common_subsumer(s1, s2)
    # print("lcs: ", lcs)
    if lcs:
        # print('LCS______________: ', s1, " - ", s2)
        # p1 = find_path([s1], lcs)
        p1 = get_path(s1, lcs)
        p1.remove(s1)
        # print(p1)
        # p2 = find_path([s2], lcs)
        p2 = get_path(s2, lcs)
        # print(p2)
        # p2.insert(0, s2)
        p2.reverse()
        p2.remove(lcs)
        path = p1 + p2
        path_len = len(path)
    if path_len == 0:
        return None
    return 1 / (1 + path_len)  # con questa formula esce lo stesso risultato della libreria

def bck_sim_leakcock_chodorow(s1, s2):
    if s1.pos() != s2.pos():
        return None
    path = []
    lcs = lowest_common_subsumer(s1, s2)
    if lcs:
        # p1 = find_path([s1], lcs)
        p1 = get_path(s1, lcs)
        # p2 = find_path([s2], lcs)
        p2 = get_path(s2, lcs)
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


def sim_leakcock_chodorow(s1, s2):
    if s1.pos() != s2.pos():
        return None
    if s1.pos() != 'n' and s1.pos() != 'v':
        return None
    if s2.pos() != 'n' and s2.pos() != 'v':
        return None
    path = []
    lcs = lowest_common_subsumer(s1, s2)
    # print('lcs: ', lcs)
    if lcs:
        pp1 = find_path([s1], lcs)
        # print("pp1: ", pp1)
        p1 = get_path(s1, lcs)
        p1.remove(s1)
        # print("p1: ", p1)
        pp2 = find_path([s2], lcs)
        # print("pp2: ", pp2)
        p2 = get_path(s2, lcs)
        # print("p2: ", p2)
        # p2.insert(0, s2)
        p2.reverse()
        p2.remove(lcs)
        path = p1 + p2
        # print(len(path))
        # print("sp1: ", s1.shortest_path_distance(s2, simulate_root=True and s1.pos() == 'v'))
    # print("path: ", path)
    # return - log((1 + len(path)) / (1 + 2 * max_depth))
    # if lcs is None and s1.pos() == 'v':
    else:
        # p1 = extract_ancestors([s1])
        p1 = get_path_to_root(s1)
        p1.remove(s1)
        # p1.append(syn1[i])
        # p2 = extract_ancestors([s2])
        # p2.append(s2)
        p2 = get_path_to_root(s2)
        # print("p1: ", p1)
        # print("p2: ", p2)
        path = p1 + p2
        # print("formula 1")
        return - log((1 + len(path) + 1) / (2 * (max_depth_v + 1)))
    if s1.pos() == 'v':
        # print("formula 2")
        return - log((1 + len(path)) / (2 * max_depth_v))
    # print("formula 3")
    return - log((1 + len(path)) / (2 * max_depth))  # con questa formula esce lo stesso risultato della libreria
    # return - log((1 + len(path)) / (1 + 2 * max_depth))

def comp_max_depth(pos):
    depth = 0
    for ii in wn.all_synsets(pos):
        try:
            depth = max(depth, ii.max_depth())
        except RuntimeError:
            print(ii)
    return depth


def pearson_index(x, y):
    ax = x.mean()
    ay = y.mean()

    num = 0
    denx = 0
    deny = 0

    d = 0

    size = 0

    for i in range(len(x)):
        if not isnan(y[i]) and not isnan(x[i]):
            # pearson
            num += (x[i] - ax) * (y[i] - ay)
            denx += pow((x[i] - ax), 2)
            deny += pow((y[i] - ay), 2)

            # spearman
            # d += pow(x[i]-y[i], 2)

            size += 1
    return num / math.sqrt(denx * deny)


def spearman_index(x, y):
    map = {}
    for k in x.index:
        map[k] = x.loc[k]
    # print(map)
    boh = pd.DataFrame({'x': x, 'y': y})
    # print(boh.to_string())
    boh = boh.dropna()
    print(boh)
    # print(boh.to_string())
    print('x_____________________________')
    a = boh.sort_values('x')
    print(a)
    b = boh.sort_values('x')
    '''
    index = 0
    for i in b['x']:
        index += 1
        if not isnan(i):
            a['x'].loc[index] = index
    '''
    a['x'] = range(1, len(a) + 1)
    print(a.to_string())
    print('y_____________________________')
    b = a.sort_values('y')
    print(b)
    b['y'] = range(1, len(a) + 1)
    print(b)
    pearson_index(b['x'], b['y'])
    # print(boh.sort_values('y'))
    # Map( Pair(x,indice(x)), Pair(y, indice(y)) )


def find_no_hyp_synsets():
    df = pd.read_csv('WordSim353.csv', header=0)
    no_hyp = []
    all_hyp = []
    for row in df.index:
        w1 = df.loc[row, 'Word 1']
        w2 = df.loc[row, 'Word 2']
        for syn1 in wn.synsets(w1):
            if not syn1 in all_hyp:
                all_hyp.append(syn1)
            if not syn1.hypernyms() and not syn1 in no_hyp:
                no_hyp.append(syn1)
            for syn2 in wn.synsets(w2):
                if not syn2 in all_hyp:
                    all_hyp.append(syn2)
                if not syn2.hypernyms() and not syn2 in no_hyp:
                    no_hyp.append(syn2)
    print("\n", len(no_hyp))
    print("\n", len(all_hyp))
    # Eseguendo questa funzione è stato possibile contare il numero di synset che non hanno iperonimi pur non essendo la radice.
    # Sono 180 su un totale di 2273 synsets


def compute_all_sim(w1, w2):
    sim_wup = []
    sim_sp = []
    sim_sp_lib = []
    sim_lc = []
    for syn1 in wn.synsets(w1):
        for syn2 in wn.synsets(w2):
            sim_wup.append(sim_wu_palmer(syn1, syn2))
            sim_sp.append(sim_shortest_path(syn1, syn2))
            sim_sp_lib.append(sim_shortest_path_lib(syn1, syn2))
            sim_lc.append(sim_leakcock_chodorow(syn1, syn2))
    max_wup = pd.Series(sim_wup, dtype=float)
    max_sp = pd.Series(sim_sp, dtype=float)
    max_sp_lib = pd.Series(sim_sp_lib, dtype=float)
    max_lc = pd.Series(sim_lc, dtype=float)
    return max_wup.max(), max_sp.max(), max_lc.max(), max_sp_lib.max()


def run():
    df = pd.read_csv('WordSim353.csv', header=0)
    sim_wup = []
    sim_sp = []
    sim_sp_lib = []
    sim_lc = []
    for row in df.index:
        w1 = df.loc[row, 'Word 1']
        w2 = df.loc[row, 'Word 2']
        result = compute_all_sim(w1, w2)
        sim_wup.append(result[0])
        sim_sp.append(result[1])
        sim_lc.append(result[2])
        sim_sp_lib.append(result[3])
    df.insert(3, 'wup sim', sim_wup)
    df.insert(4, 'sp sim', sim_sp)
    df.insert(5, 'lc sim', sim_lc)
    df.insert(6, 'sp sim lib', sim_sp_lib)
    print(df)

    print('Pearson index wup sim : ', pearson_index(df['Human (mean)'], df['wup sim']))
    print('Pearson index sp sim  : ', pearson_index(df['Human (mean)'], df['sp sim']))
    print('Pearson index sp sim lib  : ', pearson_index(df['Human (mean)'], df['sp sim lib']))
    print('Pearson index lc sim  : ', pearson_index(df['Human (mean)'], df['lc sim']))

    df1 = pd.DataFrame({'1': df['Human (mean)'], '2': df['wup sim']})
    df2 = pd.DataFrame({'1': df['Human (mean)'], '2': df['sp sim']})
    df3 = pd.DataFrame({'1': df['Human (mean)'], '2': df['lc sim']})
    df4 = pd.DataFrame({'1': df['Human (mean)'], '2': df['sp sim lib']})

    print('\nSpearman index wup sim : ', df1.corr(method='spearman').iloc[0, 1])
    print('Spearman index sp sim  : ', df2.corr(method='spearman').iloc[0, 1])
    print('Spearman index sp sim lib  : ', df4.corr(method='spearman').iloc[0, 1])
    print('Spearman index lc sim  : ', df3.corr(method='spearman').iloc[0, 1])
    # x = df['Human (mean)']
    # y = df['wup sim']
    # spearman_index(x, y)
    exit()


max_depth = comp_max_depth('n')
max_depth_v = comp_max_depth('v')
run()
