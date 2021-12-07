from pprint import pprint

from typing import Dict

from utils import *
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn


def get_frame_set_elements(frame_set: Dict[int, str]):
    """
    Funzione per la raccolta di Nome, FEs, LUs di ogni frame del frame set

    :param frame_set: il frame set con i frame ed i loro ID

    :return: due dizionari con gli elemenenti (frame_words) e le loro definizioni (frame_words_def)
    """
    frame_words = {}
    frame_words_def = {}
    for id in frame_set.keys():
        f = fn.frame_by_id(id)
        frame_words[id] = {'NAME': frame_set[id], 'FE': list(f.FE.keys()), 'LU': list(f.lexUnit.keys())}
        frame_words_def[id] = {'NAME DEF': f.definition, 'FE DEFS': [f.FE[fe].definition for fe in f.FE.keys()], 'LU DEFS': [f.lexUnit[lu].definition for lu in f.lexUnit.keys()]}
    return frame_words, frame_words_def


def get_ctx(s):
    ctx_s = []
    # print('gggggggggggggggggggggggggggggggggggggggggggggggggggggg')
    # print('(3.1) ctx_s:', ctx_s)
    for hype in s.hypernyms():
        ctx_s += hype.definition().split()
        # print('(3.1.1) ctx_s:', ctx_s)
        # ctx_s += hyp.examples()
        [ctx_s.extend(ex.split()) for ex in hype.examples()]
        # print('(3.1.2) ctx_s:', ctx_s)
    for hypo in s.hyponyms():
        ctx_s += hypo.definition().split()
        # print('(3.2.1) ctx_s:', ctx_s)
        #ctx_s += hyp.examples()
        [ctx_s.extend(ex.split()) for ex in hypo.examples()]
        # print('(3.2.2) ctx_s:', ctx_s)
    # print('get_ctx(): ', ctx_s)
    return ctx_s


# getFrameSetForStudent('pettinato')
# getFrameSetForStudent('Donini')

# frame set costruito con i frame ottenuti da getFrameSetForStudent(), la chiave è il frameID e il valore è il nome del frame eventualmente disambiguato
# i termini sono già disambiguati ed alcuni frame non presenti su WordNet sono stati sostituiti
frame_set = {
    2021: 'Conquering',
    2010: 'Hunting',
    550: 'Claim',
    2481: 'Erasing',
    2566: 'Trajectory',
    790: 'Amalgamation',
    2597: 'Convoy',
    1655: 'Be', #262: 'Abounding', #1578: 'Waver',
    2916: 'Abundance', #266: 'Bungling',
    1673: 'Hiding'
}

# build_corpus_gold(frame_set, 2021)
# exit()

# prendiamo gli elementi ed i loro contesti di disambiguazione
frame_words, frame_words_def = get_frame_set_elements(frame_set)
# pprint(frame_words)
# pprint(frame_words_def)
# exit()

# todo i tre for funzionano, c'è molto codice duplicato, fare refactoring e ottimizzare
# todo sistemare il gold_corpus.csv e fare funzione per calcolare l'accuracy (magari si può inserire nei cicli for, calcoliamo senso e controlliamo se è giusto)

for id in frame_set.keys():
    elems = frame_words[id]

    # funziona, l'accuracy sembra un po' bassa
    for w, ctx_w in zip(elems['LU'], frame_words_def[id]['LU DEFS']):
        word, pos = w.split('.')
        ctx_w = ctx_w.lower().split()

        max = 0
        best_sense = None
        for s in wn.synsets(word, pos=pos):
            ctx_s = s.definition().lower().split()
            # print('(1) ctx_s:', ctx_s)
            [ctx_s.extend(ex.lower().split()) for ex in s.examples()]
            # print(s.examples())
            # print('(2) ctx_s:', ctx_s)
            ctx_s += get_ctx(s)
            # print('(3) ctx_s:', ctx_s)
            ctx_s = set(ctx_s)
            score = len(ctx_s.intersection(ctx_w)) + 1
            if score > max:
                max = score
                best_sense = s
        print(w, '-', best_sense)


for id in frame_set.keys():
    elems = frame_words[id]

    # funziona, l'accuracy sembra buona
    for w, ctx_w in zip(elems['FE'], frame_words_def[id]['FE DEFS']):
        ctx_w = ctx_w.lower().split()

        max = 0
        best_sense = None
        for s in wn.synsets(w):
            ctx_s = s.definition().lower().split()
            # print('(1) ctx_s:', ctx_s)
            [ctx_s.extend(ex.lower().split()) for ex in s.examples()]
            # print(s.examples())
            # print('(2) ctx_s:', ctx_s)
            ctx_s += get_ctx(s)
            # print('(3) ctx_s:', ctx_s)
            ctx_s = set(ctx_s)
            score = len(ctx_s.intersection(ctx_w)) + 1
            if score > max:
                max = score
                best_sense = s
        print(w, '-', best_sense)


for id in frame_set.keys():
    elems = frame_words[id]

    # funziona, l'accuracy sembra un po' bassa
    w = elems['NAME']
    ctx_w = frame_words_def[id]['NAME DEF'].lower().split()

    max = 0
    best_sense = None
    for s in wn.synsets(w):
        ctx_s = s.definition().lower().split()
        # print('(1) ctx_s:', ctx_s)
        [ctx_s.extend(ex.lower().split()) for ex in s.examples()]
        # print(s.examples())
        # print('(2) ctx_s:', ctx_s)
        ctx_s += get_ctx(s)
        # print('(3) ctx_s:', ctx_s)
        ctx_s = set(ctx_s)
        score = len(ctx_s.intersection(ctx_w)) + 1
        if score > max:
            max = score
            best_sense = s
    print(w, '-', best_sense)






'''
    FLUSSO DI ESECUZIONE:
per ogni frame 
    per ogni elemento (name, fe, lu)
        creo contesto di disambiguazione dell'elemento (nam.def o fe.def o lu.def)
        uso bagOfWords/grafico per disambiguare e trovare il wn.synset migliore

creo corpus gold (come??)
confronto con corpus gold
aggiorno accuracy
'''




'''
############################
##         NOTE           ##
############################

L'annotazione manuale è avvenuta utilizzando l'output della funzione build_corpus_gold(), che ritorna i possibili synset
di WN ed una descrizione degli elementi del frame (Name, FEs, LUs). Usando la descrizione, è stato scelto il synset più 
adatto.
'''
