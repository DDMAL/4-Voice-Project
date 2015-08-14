__author__ = 'mborsodi'

import pandas
import music21
from vis.models.indexed_piece import IndexedPiece
from vis.analyzers.indexers import noterest, interval, ngram


# n - an int representing the number of gram you want e.g. 2-gram
def ngram_count(piece, settings, n):

    ngrams = []
    ngram_freq = {}

    ind_piece = IndexedPiece(piece)
    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    horiz_setts = settings

    # horiz-attach-later has to be true for the ngram indexer to work
    horiz_setts['horiz_attach_later'] = True

    horiz = interval.HorizontalIntervalIndexer(the_notes, horiz_setts).run()
    vert = interval.IntervalIndexer(the_notes, settings).run()
    intls = pandas.concat([horiz, vert], axis=1)

    parts = len(the_score.parts)

    # gets ngrams between all possible combinations of parts
    for x in range(parts):
        setts = {'mark singles': False,
                 'continuer': '1',
                 'n': n,
                 'horizontal': [('interval.HorizontalIntervalIndexer', str(x))]}

        for i in range(x+1, parts, 1):

            num = str(x) + ',' + str(i)
            setts['vertical'] = [('interval.IntervalIndexer', num)]
            ngram_test = ind_piece.get_data([ngram.NGramIndexer], setts, intls)
            ngrams.extend(ngram_test.values.tolist())

    # count ngrams
    for my_ngram in ngrams:
        my_ngram = str(' '.join(my_ngram))

        if 'Rest' in my_ngram:
            pass

        elif my_ngram in ngram_freq.keys():
            ngram_freq[my_ngram] += 1

        else:
            ngram_freq[my_ngram] = 1

    return ngram_freq