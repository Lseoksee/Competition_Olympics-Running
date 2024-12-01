#!/bin/bash

#INFO: 모델 학습을 시키는 스크립트임
source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition_cuda

python rl_trainer/main.py --algo=ppo --map=all --gui false --train --max_episodes 1500

# 모델 체크포인트 사용 예
# python rl_trainer/main.py --algo=ppo --map=all --gui false --train --max_episodes 1500 --load_model --actor_path run4/trained_model/actor_1500.pth --critic_path run4/trained_model/critic_1500.pth