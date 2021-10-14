# Causal Mean Matching
Code for paper: _Matching a Desired Causal State via Shift Interventions (NeurIPS 2021)_.

arXiv link: https://arxiv.org/abs/2107.01850

To generate a causal system along with its desired mean, run the following for example:
```
python generate.py --sampler 'barbasi_albert' --nnodes 100 --sparse 10 --dataset_size 1
```
To generate multiple instances with same parameters (e.g., number of nodes and DAG type), set `dataset_size` to be larger than 1. 



To run a policy on a .pkl file of problem instances, e.g., clique tree policy with single perturbation target interventions:
```
python test_policy.py ./data/barbasi_albert/nodes100_int10.pkl --sparse 1 --policy clique --results_dir results/barbasi_albert
```
For interventions with multiple perturbation targets, set `sparse` to be larger than 1. Supported policy: `random`, `clique`, `submodular`, `oracle`, `structure`.
