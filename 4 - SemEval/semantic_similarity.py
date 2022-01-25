# risultati di semeval_mapper.ipynb
# Donini         :	coppie nell'intervallo 201-250

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
import re


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
        if not vector.empty:  # escludiamo gli ID per cui non abbiamo i vettori NASARI
            nasari_vectors.append(vector)
    return nasari_vectors


def cosine_similarity(v1, v2):
    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)
    return num / den


# ----------------------------------------
# -------------- CONSEGNA 1 --------------
# ----------------------------------------


print('\n-----------------------------------------------\n')
print('Dati con le annotazioni manuali:\n')
df = pd.read_csv('annotated_data_pietro.tsv', sep='\t', names=['term 1', 'term 2', 'val Pietro'])
df_massimo = pd.read_csv('annotated_data_massimo.tsv', sep='\t', names=['1', '2', 'val'])
df['val Massimo'] = df_massimo['val']
print(df.to_string())


print('\n-----------------------------------------------\n')
print('Indici di correlazione fra gli annotatori:')
print('\nPearson index : ', df['val Pietro'].corr(df['val Massimo'], method='pearson'))  # indice di Pearson fra annotazioni Pietro e Massimo
print('Spearman index: ', df['val Pietro'].corr(df['val Massimo'], method='spearman'))  # indice di Spearman fra annotazioni Pietro e Massimo


print('\n-----------------------------------------------\n')
print('Aggiunta del valore medio fra i valori delle annotazioni:\n')
df['mean value'] = (df['val Pietro'] + df['val Massimo']) / 2  # aggiunta di una colonna con il valore medio per i calcoli successivi
df['mean value norm'] = df['mean value'] / 4  # valore medio normalizzato in [0,1] per paragonarlo con i risultati dell'algoritmo
print(df.to_string())


# calcoliamo la max cos_sim per tutti i termini
df_nasari = pd.read_csv('utils/mini_NASARI.tsv', sep='\t', header=None, index_col=0)  # usiamo la colonna con i babelSynsetIDs come indici del dataframe
cos_sim_list = []
syn1 = []
syn2 = []
for t1, t2 in zip(df['term 1'], df['term 2']):
    nasari_t1 = get_nasari_vectors(t1)
    nasari_t2 = get_nasari_vectors(t2)
    if nasari_t1 and nasari_t2:
        max_sim = 0
        syn = (None, None)
        for v1 in nasari_t1:
            for v2 in nasari_t2:
                cos_sim = cosine_similarity(np.array(v1.iloc[0][1:]), np.array(v2.iloc[0][1:]))  # dalla colonna 1 all'ultima abbiamo i valori
                if cos_sim > max_sim:
                    max_sim = cos_sim
                    syn = (v1.index[0], v2.index[0])  # come indice della Serie abbiamo i babelSynsetID, ne teniamo traccia per la seconda consegna
        cos_sim_list.append(max_sim)
        syn1.append(syn[0])
        syn2.append(syn[1])
    else:
        cos_sim_list.append(None)  # se i vettori NASARI non sono presenti nel file non possiamo calcolare la cos_sim ed inseriamo None
        syn1.append(None)  # anche i synset non ci servono
        syn2.append(None)


print('\n-----------------------------------------------\n')
print('Aggiunta dei valori annotati dal sistema (\'system val\'):\n')
df['system val'] = cos_sim_list
print(df.to_string())


print('\n-----------------------------------------------\n')
print('Indici di correlazione fra \'mean value\' e \'system val\':')
print('\nPearson index : ', df['mean value'].corr(df['system val'], method='pearson'))
print('Spearman index: ', df['mean value'].corr(df['system val'], method='spearman'))


# ----------------------------------------
# -------------- CONSEGNA 2 --------------
# ----------------------------------------


print('\n-----------------------------------------------\n')
print('Livello di agreement nelle annotazioni (kappa di Cohen) fra \'val Pietro\' e \'val Massimo\':')
print('\nKappa di Cohen: ', cohen_kappa_score(df['val Pietro'].astype(int), df['val Massimo'].astype(int)))


# syn1 e syn2 sono stati annotati durante il calcolo della cos_sim
df['babelSynsetID term 1'] = syn1
df['babelSynsetID term 2'] = syn2
print('\n-----------------------------------------------\n')
print('Aggiunta dei sensi trovati dal sistema (\'babelSynsetID term 1\', \'babelSynsetID term 2\'):\n')
print(df.to_string())


# carichiamo i sensi annotati a mano
df_gold = pd.read_csv('annotated_data_syn.tsv', sep='\t', names=['term 1', 'term 2', 'sim val', 'bnid 1', 'bnid 2', 'bn_terms 1', 'bn_terms 2'])
# print(df_gold.to_string())

# puliamo i babelSynsetID togliendo tutto ciò che è da '__' in poi (abbiamo le stringhe come nella prima colonna del file 'mini_NASARI.tsv')
res_alg1 = [re.sub('__.*$', '', str(s)) for s in df['babelSynsetID term 1']]
res_alg2 = [re.sub('__.*$', '', str(s)) for s in df['babelSynsetID term 2']]

# costruiamo un dataframe con i risultati del sistema e quelli annotati a mano per calcolare l'accuracy
df2 = pd.DataFrame({'alg 1': res_alg1,
                    'gold 1': df_gold['bnid 1'],
                    'alg 2': res_alg2,
                    'gold 2': df_gold['bnid 2']})

mask1 = df2['alg 1'] == df2['gold 1']  # controlliamo la prima colonna di termini
mask2 = df2['alg 2'] == df2['gold 2']  # controlliamo la seconda colonna di termini
acc1 = (len(df2[mask1]), len(df2[mask2]))

mask3 = (df2['alg 1'] == df2['gold 1']) & (df2['alg 2'] == df2['gold 2'])  # controlliamo le coppie di termini
acc2 = len(df2[mask3])

# print(df2.to_string())

print('\n-----------------------------------------------\n')
print('Calcolo dell\'accuracy:')
print('\nAccuracy sui singoli termini:')
print(f'\tprima colonna  :  {acc1[0]}/50')
print(f'\tseconda colonna:  {acc1[1]}/50')
print(f'Accuracy sulle coppie di termini:  {acc2}/50')

