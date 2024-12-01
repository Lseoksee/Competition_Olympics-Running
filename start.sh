#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate competition

if [ -z "$python_args" ]; then
    #python_args 환경변수가 비어있는 경우
    python evaluation_local.py --my_ai rl --opponent random --episode=100 --map=all --gui true --repeat 0 --diff-strategy
else
    #python_args 환경변수가 있는경우
    python evaluation_local.py "$python_args"
fi