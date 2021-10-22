import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
'''
term = 'board'
for synset in wn.synsets(term):
	print(synset.name(), synset.lemma_names())
	print(f'def: {synset.definition()}')
	print(f'examples: {synset.examples()}')
	print('-----hyponymes-----')
	for hypon in synset.hyponyms():
		print(f'hypon: {str(hypon)}')

	print('-----hypernyms-----')
	for hyper in synset.hypernyms():
		print(f'hypon: {str(hyper)}')

	print()
'''

print(wn.synset('board.n.02').part_meronyms())


s1 = wn.synset('cat.n.01') # prendimao il primo senso di "cat"
s2 = wn.synset('dog.n.01')

print(f'def({s1}): {s1.definition()}\n')
print(f'def({s2}): {s2.definition()}')


# ecco alcune misure di similarità
print(f'WUP_similarity({s1},{s2}): {s1.wup_similarity(s2)}\n')
print(f'LCH_similarity({s1},{s2}): {s1.lch_similarity(s2)}\n')
print(f'PTH_similarity({s1},{s2}): {s1.path_similarity(s2)}\n')



# APPUNTI ULTIMA SLD ESERCITAZIONE:
# se le 50 frasi fossero parametrizzabili sarebbe meglio
# www.nltk.org/howto/wordnet.html
