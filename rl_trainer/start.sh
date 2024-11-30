#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition_cuda

python main.py --load_model --algo=ppo --map=4 --load_run=4 --load_episode=1500