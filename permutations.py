__author__ = 'mborsodi'


def find_permutations(motifs):

    motif_list = motifs.keys()
    for each in motif_list:
        if each in motifs:
            key = ""

            for e in range(1, len(each)-1, 1):
                key += each[e]

            my_key = key.split()
            perms = _permute(my_key)

            for i in range(1, len(perms), 1):

                this = perms[i]
                this = ' '.join(this)
                this = "'" + this + "'"

                if this in motifs:

                    if each != this:
                        motifs[each].extend(motifs[this])
                        del motifs[this]

                    else:
                        motifs[each].append(0)

                else:
                    motifs[each].append(0)

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
            for each in _permute(new_arr):
                final.extend(_insert(x, each))

        return final


def _insert(x, arr):

    group = []

    for i in range(0, len(arr)+1, 1):
        group.append(list(arr))
        group[i].insert(i, x)

    return group