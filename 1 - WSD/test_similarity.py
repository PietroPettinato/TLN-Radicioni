# funzioni di test per il file "1-test_similarity.py"

# -----------------------------------
# -------------- TESTS --------------
# -----------------------------------

def check_depth(syn):
    for i in range(len(syn)):
        s1hp = syn[i]._shortest_hypernym_paths(True)
        real_depth = s1hp.get(list(s1hp)[len(s1hp) - 1])
        my_depth = depth(syn[i])
        # my_depth = get_path(syn[i])
        if real_depth != my_depth:
            print(syn[i])
            print("my_depth  : ", my_depth)
            print("real_depth: ", real_depth)
            input("ERROR: Press Enter to continue...")
    print("------ ok, depth")


def check_lowest_common_subsumer(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_lcs = lowest_common_subsumer(syn1[i], syn2[j])
            right_lcs = syn1[i].lowest_common_hypernyms(syn2[j])
            # print("my_lcs  : ", my_lcs)
            # print("real lcs: ", right_lcs)
            # if (my_lcs is [] and right_lcs) or (my_lcs not in right_lcs):
            if my_lcs and right_lcs and my_lcs not in right_lcs:
                print("\nc1[" + str(i) + "]: " + str(syn1[i]))
                print("c2[" + str(j) + "]: " + str(syn2[j]))
                print("my_lcs  : ", my_lcs)
                print("real lcs: ", right_lcs)
                input("ERROR: Press Enter to continue...")
            break
    print("------ ok, lowest_common_subsumer")


def list_replace(lst, old, new):
    i = -1
    try:
        while 1:
            i = lst.index(old, i + 1)
            lst[i] = new
    except ValueError:
        pass


def check_sim_wu_palmer(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_sim = sim_wu_palmer(syn1[i], syn2[j])
            right_sim = syn1[i].wup_similarity(syn2[j])
            if my_sim != right_sim:
                print("\nc1[" + str(i) + "]: " + str(syn1[i]))
                print("c2[" + str(j) + "]: " + str(syn2[j]))
                print("My sim_wu_palmer:    ", my_sim)
                print("Right sim_wu_palmer: ", right_sim)
                input("ERROR: Press Enter to continue...")
                # break
        # break
    print("------ ok, sim_wu_palmer")


def check_sim_shortest_path(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            right_sim = syn1[i].path_similarity(syn2[j])
            my_sim = sim_shortest_path(syn1[i], syn2[j])
            if right_sim != my_sim:
                print("\nc1[" + str(i) + "]: ", syn1[i])
                print("c2[" + str(j) + "]: ", syn2[j])
                print("Mine : ", my_sim)
                print("Right: ", right_sim)
                input("ERROR: Press Enter to continue...")
            # print("right path 1: ", syn1[i]._shortest_hypernym_paths(False))
            # print("right path 2: ", syn2[j]._shortest_hypernym_paths(False))
    print("------ ok, sim_shortest_path")


def check_leakcock_chodorow(syn1, syn2):
    for i in range(len(syn1)):
        for j in range(len(syn2)):
            my_sim = sim_leakcock_chodorow(syn1[i], syn2[j])
            try:
                right_sim = syn1[i].lch_similarity(syn2[j])
                if right_sim != my_sim:
                    print("\nc1[" + str(i) + "]: ", syn1[i])
                    print("c2[" + str(j) + "]: ", syn2[j])
                    print("Right: ", right_sim)
                    print("Mine : ", my_sim)
                    input("ERROR: Press Enter to continue...")
            except Exception:
                # print("\nc1[" + str(i) + "]: ", syn1[i])
                # print("c2[" + str(j) + "]: ", syn2[j])
                # print("right sim error")
                pass
    print("------ ok, sim_leakcock_chodorow")
