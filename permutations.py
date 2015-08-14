__author__ = 'mborsodi'


def find_permutations(motifs):

    motif_list = motifs.keys()
    for motif in motif_list:
        if motif in motifs:
            key = ""

            for e in range(1, len(motif)-1, 1):
                key += motif[e]

            my_key = key.split()
            perms = _permute(my_key)

            for i in range(1, len(perms), 1):

                this = perms[i]
                this = ' '.join(this)
                this = "'" + this + "'"

                if this in motifs:

                    if motif != this:
                        motifs[motif].extend(motifs[this])
                        del motifs[this]

                    else:
                        motifs[motif].append(0)

                else:
                    motifs[motif].append(0)

    for key in motifs:

        perms = sum(motifs[key])-motifs[key][0]
        motifs[key] = [motifs[key][0], perms]

    return motifs


def _permute(arr):

    x = arr[0]
    new_arr = []

    for i in range(1, len(arr), 1):
        new_arr.append(arr[i])

    if len(arr) == 2:
        return _insert(x, new_arr)

    else:
        final = []

        if len(arr) > 2:
            for perm in _permute(new_arr):
                final.extend(_insert(x, perm))

        return final


def _insert(x, arr):

    group = []

    for i in range(0, len(arr)+1, 1):
        group.append(list(arr))
        group[i].insert(i, x)

    return group