#4-Voice-Project

##Comparing the music of Josquin and Ockeghem

A set of python scripts that use the VIS-framework designed to complete various different tasks with the idea of comparing pieces, or sets of pieces, in mind.

###Included:

####ngrams.py

Includes the `ngram_count()` function, which takes in a piece and some settings and outputs a dictionary of all the ngrams of a given length found in the piece, and how often each one occurs. Currently, this function finds ngrams between every possible pair of voices, but always with the lower voice as the horizontally moving one. The only customizable aspect is that you can give the length of the ngrams you would like to look at (e.g. 2-grams, 3-grams, etc).

####motifs.py

Includes the `motivic_count()` function and the `given_mel()` function.

`motivic_count()` is pretty much the same as `ngram_count()`, except instead of using ngrams, it uses motifs. In this case, a motif is defined as a sequence of intervals of a given length, not interrupted by rests. 

There are two required settings for this function; the 'which' setting specifies what the function returns. The possible values are 'count', which refers to a dictionary of motifs with their frequency of occurrences, 'transpositions', a dictionary of motifs and a list of the pitches they start at, and 'both', which gives you both dictionaries in a list.

The other setting is the 'length' setting, which defines how many intervals long the motifs are that you want to look for.

The other option is the `given_mel()` function. This one takes as input a piece, settings for the offset indexer, settings for the interval indexers, a given melody in list form and a percentage of similarity. The given melody should be a list of intervals in the form of strings. Make sure your input and your settings match, e.g. if you have quality turned on in your settings, make sure to include that in your given melody.

The given percentage is just a given number, e.g. 100 or 23.563. The function will match to a motif if its intervalic content is at least that percent similarity. It also matches only to the same positions in the melody.

The function then only returns an int of how many matched melodies were found in the piece. The idea of this is to be able to find if the piece is based on any preexisting melodies. Our test-set pieces, for example, used popular chanson melodies, so this makes it easier to search for them.

####transformations.py

Includes the functions `find_transform()` and `count_transform()`.

`find_transform()` takes as input a dictionary of motifs and their frequency (the output of `motivic_count()`). It finds the transformations (inversion, retrograde and retrograde inversion) of each of the motifs and their frequency in the piece. The output is a dictionary of motifs, with lists of frequencies as values. These lists are in the form of `[prime, inversion, retrograde, retrograde inversion]`.

`count_transform()` takes the output of `find_transform()` and collapses all the values. Essentially, it counts the total number of prime form motifs there are, the total number of inversion etc in the entire piece. As output it gives a single list of four numbers, in the same form as is given as input. This can be useful in comparing pieces to each other, because you can see right away if there are major differences in the composers' use of transformations.

####permutations.py

Includes `find_permutations()`, which, similarly to `find_transform()`, takes a dictionary of motifs, finds and counts all the permutations. This one, however, since there can be so many permutations, just adds up all the occurrences of any permutation and puts them in the list with the original motif form. The output is a dictionary of motifs with lists as values in the form of `[original motif, all permutations]`.

####features.py

Features are functions that can be used for anything. 

`frequency()` takes as input a dictionary of frequencies, like the output of `motivic_count()` and `ngram_count()` and outputs a dictionary of the frequencies of each of the frequencies. For example, if you give it a dictionary of motifs, it will give you a dictionary that will tell you that there are 5 different motifs that appear 7 times each. While it is meant for frequency, this does work with any kind of dictionary value.

`write_file()` will take dictionaries or lists as input and write them to a csv file. You can give it a document name, as well as a list of any column labels you might want.

`plot_graph()` also takes dictionaries/lists and labels as input and plots them as best as it can. This tends to work best, however, if your lists or dictionaries are sorted before doing this.

`deviation()` takes a list of lists of numbers and expresses each number as a percentage of the sum of the list it's in. Then, it finds the average percentage of that number and the standard deviation. The output is in the form of a list of two lists: `[average_list, standard_dev_list]`.

An example of when this would be useful is if you find the transformations of motifs in a piece, and then do the `count_transform()` method on it. Then, if you do this to 20 pieces, and put the results in a list, you could pass it to this method. Your output would be the average percentage of the prime form, the inversion, the retrograde and the retrograde inversion in that group of pieces, and the standard deviation for each one.

####nodes.py

This is mostly still a work in progress, but basically the functions in here build network graphs using pygraphviz. There are a few different options, however, depending on what exactly you want to graph.

`parts()` is a function that takes a piece and a title and outputs one graph for each part in the piece. Each graph shows the frequency of pitches, how the pitches are connected and how frequently.

`whole_piece()` also takes a piece, but outputs all the parts in one graph. They are somewhat separated, though, because it gives each part a different node color, and the shared nodes another color.

`v_notes()` plots a graph of a piece by its vertical sonorities by pitches. Duplicate notes are removed and the lists are put into alphabetical order for better comparisons.

`vertical()` takes a piece and a pair of voices (by their numbers, e.g. `['0', '2']`) and plots a graph of the intervals between those two parts. This way you can easily see the relationship between, for example, the soprano and tenor parts.

####example_comparison.py

This is a sample file that shows some possible uses for each function. There is more documentation in the comments here about input and output and settings.