#!/bin/bash 

conda activate cellrepro

for sampler in 'complete' 'shanmugan'
do
    for nnodes in 10 100 1000 10000
    do
        for sparse in 1 5 10 25 50 100
        do
            python generate.py --sampler $sampler --nnodes $nnodes --sparse $sparse --dataset_size 10000
        done
    done
done

conda deactivate
