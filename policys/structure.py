from graphs import mean_match
import random
import networkx as nx
from causaldag import DAG


def structure_policy(p: mean_match, sparse: int) -> list:
    """
    lean the underlying graph first by coloring
    if upstream_most:
        pick upstream_most
    else:
        solved
    """
    int_list = coloring_policy(p.DAG, sparse)
    p.ess_graph = p.DAG.interventional_cpdag([{i} for i in p.DAG.nodes], cpdag=p.DAG.cpdag())    

    while not p.solved:
        upstream_most, _ = p.remained_upstream_most
        
        if upstream_most:
            size = min(sparse, len(upstream_most))
            targets = set(random.sample(upstream_most, size))
        else:
            print("Error: p should be solved!")

        p.intervene(targets)
        int_list.append(targets)
    
    return int_list


# following adapted from dct_policy
def induced_forest(graph: nx.Graph, coloring: dict, color1, color2):
    """
    Return the forest induced by taking only nodes of `color1` and `color2` from `coloring`.
    """
    forest = nx.Graph()
    forest.add_nodes_from(graph.nodes)
    forest.add_edges_from({(i, j) for i, j in graph.edges if {coloring[i], coloring[j]} == {color1, color2}})
    return forest


def worst_case_subtree(tree: nx.Graph, roots) -> set:
    if tree.number_of_nodes() == 1:
        return set()
    tree_ = tree.copy()
    tree_.remove_nodes_from(roots)
    subtrees = nx.connected_components(tree_)
    return max(subtrees, key=lambda t: len(t))


def score_color(graph: nx.Graph, coloring: dict, color0):
    colors = set(coloring.values())
    forests = [induced_forest(graph, coloring, color0, color) for color in colors if color != color0]
    vs = [v for v in graph.nodes if coloring[v]==color0]
    trees_containing_color = [forest.subgraph(set.union(*[nx.node_connected_component(forest, v) for v in vs])) for forest in forests]
    wc_subtrees = [worst_case_subtree(tree, set(vs)) for tree in trees_containing_color]
    wc_edges_learned = [
        tree.number_of_nodes() - len(wc_subtree)
        for tree, wc_subtree in zip(trees_containing_color, wc_subtrees)
    ]
    return sum(wc_edges_learned)


def pick_coloring_policy_color(graph: nx.Graph):
    coloring = nx.greedy_color(graph)
    color_scores = {color: score_color(graph, coloring, color) for color in coloring.values()}
    color = max(color_scores.keys(), key=lambda k: color_scores[k])
    return set([v for v in graph.nodes if coloring[v]==color])


def coloring_policy(dag: DAG, sparse: int):
    int_list = []

    current_cpdag = dag.cpdag()
    while current_cpdag.num_arcs != dag.num_arcs:
        undirected_portions = current_cpdag.copy()
        undirected_portions.remove_all_arcs()
        undirected_portions = undirected_portions.to_nx()

        color = pick_coloring_policy_color(undirected_portions)
        nodes = set(random.sample(color, min(sparse, len(color))))
        int_list.append(nodes)
        current_cpdag = current_cpdag.interventional_cpdag(dag, nodes)
    return int_list
