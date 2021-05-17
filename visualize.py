import networkx as nx
import graphical_models as gm
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

def draw(pdag, colored_set=set(), solved_set=set(), affected_set=set()):
    """ 
    plot a partially directed graph
    """

    p = pdag.nnodes

    nw_ax = plt.subplot2grid((4, 4), (0, 0), colspan=9, rowspan=9)

    plt.gcf().set_size_inches(4, 4)

    # directed edges
    d = nx.DiGraph()
    d.add_nodes_from(list(range(p)))
    for (i, j) in pdag.arcs:
        d.add_edge(i, j)

    # undirected edges
    e = nx.Graph()
    try:
        for pair in pdag.edges:
            (i, j) = tuple(pair)
            e.add_edge(i, j)
    except:
        print('there are no undirected edges')

    pos = nx.circular_layout(d)
    nx.draw(e, pos=pos, node_color='w', style = 'dashed', ax=nw_ax)
    color = ['w']*p
    for i in affected_set:
        color[i] = 'orange'
    for i in colored_set:
        color[i] = 'y'
    for i in solved_set:
        color[i] = 'grey'
    nx.draw(d, pos=pos, node_color=color, ax=nw_ax)
    nx.draw_networkx_labels(d, pos, labels={node: node for node in range(p)}, ax=nw_ax)

    