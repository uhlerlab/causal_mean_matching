from graphs import mean_match
import random
import graphical_models as gm
import networkx as nx
from networkx.algorithms.tree.decomposition import junction_tree
from networkx.algorithms.components.connected import connected_components


def clique_tree_policy(p: mean_match, sparse: int, central: bool=True) -> list:
    """
    if upstream_most:
        pick upstream_most
    else:
        find clique trees
        central=True: pick central minimal separators
        central=False: pick union of minimal separators
    """

    int_list = []

    while not p.solved:
        upstream_most, partial_upstream_most = p.remained_upstream_most
        if upstream_most:
            size = min(sparse, len(upstream_most))
            targets = set(random.sample(upstream_most, size))    
        elif partial_upstream_most:
            size = min(sparse, len(partial_upstream_most))
            targets = set()

            top_chain_components = p.DAG.induced_subgraph(partial_upstream_most)
            assert not top_chain_components.arcs.intersection(p.ess_graph.arcs), "top chain components should be undirected!"

            ucg, top_join_forests = join_forest(top_chain_components)
            top_trees = sorted(connected_components(top_join_forests), key=len)
            
            while size>0 and top_trees:
                tree_nodes = top_trees.pop()
                sep = central_sep(top_join_forests.subgraph(tree_nodes), size, ucg)
                if sep:
                    if len(sep)<= size:
                        targets = targets.union(sep)
                        size -= len(sep)
                    else:
                        targets = targets.union(random.sample(sep, size))
                        size = 0

            if size:
                add_targets = random.sample(partial_upstream_most-targets, size)
                targets = targets.union(add_targets)
        else:
            print("Error: p should be solved!")
        
        p.intervene(targets)
        int_list.append(targets)
    
    return int_list


def join_forest(dag: gm.DAG):
    """
    return the undirected graph 
    and the bipartite-formed clique tree/forest of a chordal graph
    """

    ucg = nx.Graph()
    ucg.add_nodes_from(dag.nodes)
    ucg.add_edges_from(dag.arcs)

    join_forest = junction_tree(ucg)

    return ucg, join_forest


def central_sep(tree: nx.Graph, sparse: int, ucg:nx.Graph):
    """
    return the most central separator that does not exceed sparsity constraint in a clique tree
    """

    potential_seps = []
    all_nodes = set()

    for node in tree.nodes(data='type'):
        if node[1] == 'sepset' and len(node[0]) <= sparse:
            potential_seps.append(node[0])
            for sep in potential_seps:
                if set(node[0])!=set(sep):
                    if set(node[0]).issubset(set(sep)):
                        potential_seps.remove(node[0])
                        break
                    elif set(sep).issubset(set(node[0])):
                        potential_seps.remove(sep)
            
        elif node[1] == 'clique':
            all_nodes = all_nodes.union(node[0])

    if not potential_seps and len(all_nodes) <= sparse:
        return all_nodes

    best_sep = None
    best_score = len(all_nodes)
    subucg = ucg.subgraph(all_nodes)
    
    for sep in potential_seps:
        tmp = subucg.copy()
        tmp.remove_nodes_from(sep)
        score = len(max(connected_components(tmp), key=len))
        if score < best_score:
            best_sep = sep
            best_score = score
    
    return best_sep

