#!/bin/bash
git pull

source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition_cuda

python evaluation_local.py --my_ai rl --opponent random --episode=100 --map=all --gui false --repeat 0 --diff-strategy