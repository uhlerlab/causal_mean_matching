import os
import pickle
import argparse
from tqdm import tqdm

from graphs import mean_match


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--sampler", type=str, help="type of dag sampler")
    parser.add_argument("--nnodes", type=int, help="number of nodes in each dag")
    parser.add_argument("--sparse", type=int, help="size of intervention")
    parser.add_argument("--dataset_size", type=int, help="dataset size")
    parser.add_argument("--data_dir", type=str, default="./data", help="directory to save problems")

    opts = parser.parse_args()
    
    opts.sparse = min(opts.sparse, opts.nnodes)
    
    file_dir = os.path.join(opts.data_dir, opts.sampler)
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)

    problems = []
    for i in tqdm(range(opts.dataset_size)):
        P = mean_match(opts.nnodes, opts.sampler, opts.sparse)
        problems.append(P)
        
    filename = os.path.join(file_dir, 'nodes{}_int{}.pkl'.format(opts.nnodes, opts.sparse))
    with open(filename, 'wb') as f:
        pickle.dump(problems, f, pickle.HIGHEST_PROTOCOL)
