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

from nltk.corpus import semcor as sc
from nltk.corpus import wordnet as wn


def lesk_algorithm(w, s):
    try:
        best_sense = wn.synsets(w)[0]
    except IndexError:
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
        #print('best sense: ', best_sense.lemmas()[0])
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

    tot, good = accuracy
    tot += 1
    if best_sense and sense_gold and (best_sense.lemmas()[0] == sense_gold):
        good += 1
    accuracy = (tot, good)
    i += 1

print('\n\n-----------------------------------------')
print('accuracy(tot/corrects): ', accuracy)
print('-----------------------------------------')
