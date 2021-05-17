from graphs import mean_match
import random
import networkx as nx
from networkx.algorithms.components.connected import connected_components
from itertools import combinations
from .SATURATE import SATURATE

def submodular_policy(p: mean_match, sparse: int) -> list:
    """
    if upstream_most:
        pick upstream_most
    else:
        use submodular optimization
        to find the best separator set
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

            ucg = nx.Graph()
            ucg.add_nodes_from(top_chain_components.nodes)
            ucg.add_edges_from(top_chain_components.arcs)
            uccgs = sorted(connected_components(ucg), key=len, reverse=True)

            while size and uccgs:
                uccg = uccgs.pop()
                uccg = ucg.subgraph(uccg)
                sep = SATURATE(F, uccg, size)
                assert len(sep) <= size, "SATURATE should return feasible solution!"
                targets = targets.union(sep)
                size -= len(sep)
                
            if size:
                add_targets = random.sample(partial_upstream_most-targets, size)
                targets = targets.union(add_targets)
        else:
            print("Error: p should be solved!")
        
        p.intervene(targets)
        int_list.append(targets)
    
    return int_list


def F(c: int, U: set, uccg: nx.Graph) -> float:
    """
    return the average threshold function F_c(U)
    """
    f = 0  
    V = set(uccg)
    V_U = V - U

    fs = {}
    for pair in combinations(V_U, 2):
        try:
            paths = 0
            paths_through_U = 0
            for path in nx.all_simple_paths(uccg, source=pair[0], target=pair[1]):
                if set(path) & U:
                    paths_through_U += 1
                paths += 1
            f_pair = 1 - paths_through_U / paths
        except nx.exception.NetworkXNoPath:
            f_pair = 0
        fs[pair] = f_pair
    
    for i in V:
        try:
            f += max(c, sum([v for k,v in fs.items() if i in k]))
        except:
            f += c

    return f/len(V)
        

