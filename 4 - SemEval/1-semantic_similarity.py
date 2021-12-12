# risultati di semeval_mapper.ipynb
# Pettinato      :	coppie nell'intervallo 51-100
# Donini         :	coppie nell'intervallo 201-250

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as sck_cs


df = pd.read_csv('annotated_data_pietro.tsv', sep='\t', names=['term 1', 'term 2', 'val Pietro'])

# todo aggiungere a df un'altra colonna con i valori di Massimo
# il file 'annotated_data_massimo.tsv' è la copia del mio ma ho cambiato i primi 4 valori per fare prove con gli indici e non avere l'indice == 1
df_massimo = pd.read_csv('annotated_data_massimo.tsv', sep='\t', names=['1', '2', 'val'])
df['val Massimo'] = df_massimo['val']
print(df)
print('\nMean value Pietro:', df['val Pietro'].sum() / len(df['val Pietro']))
print('\nMean value Massimo:', df['val Massimo'].sum() / len(df['val Massimo']))
print('\nPearson index:\n', df.corr(method='pearson'))
print('\nSpearman index:\n', df.corr(method='spearman'))


def term_to_bn_syn_ids(term):
    """
    Dato il termine nella forma '#termine' trova i suoi babelSynsetIDs nel file 'SemEval17_IT_senses2synsets.txt'

    :param term: il termine di cui cercare i babelSynsetIDs

    :return: la lista di babelSynsetIDs per t o la lista vuota se il termine non viene trovato
    """
    start = False  # serve per capire quando iniziano i babelSynsetIDs
    res = []
    with open('utils/SemEval17_IT_senses2synsets.txt', 'r') as f:
        for line in f.readlines():
            if start:  # iniziamo a raccogliere gli id
                if line[0] == '#':  # se la linea inizia per '#' vuol dire che iniziano gli ID di un nuovo termine e che quindi dobbiamo fermarci
                    return res
                res.append(line.rstrip('\n'))
            elif line.rstrip('\n') == term:  # quando troviamo il termine possiamo iniziare a raccogliere i babelSynsetIDs (start = True)
                start = True
    return res


def bn_syn_ids_to_nasari(bn_id):
    """
    Dato il babelSynsetID trova il suo vettore NASARI nel file 'mini_NASARI.tsv'

    :param bn_id: il babelSynsetID di cui cercare il vettore NASARI

    :return: il vettore NASARI
    """
    # todo che succede se il bn_id non è presente nel file? Bisogna tornare la lista vuota (se non lo fa già)
    nasari_vector = df_nasari[df_nasari.index.str.startswith(bn_id).fillna(False)]  # prendiamo la riga che inizia con il babelSynsetID
    return nasari_vector


def get_nasari_vectors(term):
    """
    Dato un termine ritorna i suoi vettori nasari

    :param term: il termine

    :return: la lista dei vettori NASARI di term o la lista vuota se il termine non ha vettori NASARI nel file 'mini_NASARI.tsv'
    """
    bn_syn_ids = term_to_bn_syn_ids('#' + term)
    nasari_vectors = []
    for id in bn_syn_ids:
        vector = bn_syn_ids_to_nasari(id)
        if vector.empty:
            print(f'al termine \'{term}\' manca il babelSynsetID {id} in \'mini_NASARI.tsv\', clear() dei vettori trovati e return')
            nasari_vectors.clear()
            return nasari_vectors
        nasari_vectors.append(vector)
    return nasari_vectors

'''
t = 'terremoto'
res = term_to_bn_syn_ids('#' + t)
print(f'\n\nBabelSynsetIDs for term \'{t}\':\n {res}')
nasari_vector = bn_syn_ids_to_nasari(res[0])
# nasari_vector = bn_syn_ids_to_nasari('blabla')
print('nasari_vector:', nasari_vector)
print('nasari_vector:', get_nasari_vectors(t))  # FUNZIONAAAAAA
'''


def cosine_similarity(v1, v2):
    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)
    return num/den


df_nasari = pd.read_csv('utils/mini_NASARI.tsv', sep='\t', header=None, index_col=0)  # usiamo la colonna con i babelSynsetIDs come indici del dataframe
cos_sim_list = []
for t1, t2 in zip(df['term 1'], df['term 2']):
    nasari_t1 = get_nasari_vectors(t1)
    nasari_t2 = get_nasari_vectors(t2)
    if nasari_t1 and nasari_t2:
        max_sim = 0
        for v1 in nasari_t1:
            for v2 in nasari_t2:
                cos_sim = cosine_similarity(np.array(v1.iloc[0][1:]), np.array(v2.iloc[0][1:]))
                if cos_sim > max_sim:
                    max_sim = cos_sim
        print('\nt1 = ', t1)
        print('t2 = ', t2)
        print('max cos_sim:', max_sim)
        cos_sim_list.append(max_sim)

        # todo i valori con None (Nan nel data frame) sono troppi, forse c'è un errore, Pio fa così: (molti hanno fatto l'accesso a BabelNet)
        '''
        for (id1, v1), (id2, v2) in itertools.product(w1_vectors, w2_vectors): # generate cartesian product of all possible pairs of senses
        if not(v1 is None or v2 is None): # skip if one or both of v1,v2 are none
            scores.append(similarity_func(v1, v2))
            senses.append((id1,id2))
        '''
        # input('---- continue? ----')
    else:
        print('\nt1 = ', t1)
        print('t2 = ', t2)
        print('max cos_sim:', None)
        print('nasari_t1 e/o nasari_t2 è vuoto')
        cos_sim_list.append(None)
        # input('---- continue? ----')

df['system val'] = cos_sim_list
print(df)


# prova per cotrollare se il calcolo della cos_sim è corretto (è corretto)
cos_sim_list2 = []
for t1, t2 in zip(df['term 1'], df['term 2']):
    nasari_t1 = get_nasari_vectors(t1)
    nasari_t2 = get_nasari_vectors(t2)
    if nasari_t1 and nasari_t2:
        max_sim = 0
        for v1 in nasari_t1:
            for v2 in nasari_t2:
                # n1 = np.array(v1).reshape(1, len(v1))
                # n2 = np.array(v2).reshape(1, len(v2))
                cos_sim = sck_cs(v1, v2)[0][0]
                if cos_sim > max_sim:
                    max_sim = cos_sim
        cos_sim_list2.append(max_sim)
    else:
        cos_sim_list2.append(None)
df['system val check'] = cos_sim_list2
print(df)





'''
	ragionamento prima parte eserictazione 4

passiamo da termine a/ai babelSynID con il file SemEval17_IT_senses2synsets.txt

con il/i babelSynID prendiamo il/i vettori NASARI con il file mini_NASARI.tsv

per ogni vettore NASARI di termine_1
	per ogni vettore NASARI di termine_2
		calcolo cos_sim
		aggiorno max_sim
ritorno max_sim (forse serve normalizzazione fra [0,4])
'''