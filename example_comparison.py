import ngrams
import motifs
import transformations
import permutations
import features
import nodes


josqy = [
    'music/testing/Josquin-1.midi',  # Fortuna Desperata
    'music/testing/Josquin-2.mei'  # Malheur me bat
]

ocky1 = [
    'music/testing/Ockeghem-1.mei',  # De plus en plus
    'music/testing/Ockeghem-2.mid'  # Ma maistresse
]


# settings are the settings used for the interval indexers in VIS
settings = {'simple or compound': 'simple', 'quality': True}


# ngram_count() returns a dictionary of ngrams and how frequently they occur
ngrams.ngram_count(josqy[0], settings, 4)


# off_setts are the settings used by the offset indexer
off_setts = {'quarterLength': 1.0, 'horiz-attach-later': True}


# the length provided refers to how long the motifs are that you search for
# length accepts only ints
# The possible values for 'which' are 'Count', 'Transformations' and 'Both'.
# 'Count' returns a dictionary of motifs and how how frequently they occur.
# 'Transformations' returns a one of motifs and at which pitches they occur.
# 'Both' returns a list of these two dictionaries.
setts = {'length': 4, 'which': 'Count'}

the_motifs = motifs.motivic_count(josqy[0], settings, setts)


# This is a sample melody that you can search the piece for
melody = ['m2', 'M2', 'M2']


# This function takes the melody and piece, and finds how often it occurs. It
# searches by percent similarity, so that must also be included. It only returns
# an int of how many occurrences there are.
motifs.given_mel(melody, josqy[0], off_setts, settings, 100)


# find_transform() finds and counts the transformations of the motifs. It takes
# a dictionary of motifs that motivic_count() outputs. 'which' setting must be
# 'Count' for this to work properly.
trans = transformations.find_transform(the_motifs)


# count_transform() takes output from find_transform() and counts how many times
# each type of transformation occurs all together.
transformations.count_transform(trans)

# find_permutations() has the same input as find_transform(). Its output is the
# same, but all the permutations are counted as one (e.g. the output [1, 13]
# means there is 1 original version of the motif, and 13 permutations total).
the_motifs = motifs.motivic_count(josqy[0], settings, setts)
permutations.find_permutations(the_motifs)


# frequency() finds how often each value in a dictionary occurs, rather than the
# keys.
the_motifs = motifs.motivic_count(josqy[0], settings, setts)
for each in the_motifs:
    the_motifs[each] = the_motifs[each][0]
motif_freq = features.frequency(the_motifs)


# write_file() takes lists or dictionaries as input and writes them to a csv
# file. A title and any labels you wish to be included are taken as arguments
# as well as the data itself.
# For example, to write a file of the motifs and their transformations you could
# do something like this:
labels = [
    'motif',
    'prime form',
    'inversion',
    'retrograde',
    'retrograde inversion']

features.write_file(trans, 'my_transformations', labels)


# Similarly, plot_graph() takes lists or dictionaries and plots them as best it
# can. It is usually best to sort your data before giving it to this function,
# because it doesn't have anything like that implemented yet.
features.plot_graph(motif_freq, 'my motivic frequencies', 'x', 'y')


# deviation() takes as input a list of lists. Each list is numbers (usually
# taken from the output of count_transform()). The function the finds the
# percentage of the whole that each number is, averages the different types of
# numbers and finds the standard deviation. Types of numbers means that it
# averages all the counted occurrences of the prime form together, or of the
# inversion.
numbers = []
for each in josqy:

    the_motifs = motifs.motivic_count(each, settings, setts)
    trans = transformations.find_transform(the_motifs)
    thing = transformations.count_transform(trans)
    numbers.append(thing)

features.deviation(numbers)