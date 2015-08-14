__author__ = 'mborsodi'


def count_transform(trans_dict):

    keys = trans_dict.keys()

    all_nums = []

    for key in keys:
        all_nums.append(trans_dict[key])

    each_trans = zip(*all_nums)

    list_sums = []

    for key in each_trans:
        list_sums.append(sum(key))

    return list_sums


def _find_inv(motif):

    invs = []
    new_motif = ""

    # separating out intervals from string
    for e in range(1, len(motif)-1, 1):
        new_motif += motif[e]

    letters = []

    temp_inv = new_motif.split()

    for i in range(0, len(temp_inv), 1):

        for x in range(0, len(temp_inv[i])-1, 1):
            if temp_inv[i][x].isalpha():
                letters.append(temp_inv[i][x])
                temp_inv[i] = temp_inv[i].replace(temp_inv[i][x], '')

    # inversion
    for i in range(len(temp_inv)):

        inv = str(-(int(temp_inv[i])))
        temp_inv[i] = inv[:len(inv)-3] + letters[i] + inv[len(inv)-1:]

        invs.append(temp_inv[i])

    invs = ' '.join(invs)
    invs = "'" + invs + "'"
    return invs


# used by find_transform to get the retrograde of melodies
def _find_ret(motif):

    new_motif = ""

    # separating out intervals from string
    for e in range(1, len(motif)-1, 1):
        new_motif += motif[e]

    temp_ret = new_motif.split()
    temp_ret.reverse()

    ret = ' '.join(temp_ret)
    ret = "'" + ret + "'"

    return ret


def find_transform(motifs):

    dict_list = list(motifs.keys())

    for intls in dict_list:

        if intls in motifs:

            transformations = [
                _find_inv(intls),
                _find_ret(intls),
                _find_inv(_find_ret(intls))
            ]

            for trans in transformations:

                if trans in motifs:
                    if intls != trans:
                        motifs[intls].extend(motifs[trans])
                        del motifs[trans]

                    else:
                        motifs[intls].append(0)

                else:
                    motifs[intls].append(0)

    return motifs