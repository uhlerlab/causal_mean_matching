import os
import argparse
import pickle
from tqdm import tqdm

from graphs import mean_match
from policys import random_policy, clique_tree_policy, submodular_policy


def run_policy(file, policy, size, opts):
    with open(file, 'rb') as f:
        problems = pickle.load(f)

    ints = []
    for p in tqdm(problems):
        if p.DAG.nnodes <= size:
            return

        p.reset()
        int = policy(p, size)
        ints.append(len(int))


    if not os.path.isdir(opts.results_dir):
        os.makedirs(opts.results_dir)

    filename = os.path.split(file)[1]
    savename = os.path.join(opts.results_dir, "{}_size{}_{}".format(opts.policy, size, filename))
    with open(savename, 'wb') as f:
        pickle.dump(ints, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", nargs='+', help="input problem directory")
    parser.add_argument("--policy", type=str, help="intervention policy")
    parser.add_argument("--sparse", type=int, nargs='+', help="size of intervention")
    parser.add_argument("--results_dir", default='results', help="directory to save results")

    opts = parser.parse_args()

    policy = {
        'random': random_policy,
        'clique': clique_tree_policy,
        'submodular': submodular_policy
    }.get(opts.policy, None)
    assert policy is not None, "please specify a supported policy!"

    sparse = opts.sparse if opts.sparse is not None else [1]

    for size in sparse:
        for file in opts.dataset:
            run_policy(file, policy, size, opts) 
