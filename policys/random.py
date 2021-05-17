from graphs import mean_match
import random

def random_policy(p: mean_match, sparse: int) -> list:
    """
    if upstream_most:
        pick upstream_most
    else:
        randomly pick from partial_upstream_most
    """

    int_list = []

    while not p.solved:
        upstream_most, partial_upstream_most = p.remained_upstream_most
        
        if upstream_most:
            size = min(sparse, len(upstream_most))
            targets = set(random.sample(upstream_most, size))
        elif partial_upstream_most:
            size = min(sparse, len(partial_upstream_most))
            targets = set(random.sample(partial_upstream_most, size))
        else:
            print("Error: p should be solved!")

        p.intervene(targets)
        int_list.append(targets)
    
    return int_list

