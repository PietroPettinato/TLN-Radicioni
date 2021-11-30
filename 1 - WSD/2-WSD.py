# todo per Massimo, avviare python dal terminale di IntelliJ e dare questi due comandi per scaricare il corpus SemCor
# import nltk
# nltk.download('semcor')
#
# dare questo comando per verificare se è tutto ok, stampa una lista con la frase "'The', 'Fulton', 'County', 'Grand', 'Jury', 'said', 'Friday' ....."
# print(sc.sents())
#
#
# possibile funione per caricare manualmente il corpus (cambiare il path)
# semcor = LazyCorpusLoader(
# "semcor", SemcorCorpusReader, r"brown./tagfiles/br-.*\.xml", wordnet
# )  # Must be defined *after* wordnet corpus.

from pprint import pprint
from nltk.corpus import semcor as sc
from nltk.corpus import wordnet as wn
import numpy as np


def lesk_algorithm(w, s):
    if not w:
        return None
    try:
        best_sense = wn.synsets(w)[0]
    except IndexError:  # if wn.synsets(w) is empty
        best_sense = None
    max_overlap = 0
    # context = set(s.split())
    context = set(s)
    signature = []
    for syn in wn.synsets(w):
        signature = syn.definition().split()
        for ex in syn.examples():
            signature += ex.split()
        signature = set(signature)
        overlap = signature.intersection(context)
        if len(overlap) > max_overlap:
            max_overlap = len(overlap)
            best_sense = syn
    return best_sense


def run():
    """
    Esecuzione sulle prime 50 frasi del corpus e con il primo sostantivo della frase

    :return: accuracy dell'esecuzione
    """
    i = 0
    accuracy = (0, 0)
    for s in sc.tagged_sents(tag='pos'):
        if i == 50:
            break
        '''
        pprint(s)
        for t in s:
            print(t.pos())
            print(t.leaves())
            print(t.label())
            if t.label() == 'NN':
                # w = t.pos()
                w = t.leaves()[0]
                print('w: ', w)
                m = t.label()
                print('m: ', m)
                break
        '''
        noun = [t.leaves()[0] for t in s if t.label() == 'NN'][0]
        #print('\nnoun: ', noun)
        sentence = sc.sents()[i]
        #print('sentence: ', sentence)
        best_sense = lesk_algorithm(noun, sentence)
        #try:
            #print('best sense: ', best_sense.lemmas())
        #except AttributeError:
            #print('best sense: ', None)

        sense_gold = None
        for t in sc.tagged_sents(tag='sem')[i]:
            #print(t)
            if t[0] == noun:
                try:
                    sense_gold = t.label()
                except AttributeError:
                    pass
                break
        #print('correct   : ', sense_gold)

        tot, corrects = accuracy
        tot += 1
        #if best_sense and sense_gold and (best_sense.lemmas()[0] == sense_gold): # todo controllare quale if usare, il secondo è corretto o scarta anche alcune giuste?
        if best_sense and sense_gold and (str(best_sense.lemmas()[0]) == str(sense_gold)):
            corrects += 1
            #print('corrects++')
        else:
            pass
            #input('---- wrong ----')
        accuracy = (tot, corrects)
        i += 1
    return accuracy


def random_sentences_selector():
    # x = 37176 # to speed up computation we use the result of len(sc.sents()) as a constant
    x = 1500  # it takes too long with an high number (37176), so we consider a smaller fixed integer
    indexes = np.random.randint(0, x, 50)
    sentences = {i: sc.tagged_sents(tag='pos')[i] for i in indexes}
    return sentences


def random_noun_selector(s):
    nouns = [t.leaves()[0] for t in s if t.label() == 'NN']
    if len(nouns) == 0:
        return None
    index = np.random.randint(0, len(nouns))
    return nouns[index]


def randomized_run():
    """
    Esecuzione su 50 frasi random del corpus e con un sostantivo casualmente scelto nella frase

    :return: accuracy dell'esecuzione
    """
    accuracy = (0, 0)
    sentences = random_sentences_selector()
    for k in sentences.keys():
        #pprint(sentences[k])
        noun = random_noun_selector(sentences[k])
        #print('\nnoun: ', noun)
        sentence = sc.sents()[k]
        #print('sentence: ', sentence)
        best_sense = lesk_algorithm(noun, sentence)
        #try:
            #print('best sense: ', best_sense.lemmas()[0])
        #except AttributeError:
            #print('best sense: ', None)

        sense_gold = None
        for t in sc.tagged_sents(tag='sem')[k]:
            #print(t)
            if t[0] == noun:
                try:
                    sense_gold = t.label()
                except AttributeError:
                    pass
                break
        #print('correct   : ', sense_gold)

        tot, corrects = accuracy
        tot += 1
        if best_sense and sense_gold and (str(best_sense.lemmas()[0]) == str(sense_gold)):
            corrects += 1
            #print('corrects++')
        accuracy = (tot, corrects)
        #input('---- continue? ----')
    return accuracy


accuracy = run()
print('\n\n------------------------------------------------')
print('  accuracy (tot/corrects)     : ', accuracy, end='\n')
for i in range(10):
    accuracy_rand = randomized_run()
    print(f'  {i}) accuracy rand (tot/corrects): ', accuracy_rand)
print('------------------------------------------------')


'''
------------------------------------------------
  accuracy (tot/corrects)     :  (50, 26)
  
  0) accuracy rand (tot/corrects):  (51, 19)
  1) accuracy rand (tot/corrects):  (50, 17)
  2) accuracy rand (tot/corrects):  (49, 11)
  3) accuracy rand (tot/corrects):  (51, 18)
  4) accuracy rand (tot/corrects):  (50, 16)
  5) accuracy rand (tot/corrects):  (51, 15)
  6) accuracy rand (tot/corrects):  (51, 18)
  7) accuracy rand (tot/corrects):  (51, 15)
  8) accuracy rand (tot/corrects):  (50, 21)
  9) accuracy rand (tot/corrects):  (48, 17)
------------------------------------------------

media      : 52%
media_rand : 33,4%



############################
##         NOTE           ##
############################

La scelta random delle frasi avviene usando un valore inferiore alla dimensione delle frasi del corpus per velocizzare il loro recupero. 
Infatti se gli indici sono troppo grandi, il tempo per l'accesso aumenta notevolmente. È sufficiente cambiare il valore per considerare il numero completo.

L'accuracy è molto più alta per le prime 50 frasi, con la randomizzazione cala notevolmente passando da circa 50% a circa 30%, probabilmente influisce 
il nome scelto e la complessità della frase.

'''
