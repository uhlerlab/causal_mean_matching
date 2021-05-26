from graphs import mean_match
import random

def oracle_policy(p: mean_match, sparse: int) -> list:
    """
    knows the underlying graph
    if upstream_most:
        pick upstream_most
    else:
        solved
    """
    # for i in p.DAG.nodes:
    #     for _,j in p.DAG.outgoing_arcs(i):
    #         if p.ess_graph.has_edge(i,j):
    #             p.ess_graph.add_known_arc(i,j)
    # print(p.ess_graph.edges)
    # print(p.ess_graph.arcs)

    p.ess_graph = p.DAG.interventional_cpdag([{i} for i in p.DAG.nodes], cpdag=p.DAG.cpdag())
    int_list = []

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

