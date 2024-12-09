# Competition_Olympics-Running

-   기계학습 프로그래밍 경진 대회

## 실행

### Docker-Compose 사용

> Docker swarm이 활성화 되야 함

```bash
# 이미지 빌드
docker buildx build --load -t competition . && \
    docker buildx prune -f --all && \
    docker rm -f buildx_buildkit_multi-arch-builder0 && \
    docker rmi moby/buildkit:buildx-stable-1

# 서비스 시작
docker stack deploy -d -c docker-compose.yml competition

# 서비스 로그보기
docker service logs -f competition_run
```

#### 컨테이너 로그 저장하기

```bash
# 실행 권한 주기
chmod +x log.sh

# ./log 폴더에 로그 파일 저장
./log.sh
```

### 로컬에서 직접 테스트

1. **Conda 가상환경 생성**

    ```bash
    conda env create -f environment.yml
    conda activate competition_cuda

    # 만약 CUDA 없으면
    conda env create -f environment_NonCuda.yml
    conda activate competition_noncuda
    ```

2. **실행**

    > Linux 환경에서는 `start.sh` 실행하면 됨

    ```bash
    python evaluation_local.py --my_ai rl --opponent random --episode 100 --map all --gui false --repeat 0 --diff-strategy
    ```

#### 옵션 설명

-   `--my_ai rl`:

    -   `rl` 고정

-   `--opponent random`

    -   `random` 고정

-   `--episode <에피소드 수>`

    -   실제 대회 진행 시 `100` 으로

-   `--gui <true|false>`

    -   pygame GUI 사용 여부

-   `--strategy <전략>`

    -   agent 에 행동 전략 선택
    -   `전략`: constants.py 에 _STRATEGY_ 상수에 정의 되있는 Key값
    -   **`--diff-strategy` 옵션 사용 시 사용 하지 말것!**

-   `--diff-strategy`

    -   constants.py 에 _MAP_STRATEGY_ 상수에 정의된 맵 별 agent 행동 전략을 사용
    -   **`--strategy ` 옵션 사용 시 사용 하지 말것!**

-   `--map <원하는 맵|all>` _(optional)_

    > default: all

    -   1~11 중 선택, 랜덤하게 하려면 해당 옵션을 쓰지 말거나, `all`로
    -   대회 진행시 `all` 로

-   `--repeat <반복 횟수>` _(optional)_

    > default: 0

    -   게임 진행 횟수, 무한반복=0

## 모델 학습

1. **Conda 가상환경 생성**

    ```bash
    conda env create -f environment.yml
    conda activate competition_cuda

    # 만약 CUDA 없으면
    conda env create -f environment_NonCuda.yml
    conda activate competition_noncuda
    ```

2. **실행**

    > Linux 환경에서는 `start_train.sh` 실행하면 됨

    ```bash
    python rl_trainer/main.py --map all --gui false --train --max_episodes 1500
    ```

### 옵션 설명

-   `--map <원하는 맵|all>`

    -   학습할 맵
    -   모든 맵을 `max_episodes` 만큼 순회하여 학습하고 싶다면 `all` 로

-   `--gui <true|false>`

    -   pygame GUI 사용 여부

-   `--train` _(optional)_

    -   학습 사용 선언
    -   만약 단순히 모델 테스트만 하고 싶은 경우 해당 옵션을 쓸 필요 없음

-   `--max_episodes <최대 에피소드 수>` _(optional)_

    > default: 1500

    -   한 맵당 학습할 에피소드 수

-   `--load_model` _(optional)_

    -   모델 체크포인트 불러오기 허용 선언
    -   **해당 옵션을 사용하면 반드시 `--actor_path`와 `--actor_path` 옵션도 추가 해야한다**

-   `--actor_path <actor 체크포인트 경로>` _(optional)_

    -   `actor` 모델 체크포인트 불러오기 (`--load_model` 옵션과 함깨 사용)
    -   `./rl_trainer/models/olympics-running` 폴더 기준임

-   `--critic_path <actor 체크포인트 경로>` _(optional)_

    -   `critic` 모델 체크포인트 불러오기 (`--load_model` 옵션과 함깨 사용)
    -   `./rl_trainer/models/olympics-running` 폴더 기준임

## 참고

### CUDA 사용 여부 설정

-   `constants.py` 에서 _DEVICE_ 상수 값을 `"CUDA"` 또는 `"CPU"` 로 설정

### Docker-Swarm 에서 GPU 사용하는법

1. GPU GUID 확인

    ```bash
    nvidia-smi -a | grep UUID
    # GPU-XXXXX
    ```

2. `/etc/docker/daemon.json` 파일 수정

    > 없으면 만듬

    ```json
    {
        "runtimes": {
            "nvidia": {
                "path": "/usr/bin/nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "default-runtime": "nvidia",
        "node-generic-resources": ["NVIDIA-GPU=<위에서 확인한 GUID"]
    }
    ```

3. `/etc/nvidia-container-runtime/config.toml`에 아래 구문 추가

    ```toml
    swarm-resource = "DOCKER_RESOURCE_GPU"
    ```

4. docker 재시작

    ```bash
    sudo systemctl restart docker
    ```
