__author__ = 'mborsodi'

import music21
from vis.models.indexed_piece import IndexedPiece
from vis.analyzers.indexers import noterest, interval, offset
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pg


# finds percentage of occurrences in dictionary - so that graphs can be more
# accurately compared to each other
def _percentage(dictionary):
    values = dictionary.values()

    total = sum(values)

    new_dictionary = {}

    for key in dictionary:
        nom = dictionary[key] * 1.0
        new = (nom / total) * 100
        new_dictionary[key] = new

    return new_dictionary


# generic version of graph
def _make_graph(nodes, name):
    node_freq = {}
    gr = pg.AGraph(directed=True)
    gr.node_attr = dict(style='filled',
                        shape='circle',
                        fixedsize='true',
                        fontcolor='#000000',
                        fontsize='10.0',
                        fillcolor='coral2')
    gr.graph_attr = dict(overlap='false', size='50!')
    gr.edge_attr = dict(color='coral2')

    for node in nodes:

        if node is 'Rest':
            pass

        elif node in node_freq:
            node_freq[node] += 1

        else:
            node_freq[node] = 1

    node_perc = _percentage(node_freq)

    for node in nodes:

        if node is 'Rest':
            pass
        else:
            i = node_perc[node]
            i = ((i / 100) * 5) + 1

            gr.add_node(node)
            n = gr.get_node(node)
            n.attr['height'] = i
            n.attr['width'] = i

    edge_freq = {}

    for i in range(len(nodes) - 1):

        edge = nodes[i] + nodes[i + 1]

        if nodes[i] is 'Rest' or nodes[i + 1] is 'Rest':
            pass

        elif edge in edge_freq:
            edge_freq[edge] += 1

        else:
            edge_freq[edge] = 1

    edge_perc = _percentage(edge_freq)

    for i in range(len(nodes) - 1):

        if nodes[i] is 'Rest' or nodes[i + 1] is 'Rest':
            pass
        else:

            w = edge_perc[nodes[i] + nodes[i + 1]]
            # w = ((w/100)*20) + 0.2

            gr.add_edge(nodes[i], nodes[i + 1])
            e = gr.get_edge(nodes[i], nodes[i + 1])
            e.attr['penwidth'] = w

    gr.layout(prog='dot')

    gr.draw(name + '.png')


# builds graph of each part individually
def parts(piece, title):
    the_score = music21.converter.parse(piece)
    num_parts = len(the_score.parts)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    for i in range(num_parts):
        notes = the_notes['noterest.NoteRestIndexer'][str(i)]
        part_notes = []

        for note in notes:
            part_notes.append(str(note))

        if 'nan' in part_notes:
            while 'nan' in part_notes:
                part_notes.remove('nan')

        _make_graph(part_notes, title + '-part' + str(i))


# builds graph of all the notes in a piece
def whole_piece(piece, title):
    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    all_notes = []

    for i in range(len(the_score.parts)):

        notes = the_notes['noterest.NoteRestIndexer'][str(i)]
        part_notes = []

        for note in notes:
            note = str(note)
            if note == 'nan':
                pass
            else:
                part_notes.append(note)

        all_notes.append(part_notes)

    _multi_color(all_notes, title)


# returns list of shared values
def _compare(list_of_lists):

    shared = []

    for i in range(len(list_of_lists)):

        for x in range(i + 1, len(list_of_lists), 1):

            for the_list in list_of_lists[i]:

                if the_list in list_of_lists[x]:

                    shared.append(the_list)

    return shared


# graph with multiple parts shown in different colors
def _multi_color(nodes, name):
    gr = pg.AGraph(directed=True)

    colors = ['aquamarine3',
              'blue',
              'blueviolet',
              'brown1',
              'cadetblue3',
              'chartreuse3',
              'chocolate2',
              'coral2',
              'cornflowerblue',
              'darkgoldenrod1',
              'darkolivegreen4',
              'darkorange1',
              'darkorchid1',
              'darkseagreen',
              'deepskyblue3',
              'firebrick2',
              'gold2',
              'greenyellow']

    gr.node_attr['style'] = 'filled'
    gr.node_attr['shape'] = 'circle'
    gr.node_attr['fixedsize'] = 'true'
    gr.node_attr['fontcolor'] = '#000000'
    gr.node_attr['fontsize'] = '10.0'

    gr.graph_attr['overlap'] = 'false'

    sh = gr.add_subgraph()
    shared = _compare(nodes)
    node_freq = {}

    x = 0
    for part in nodes:
        sg = gr.add_subgraph()

        for note in part:

            if note != 'Rest':

                if note not in shared:
                    sg.add_node(note)
                    node = sg.get_node(note)
                    node.attr['fillcolor'] = colors[x]

                if note in node_freq:
                    node_freq[note] += 1

                else:
                    node_freq[note] = 1

        x += 1

    for note in shared:

        sh.add_node(note)
        node = sh.get_node(note)
        node.attr['fillcolor'] = colors[x]

    node_perc = _percentage(node_freq)

    for part in nodes:

        for note in part:

            if note != 'Rest':
                i = node_perc[note]
                i = ((i / 100) * 5) + 0.3

                gr.add_node(note)
                n = gr.get_node(note)
                n.attr['height'] = i
                n.attr['width'] = i

    edge_freq = {}

    for node in nodes:
        for i in range(len(node) - 1):

            edge = node[i] + node[i + 1]

            if 'Rest' in edge:
                pass

            elif edge in edge_freq:
                edge_freq[edge] += 1

            else:
                edge_freq[edge] = 1

        edge_perc = _percentage(edge_freq)

        for i in range(len(node) - 1):

            if node[i] is 'Rest' or node[i + 1] is 'Rest':
                pass
            else:

                w = edge_perc[node[i] + node[i + 1]]
                gr.add_edge(node[i], node[i + 1])
                e = gr.get_edge(node[i], node[i + 1])
                e.attr['penwidth'] = w

    gr.draw(name + '.png', prog='dot')


# vertical sonorities using actual pitches rather than intervals
def v_notes(piece):
    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    setts = {'quarterLength': 0.5, 'method': 'ffill'}
    off = offset.FilterByOffsetIndexer(the_notes, setts).run()

    all_notes = []

    for i in range(len(the_score.parts)):

        notes = off['offset.FilterByOffsetIndexer'][str(i)]
        part_notes = []

        for note in notes:
            note = str(note)
            if note == 'nan':
                pass
            elif note == 'Rest':
                pass
            else:
                part_notes.append(note[:-1])

        all_notes.append(part_notes)

    vert = []

    for note in zip(*all_notes):
        new = list(set(note))
        new.sort(cmp=lambda y, z: cmp(y[0], z[0]))
        new = ' '.join(new)
        vert.append(new)

    _make_graph(vert, 'vertnotes')


    # still working with networkx (needs to be changed) - build graph of the


# interval between only a pair of voices
def vertical(piece, pair, settings, title):
    ind_piece = IndexedPiece(piece)

    # get notes
    the_score = music21.converter.parse(piece)
    the_notes = noterest.NoteRestIndexer(the_score).run()

    setts = {'quarterLength': 1.0, 'method': 'ffill'}
    off = offset.FilterByOffsetIndexer(the_notes, setts).run()

    vert = interval.IntervalIndexer(off, settings).run()
    my_pair = vert['interval.IntervalIndexer', pair]

    piece_range = int(the_notes.last_valid_index())

    intervals = []

    for x in range(0, piece_range, 1):

        name = [str(my_pair.get(x))]
        new_name = []

        for note in name:
            if note == 'Rest':
                pass

            elif note not in new_name:
                new_name.append(note)

            else:
                pass

        intervals.append(new_name)

    nodes = []

    for intl in intervals:

        if not intl:
            pass

        else:
            intl = sorted(intl)
            intl = ' '.join(intl)
            nodes.append(intl)

    gr = nx.DiGraph()

    node_freq = {}
    edge_freq = {}

    for i in range(len(nodes)):

        if nodes[i] in node_freq:
            node_freq[nodes[i]] += 1

        else:
            node_freq[nodes[i]] = 1

        if i + 1 < len(nodes):
            edge = nodes[i] + ' - ' + nodes[i + 1]
            if nodes[i] == nodes[i + 1]:
                pass

            elif edge in edge_freq:
                edge_freq[edge] += 1

            else:
                edge_freq[edge] = 1

    for e in range(len(nodes) - 1):

        if 'nan' in nodes[e]:
            pass

        elif 'nan' in nodes[e + 1]:
            pass

        elif not nodes[e]:
            pass

        elif not nodes[e + 1]:
            pass

        else:
            gr.add_node(nodes[e], frequency=node_freq[nodes[e]])
            gr.add_node(nodes[e + 1], frequency=node_freq[nodes[e + 1]])

            if nodes[e] == nodes[e + 1]:
                pass
            else:
                gr.add_edge(nodes[e], nodes[e + 1])

    sizes = []

    for note in node_freq.values():
        note *= 100
        sizes.append(note)

    edges = gr.edges()

    weights = []

    for i in range(len(edges)):
        edge = edges[i]
        width = edge_freq[edge[0] + ' - ' + edge[1]]
        weights.append(width)

    nx.draw_graphviz(gr, node_size=sizes, edge_color=weights,
                     edge_cmap=plt.cm.Blues, node_color='#A0CBE2', width=4,
                     arrows=False)

    fig = plt.gcf()
    fig.set_size_inches(18.5, 13.5)
    plt.savefig('output/graphs/results/' + title + '.png', facecolor='#97b9c3',
                transparent=True)

    plt.clf()