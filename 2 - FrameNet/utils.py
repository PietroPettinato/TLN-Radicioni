import hashlib
from random import randint
from random import seed
from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn


def print_frames_with_IDs():
    for x in fn.frames():
        print('{}\t{}'.format(x.ID, x.name))


def get_frams_IDs():
    return [f.ID for f in fn.frames()]


def getFrameSetForStudent(surname, list_len=5):
    nof_frames = len(fn.frames())
    base_idx = (abs(int(hashlib.sha512(surname.encode('utf-8')).hexdigest(), 16)) % nof_frames)
    print('\nstudent: ' + surname)
    framenet_IDs = get_frams_IDs()
    i = 0
    offset = 0
    seed(1)
    while i < list_len:
        fID = framenet_IDs[(base_idx + offset) % nof_frames]
        f = fn.frame(fID)
        fNAME = f.name
        print('\tID: {a:4d}\tframe: {framename}'.format(a=fID, framename=fNAME))
        offset = randint(0, nof_frames)
        i += 1

# getFrameSetForStudent('Rossi')
# getFrameSetForStudent('verdi')
# getFrameSetForStudent('Gialli')
# getFrameSetForStudent('Radicioni')


def print_frame_info(f):
    print('NAME: {}[{}]\tDEF: {}'.format(f.name, f.ID, f.definition))

    print('\n____ FEs ____')
    FEs = f.FE.keys()
    for fe in FEs:
        fed = f.FE[fe]
        print('\tFE: {}\tDEF: {}'.format(fe, fed.definition))
        # print(fed.definition)

    print('\n____ LUs ____')
    LUs = f.lexUnit.keys()
    for lu in LUs:
        lud = f.lexUnit[lu]
        print('\tLU: {}\tDEF: {}'.format(lu, lud.definition))


def get_frame_words(f):
    words = list(f.FE.keys())
    words += f.lexUnit.keys()
    return words


def build_corpus_gold(frame_set, frame_id):
    # raccogliamo gli elementi in una lista
    f = fn.frame_by_id(frame_id)
    frame_words_list = [frame_set[frame_id]]
    frame_words_list += get_frame_words(f)
    print(frame_words_list, end='\n-------------------------------\n')
    # la lista viene manualmente disambiguata e viene assegnata alla variabile l (più avanti)

    # per avere le descrizioni (cambiare manualmente il frameID)
    print_frame_info(fn.frame_by_id(frame_id))

    # per avere i termini (altre liste nel flie 'liste disambiguate corpus gold.txt')
    l = ['Hiding', 'Obstruction', 'Object', 'Observer', 'Degree', 'Agent', 'Place', 'Place', 'Time', 'Explanation', 'Means', 'Purpose', 'Manner', 'hide.v', 'conceal.v', 'mask.v', 'shroud.v', 'camouflage.v', 'block.v', 'cover.v']
    for w in l:
        ss = wn.synsets(w)
        if not ss:
            n, pos = w.split('.')
            ss = wn.synsets(n, pos)
        print(f'{w},', str(ss).replace('Synset(', '').replace(')', ''))

