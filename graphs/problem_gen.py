import numpy as np
from .DAG_gen import *


class mean_match(object):
    
    def __init__(self, nnodes, sampler = 'random', sparse = 10):   

        type_graph = {
            'random': random_graph,
            'line': line_graph,
            'tree': tree_graph,
            'complete': complete_graph,
            'shanmugam': shanmugam_random_chordal,
            'd_tree': random_directed_tree,
            'clique_tree': tree_of_cliques,
            'barbasi_albert': barabasi_albert_graph
            }.get(sampler, None)
        assert type_graph, "unsupported sampler!"
        self.DAG = type_graph(nnodes)

        assert nnodes >= sparse, "intervention size exceeds graph size!"
        self.intervention = set(np.random.permutation(nnodes)[0:sparse])

        self.solved_intervention = None
        self.ess_graph = None
        self.reset()


    @property
    def remained_changed_nodes(self):
        remained_nodes = set()
        for i in self.intervention:
            if i not in self.solved_intervention:
                remained_nodes.add(i)
                des_i = self.DAG.descendants_of(i)
                remained_nodes = remained_nodes.union(des_i)
        return remained_nodes

    @property
    def remained_upstream_most(self):
        remained_nodes = self.remained_changed_nodes
    
        upstream_most = set()
        partial_upstream_most = set()
        for i in remained_nodes:
            remained_nbrs = self.DAG.neighbors_of(i).intersection(remained_nodes)
            up = True
            partial_up = True
            for j in remained_nbrs:
                if (j,i) in self.ess_graph.arcs:
                    up = False
                    partial_up = False
                elif {i,j} in self.ess_graph.edges:
                    up = False
            if up:
                upstream_most.add(i)
            elif partial_up:
                partial_upstream_most.add(i)  
        
        return upstream_most, partial_upstream_most


    @property
    def solved(self):
        if self.solved_intervention == self.intervention:
            return(True)
        else:
            return(False)

    
    def intervene(self, targets):
        targets_upstream_most = self.DAG.upstream_most(targets)
        self.ess_graph = self.DAG.interventional_cpdag([targets, targets_upstream_most], cpdag=self.ess_graph)

        if targets.issubset(self.intervention):
            ans_targets = self.DAG.ancestors_of(targets).intersection(self.intervention)
            if ans_targets.issubset(self.solved_intervention):
                self.solved_intervention = self.solved_intervention.union(targets)
                #print("current discovered targets: {}".format(self.solved_intervention))

    
    def reset(self):
        self.solved_intervention = set()
        changed_nodes = self.remained_changed_nodes
        self.ess_graph = self.DAG.interventional_cpdag([changed_nodes], cpdag=self.DAG.cpdag())




        








        

