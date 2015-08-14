import matplotlib.pyplot as plt
import csv
import numpy


# counts frequency of events in a dictionary; returns dictionary of frequencies
def frequency(dictionary):

    freq = dict()

    for each in dictionary:
        if dictionary[each] in freq:
            freq[dictionary[each]] += 1
        else:
            freq[dictionary[each]] = 1

    return freq


# function that writes dictionaries or lists to a file
def write_file(my_input, name, labels):

    with open('output/' + name + '.csv', 'wb') as output:
        writer = csv.writer(output)

        writer.writerow(labels)

        if type(my_input) is dict:
            key = my_input.keys()
            value = my_input.values()

            for i in range(0, len(my_input)-1, 1):
                my_row = [key[i]]
                my_row.extend(value[i])
                writer.writerow(my_row)

        elif type(my_input) is list:
            rows = zip(*my_input)
            for row in rows:
                writer.writerow(row)


# plots graph from lists or dictionaries
def plot_graph(my_input, title, xlabel, ylabel):

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    x = 0

    if type(my_input) is list:
        for n in range(len(my_input), 0, -2):

            my_input.insert(n, colors[x])
            x += 1

        plt.plot(*my_input)

    elif type(my_input) is dict:

        my_keys = list(my_input)
        my_keys.sort()
        my_val = [my_input[each] for each in my_keys]

        plt.plot(my_keys, my_val)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def deviation(all_nums):

    final = []
    the_sum = []

    for nums in all_nums:
        total = sum(nums)
        percentages = []

        for each in nums:
            perc = float(each)/total * 100
            percentages.append(perc)

        the_sum.append(percentages)

    arr = numpy.array(the_sum)
    ave = numpy.mean(arr, axis=0)
    std = numpy.std(arr, axis=0)

    ave_list = []
    std_list = []

    for i in range(len(ave)):
        ave_list.append(ave[i])
        std_list.append(std[i])

    final.append(ave_list)
    final.append(std_list)
    return final