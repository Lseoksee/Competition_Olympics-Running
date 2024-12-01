import re
import numpy as np
import torch
import random
from agents.rl.submission import agent as rl_agent
from constants import DEVICE, MAP_STRATEGY, STRATEGY
from env.chooseenv import make
from tabulate import tabulate
import argparse
from torch.distributions import Categorical
import os
from datetime import datetime

from env.olympics_running import OlympicsRunning
from utils.utills import Log


def get_join_actions(state, algo_list, strategy_list: dict[int, list[int]]):
    joint_actions = []

    for agent_idx in range(len(algo_list)):
        if algo_list[agent_idx] == "random":
            driving_force = random.uniform(-100, 200)
            turing_angle = random.uniform(-30, 30)
            joint_actions.append([[driving_force], [turing_angle]])

        elif algo_list[agent_idx] == "rl":
            # INFO: 이게 아마 환경 데이터
            obs = state[agent_idx]["obs"].flatten()
            actions_raw = int(rl_agent.choose_action(obs))
            actions = strategy_list[actions_raw]
            joint_actions.append([[actions[0]], [actions[1]]])

    return joint_actions


def run_game(
    env: OlympicsRunning,
    algo_list,
    episode,
    shuffle_map,
    map_num,
    strategy: str,
    diff_strategy: bool,
    render_gui: bool,
    verbose=False,
):
    """

    Returns:
        tuple[float, float]:
            - [0]: rl 이긴 횟수
            - [1]: 평균 step 수
    """
    total_reward = np.zeros(2)
    num_win = np.zeros(3)  # agent 1 win, agent 2 win, draw
    total_steps = []  # 각 에피소드의 step 수 저장
    episode = int(episode)

    for i in range(1, int(episode) + 1):
        episode_reward = np.zeros(2)

        state, map_index = env.reset(shuffle_map)

        if strategy:
            map_strategy = STRATEGY[strategy]
        elif diff_strategy:
            Log(f"{map_index}번 맵전략: {MAP_STRATEGY[map_index]}")  # type: ignore
            map_strategy = STRATEGY[MAP_STRATEGY[map_index]]  # type: ignore
        else:
            raise Exception(
                "--diff-strategy값 또는 --strategy값을 실행 인자로 넣어주세요"
            )

        if render_gui:
            env.env_core.render()

        step = 0

        while True:
            # 메 스탭 지날때 마다 환경에서 상태 정보 갱신
            joint_action = get_join_actions(state, algo_list, map_strategy)
            # 상태에 따른 행동 선택
            next_state, reward, done, _, info = env.step(joint_action)
            reward = np.array(reward)
            episode_reward += reward

            if render_gui:
                env.env_core.render()

            step += 1  # step 증가

            if done:
                # reward[0] = random, reward[1]=rl
                if reward[0] != reward[1]:
                    if reward[0] == 100:
                        num_win[0] += 1
                    elif reward[1] == 100:
                        num_win[1] += 1
                        total_steps.append(step)  # 이긴 경우 에피소드별 step 수 저장
                        Log(f"{map_index}번 맵에서 {step}번 스탭만에 승리")
                    else:
                        raise NotImplementedError
                else:
                    num_win[2] += 1

                if not verbose:
                    if i % 100 == 0 or i == episode:
                        print()
                break
            state = next_state

        total_reward += episode_reward

    # 결과 출력
    total_reward /= episode
    average_steps = np.mean(total_steps)  # 평균 step 수 계산
    Log("total reward: ", total_reward)
    Log(f"Result in map {map_num} within {episode} episode:")

    header = ["Name", algo_list[0], algo_list[1]]
    data = [
        ["score", np.round(total_reward[0], 2), np.round(total_reward[1], 2)],
        ["win", num_win[0], num_win[1]],
        ["avg_steps", average_steps, "-"],
    ]  # 평균 step 추가
    print(tabulate(data, headers=header, tablefmt="pretty"))

    return int(num_win[1]), float(average_steps)


if __name__ == "__main__":
    is_available_cuda = False
    if torch.cuda.is_available():
        is_available_cuda = True
        print("CUDA 사용 가능")
    else:
        print("CUDA 사용 불가능")

    parser = argparse.ArgumentParser()
    parser.add_argument("--my_ai", default="rl", help="rl/random")
    parser.add_argument("--opponent", default="random", help="rl/random")
    parser.add_argument("--episode", default=20)
    parser.add_argument("--map", default="all", help="1/2/3/4/all")
    
    #INFO: constants.py 파일에 정의되어 있음
    parser.add_argument("--strategy", help="행동 전략")
    
    #INFO: constants.py 파일에 정의되어 있음
    parser.add_argument(
        "--diff-strategy", help="맵별 행동 전략 다르게 설정", action="store_true"
    )
    parser.add_argument("--gui", required=True, help="pygame gui 사용 여부")
    parser.add_argument("--repeat", default=0, help="반복 횟수 (무한=0)")
    args = parser.parse_args()

    if DEVICE == "cuda" and is_available_cuda:
        print("디바이스: CUDA")
    else:
        print("디바이스: CPU")

    env_type = "olympics-running"
    game = make(env_type, conf=None, seed=1)

    if args.map != "all":
        game.specify_a_map(int(args.map))
        shuffle = False
    else:
        shuffle = True

    agent_list = [args.opponent, args.my_ai]  # your are cojntrolling agent green

    render_gui = True if args.gui == "true" else False

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print(now.center(40, "="))
    print()

    # 최고 좋은 점수 저장
    max_repeat = {
        "repeat": 0,
        "count": 0,
        "avg": 0.0,
    }
    repeat = int(args.repeat)
    i = 1
    while True:
        # 0으로 설정되있으면 무한 반복
        if repeat != 0 and ((repeat + 1) <= i):
            break
        Log(f"{i}번째 시도")
        print()
        conut, avg = run_game(
            game,
            algo_list=agent_list,
            episode=args.episode,
            shuffle_map=shuffle,
            map_num=args.map,
            diff_strategy=args.diff_strategy,
            strategy=args.strategy,
            render_gui=render_gui,
            verbose=False,
        )

        #  최고 기록 구하기 (승리 횟수가 가장 많고 같을 경우 평균 step이 작은 것을 선택)
        if conut >= max_repeat["count"]:
            if not max_repeat["avg"] or avg < max_repeat["avg"]:
                max_repeat["repeat"] = i
                max_repeat["count"] = conut
                max_repeat["avg"] = avg

        print(
            "현재 최고기록: {}번째 시도, 승리 횟수: {}, 평균step: {}".format(
                max_repeat["repeat"], max_repeat["count"], max_repeat["avg"]
            )
        )

        print()
        i += 1
