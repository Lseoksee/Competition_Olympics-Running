#!/bin/bash

#INFO: 모델 학습을 시키는 스크립트임
source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition_cuda

python rl_trainer/main.py --algo=ppo --map=all --gui false --train --max_episodes 1500