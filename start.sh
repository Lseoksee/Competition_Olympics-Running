#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition

python evaluation_local.py --my_ai rl --opponent random --episode=100 --map=all