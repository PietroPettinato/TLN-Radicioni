# todo per Massimo, avviare python dal terminale di IntelliJ e dare questi due comandi per scaricare il corpus SemCor
# import nltk
# nltk.download('semcor')
#
# dare questo comando per verificare se è tutto ok, stampa una lista con la frase "'The', 'Fulton', 'County', 'Grand', 'Jury', 'said', 'Friday' ....."
# print(sc.sents())

from nltk.corpus import semcor as sc
from nltk.corpus import wordnet as wn
import numpy as np


def lesk_algorithm(w, s):
    """
    Implementazione dell'algoritmo di Lesk.

    :param w: la parola da disambiguare
    :param s: la frase in cui si trova la parola w

    :return: il miglior synset per la parola in base alla disambiguazione
    """
    if not w:
        return None
    try:
        best_sense = wn.synsets(w)[0]
    except IndexError:  # nel caso in cui wn.synsets(w) è vuoto
        best_sense = None
    max_overlap = 0
    # context = set(s.split())
    context = set(s)
    signature = []
    for syn in wn.synsets(w):
        signature = syn.definition().lower().split()
        for ex in syn.examples():
            signature += ex.lower().split()
        signature = set(signature)
        overlap = signature.intersection(context)
        if len(overlap) > max_overlap:
            max_overlap = len(overlap)
            best_sense = syn
    return best_sense


def run():
    """
    Esecuzione sulle prime 50 frasi del corpus e con il primo sostantivo della frase.

    :return: accuracy dell'esecuzione
    """
    i = 0
    accuracy = (0, 0)
    for s in sc.tagged_sents(tag='pos'):
        if i == 50:
            break
        # prendiamo il primo nome
        noun = [t.leaves()[0] for t in s if t.label() == 'NN'][0]
        # prendiamo la frase
        sentence = sc.sents()[i]
        # usiamo l'algoritmo di Lesk per la disambiguzione del nome
        best_sense = lesk_algorithm(noun, sentence)

        # prendiamo dal corpus SemCor il senso corretto di noun
        sense_gold = None
        for t in sc.tagged_sents(tag='sem')[i]:
            if t[0] == noun:
                try:
                    sense_gold = t.label()
                except AttributeError:
                    pass
                break

        # aggiorniamo l'accuracy
        tot, corrects = accuracy
        tot += 1
        if best_sense and sense_gold and (str(best_sense.lemmas()[0]) == str(sense_gold)):
            corrects += 1
            # print('corrects++')
        accuracy = (tot, corrects)
        i += 1
    return accuracy


def random_sentences_selector():
    """
    Genera degli interi casuali che vengono usati come indici per scegliere frasi dal corpus SemCor.

    :return: un dizionario con l'indice intero e la corrispondente frase scelta casualmente
    """
    # x = 37176 # per velocizzare la computazione trattiamo il risultato di len(sc.sents()) come una costante
    x = 1500  # usando un numero molto alto (37176) la computazione è comunque troppo lenta, usiamo un intero più piccolo per velocizzare il processo
    # questo esclude alcune frasi del corpus, ma ci consente di considerare comunque un campione abastanza vasto

    indexes = np.random.randint(0, x, 50)
    sentences = {i: sc.tagged_sents(tag='pos')[i] for i in indexes}
    return sentences


def random_noun_selector(s):
    """
    Sceglie un nome a caso dalla frase.

    :param s: frase da cui scegliere il nome

    :return: il nome scelto
    """
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
        noun = random_noun_selector(sentences[k])
        sentence = sc.sents()[k]
        best_sense = lesk_algorithm(noun, sentence)

        sense_gold = None
        for t in sc.tagged_sents(tag='sem')[k]:
            if t[0] == noun:
                try:
                    sense_gold = t.label()
                except AttributeError:
                    pass
                break

        tot, corrects = accuracy
        tot += 1
        # if best_sense and sense_gold and (best_sense == sense_gold.synset()):
        if best_sense and sense_gold and (str(best_sense.lemmas()[0]) == str(sense_gold)):
            corrects += 1
        accuracy = (tot, corrects)
    return accuracy


# chiamiamo le funzioni e calcoliamo le accuracy
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

Il lemma scelto è sempre il primo della lista, si potrebbe provare a capire quale sia il migliore fra quelli disponibili

'''
