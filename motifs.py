__author__ = 'mborsodi'

import music21
from vis.analyzers.indexers import noterest, interval, offset


def given_mel(melody, piece, off_setts, intl_setts, percent):

    result = 0

    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    off = offset.FilterByOffsetIndexer(the_notes, off_setts).run()
    horiz = interval.HorizontalIntervalIndexer(off, intl_setts).run()

    for x in range(len(the_score.parts)):

        part_ints = (horiz['interval.HorizontalIntervalIndexer', str(x)])
        part_ints = part_ints.tolist()

        for i in range(0, len(part_ints), 1):
            part_ints[i] = str(part_ints[i])

        while 'nan' in part_ints:
            part_ints.remove('nan')

        result += _compare(melody, part_ints, percent)

    return result


def _compare(melody, my_notes, percent):

    percent /= 100.0
    result = 0
    length = len(melody)

    for e in range(0, len(my_notes)-length, 1):

        test = []
        for i in range(0, length, 1):
            test.append(my_notes[e+i])

        temp = 0

        for s, y in zip(test, melody):
            if s == y:
                temp += 1.0
            else:
                break

        if temp/length >= percent:
            result += 1

    return result


def motivic_count(piece, intl_setts, settings):

    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()
    horiz = interval.HorizontalIntervalIndexer(the_notes, intl_setts).run()

    int_dict = {}
    transpose_dict = {}

    for n in range(len(the_score.parts)):

        # find notes in order to be able to find the transposition later
        my_notes = the_notes['noterest.NoteRestIndexer'][str(n)].tolist()

        intls = (horiz['interval.HorizontalIntervalIndexer', str(n)]).tolist()

        # convert each to string
        for i in range(len(intls)):
            intls[i] = str(intls[i])

        for i in range(len(my_notes)):
            my_notes[i] = str(my_notes[i])

        # remove 'nan' from both lists
        while 'nan' in intls:
            intls.remove('nan')

        while 'nan' in my_notes:
            my_notes.remove('nan')

        last_pos = (len(intls) - 1)

        # function to add the motifs to both dictionaries
        def add_to(the_motif, pos):

            notes = ' '.join(the_motif)
            notes = "'" + notes + "'"

            if notes in int_dict:
                int_dict[notes][0] += 1
                transpose_dict[notes].append(my_notes[pos])

            else:
                int_dict[notes] = [1]
                transpose_dict[notes] = [my_notes[pos]]

        # create motif of a given length starting on each possible note
        for i in range(last_pos - settings['length']):

            motif = []
            for x in range(settings['length']):

                motif.append(intls[i + x])

            if 'Rest' in motif:
                pass

            else:
                add_to(motif, i)

    which_dict = {
        'count': int_dict,
        'transpositions': transpose_dict,
        'both': [int_dict, transpose_dict]
    }

    if settings['which'] in which_dict:
        return which_dict[settings['which']]

    else:
        return