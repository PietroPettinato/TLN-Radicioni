from pprint import pprint

from typing import Dict

import pandas as pd

from utils import *
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn


def get_frame_set_elements(frame_set: Dict[int, str]):
    """
    Funzione per la raccolta di Name, FEs, LUs di ogni frame del frame set

    :param frame_set: il frame set con i frame ed i loro ID

    :return: due dizionari con gli elementi (frame_words) e le loro definizioni (frame_words_def)
    """
    frame_words = {}
    frame_words_def = {}
    for id in frame_set.keys():
        f = fn.frame_by_id(id)
        frame_words[id] = {'NAME': frame_set[id], 'FE': list(f.FE.keys()), 'LU': list(f.lexUnit.keys())}
        frame_words_def[id] = {'NAME DEF': f.definition, 'FE DEFS': [f.FE[fe].definition for fe in f.FE.keys()],
                               'LU DEFS': [f.lexUnit[lu].definition for lu in f.lexUnit.keys()]}
    return frame_words, frame_words_def


def get_ctx(s):
    """
    Prende gli iperonimi e gli iponimi del synset s e ritorna una lista con tutti i termini delle loro definizioni e dei loro esempi

    :param s: il synset di WN

    :return: lista di termini che fungono da contesto per s
    """
    ctx_s = []
    for hype in s.hypernyms():
        ctx_s += hype.definition().split()
        [ctx_s.extend(ex.split()) for ex in hype.examples()]
    for hypo in s.hyponyms():
        ctx_s += hypo.definition().split()
        [ctx_s.extend(ex.split()) for ex in hypo.examples()]
    return ctx_s


def find_sense(word, ctx_w, pos:str=None):
    """
    Trova il senso in WN per la parola word tramite un approccio bag of words.

    :param word: il termine da disambiguare
    :param ctx_w: il contesto del termine word composto dalle definizioni del suo frame in FrameNet
    :param pos: l'eventuale POS del termine (usato solo per le lexical units)

    :return: il senso più adatto per il termine word
    """
    multiwords = {'Particular_iteration': 'Iteration',
                  'Part_1': 'Part',
                  'Part_2': 'Part',
                  'band together': 'band',
                  'come together': 'come',
                  'Aggregate_property': 'Property',
                  'Source_symbol': 'Symbol',
                  'Source_representation': 'Representation',
                  'Target_symbol': 'Symbol',
                  'Target_representation': 'Representation',
                  'Hidden_object': 'Object',
                  'Potential_observer': 'Observer'
                  }
    if word in multiwords.keys():
        # in caso di multiwords usiamo un dizionario per ricondurle al termine reggente
        word = multiwords[word]
    max = 0
    best_sense = None
    for s in wn.synsets(word, pos=pos):
        ctx_s = s.definition().lower().split()
        [ctx_s.extend(ex.lower().split()) for ex in s.examples()]
        ctx_s += get_ctx(s)
        ctx_s = set(ctx_s)
        score = len(ctx_s.intersection(ctx_w)) + 1
        if score > max:
            max = score
            best_sense = s
    return best_sense


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
    1655: 'Be',
    2916: 'Abundance',
    1673: 'Hiding'
}

# build_corpus_gold(frame_set, 2021)

# prendiamo gli elementi ed i loro contesti di disambiguazione da FrameNet
frame_words, frame_words_def = get_frame_set_elements(frame_set)
# pprint(frame_words)
# pprint(frame_words_def)


# con gli elementi trovati estraiamo i sensi da WN
words = []
senses = []
for id in frame_set.keys():
    elems = frame_words[id]

    # disambiguiamo il nome del frame
    w = elems['NAME']
    ctx_w = frame_words_def[id]['NAME DEF'].lower().split()
    words.append(w)
    senses.append(find_sense(w, ctx_w).name())

    # disambiguiamo i FEs del frame
    for w, ctx_w in zip(elems['FE'], frame_words_def[id]['FE DEFS']):
        ctx_w = ctx_w.lower().split()
        words.append(w)
        senses.append(find_sense(w, ctx_w).name())

    # disambiguiamo le lexical units del frame
    for w, ctx_w in zip(elems['LU'], frame_words_def[id]['LU DEFS']):
        word, pos = w.split('.')
        ctx_w = ctx_w.lower().split()
        words.append(w)
        senses.append(find_sense(word, ctx_w, pos).name())


df = pd.DataFrame({'word': words,
                   'sense': senses})
df_gold = pd.read_csv('corpus gold/gold_corpus.csv', names=['word', 'gold sense'])
df['gold sense'] = df_gold['gold sense']

# stampiamo i risultati
print(df.to_string())

# calcoliamo l'accuracy
accuracy = (len(df[df['sense'] == df['gold sense']]), len(df))
print(f'\n\nAccuracy: {accuracy[0]}/{accuracy[1]}')




'''
############################
##         NOTE           ##
############################

L'annotazione manuale è avvenuta utilizzando l'output della funzione build_corpus_gold(), che ritorna i possibili synset
di WN ed una descrizione degli elementi del frame (Name, FEs, LUs). Usando la descrizione, è stato scelto il synset più 
adatto.

In caso di multiwords usiamo una mappa per ricondurle al termine corretto, un approccio più generale potrebbe essere
quello di usare un parser e delle regole per scegliere fra le varie parole.


Nei risultati notiamo che il programma funziona bene per le LU (il POS tag aiuta molto).
'''
