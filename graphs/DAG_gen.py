import graphical_models as gm
import networkx as nx
import numpy as np
from itertools import combinations
import random

def random_graph(nnodes, density=.2):
    """
    random erdos-renyi graph
    """
    return gm.rand.directed_erdos(nnodes, density)


def line_graph(nnodes):
    """
    random line graph
    """
    dag = gm.DAG(set(range(nnodes)))

    perm = np.random.permutation(nnodes)
    orient = np.random.randint(0, 2, nnodes-1)
    dag.add_arcs_from(((perm[i], perm[i+1]), (perm[i+1], perm[i]))[orient[i]] for i in range(nnodes-1))
    
    return dag


def tree_graph(nnodes):
    """
    random tree graph
    """
    dag = gm.DAG(set(range(nnodes)))

    tree = nx.random_tree(nnodes)
    queue = [0]
    while queue:
        current_node = queue.pop()
        nbrs = list(tree.neighbors(current_node))
        nbr_size = len(nbrs)
        orient = np.random.randint(0, 2, nbr_size)
        dag.add_arcs_from(((current_node, nbrs[i]), (nbrs[i], current_node))[orient[i]] for i in range(nbr_size))
        queue += nbrs
        tree.remove_node(current_node)

    return dag


def complete_graph(nnodes):
    """
    complete graph
    """
    dag = gm.DAG(set(range(nnodes)))

    perm = np.random.permutation(nnodes)
    for (i,j) in combinations(perm, 2):
        dag.add_arc(i,j)
    
    return dag


def shanmugam_random_chordal(nnodes, density=.2):
    """
    random chordal graph with no v-structure
    """
    while True:
        d = nx.DiGraph()
        d.add_nodes_from(set(range(nnodes)))
        order = list(range(1, nnodes))
        for i in order:
            num_parents_i = max(1, np.random.binomial(i, density))
            parents_i = random.sample(list(range(i)), num_parents_i)
            d.add_edges_from({(p, i) for p in parents_i})
        for i in reversed(order):
            for j, k in combinations(d.predecessors(i), 2):
                d.add_edge(min(j, k), max(j, k))

        perm = np.random.permutation(list(range(nnodes)))
        d = nx.relabel.relabel_nodes(d, dict(enumerate(perm)))

        return gm.DAG.from_nx(d)


def random_directed_tree(nnodes):
    """
    random tree with no v-structure
    """
    g = nx.random_tree(nnodes)
    root = random.randint(0, nnodes-1)
    d = nx.DiGraph()

    queue = [root]
    while queue:
        current_node = queue.pop()
        nbrs = list(g.neighbors(current_node))
        d.add_edges_from([(current_node, nbr) for nbr in nbrs])
        queue += nbrs
        g.remove_node(current_node)
    return gm.DAG.from_nx(d)


def tree_of_cliques(nnodes, degree=3, min_clique_size=3, max_clique_size=5):
    """
    random tree of cliques with no v-structure
    """
    counter = random.randint(min_clique_size, max_clique_size)
    source_clique = list(range(counter))
    previous_layer_cliques = [source_clique]
    current_layer_cliques = []
    arcs = set(combinations(source_clique, 2))

    while counter < nnodes:
        for parent_clique in previous_layer_cliques:
            for d in range(degree):
                if counter < nnodes:
                    clique_size = random.randint(min_clique_size, max_clique_size)
                    intersection_size = min(len(parent_clique)-1, random.randint(int(clique_size/2), clique_size-1))
                    num_new_nodes = clique_size - intersection_size

                    indices = set(random.sample(parent_clique, intersection_size))
                    intersection = [
                        parent_clique[ix] for ix in range(len(parent_clique))
                        if ix in indices
                    ]
                    new_clique = intersection + list(range(counter, counter+num_new_nodes))
                    current_layer_cliques.append(new_clique)
                    arcs.update(set(combinations(new_clique, 2)))
                    counter += num_new_nodes
        previous_layer_cliques = current_layer_cliques.copy()
    g = nx.DiGraph()
    g.add_edges_from(arcs)
    # if not nx.is_connected(g.to_undirected()):
        # raise RuntimeError
    return gm.DAG.from_nx(g)


def barabasi_albert_graph(nnodes, m=2):
    """
    barabasi albert graph with random orientaions
    """
    g = nx.barabasi_albert_graph(nnodes, m)

    dag = gm.DAG(set(range(nnodes)))
    perm = np.random.permutation(nnodes)
    for (i,j) in g.edges:
        if perm[i] < perm[j]:
            dag.add_arc(i,j)
        else:
            dag.add_arc(j,i)

    return dag
