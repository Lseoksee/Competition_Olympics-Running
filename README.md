# Competition_Olympics-Running

-   기계학습 프로그래밍 경진 대회

## 실행

### Docker-Compose 사용

```bash
docker buildx build --load -t competition . && docker compose -p competition up -d
```

### 로컬에서 직접 테스트

> Linux 환경에서는 `start.sh` 실행하면 됨

```bash
python evaluation_local.py --my_ai rl --opponent random --episode=100 --map=all --gui false --repeat 0 --diff-strategy --load_model actor_1500.pth [...추가 옵션]
```

#### 옵션 설명

-   `--my_ai rl`: `rl` 고정 (필수)
-   `--opponent random`: `random`으로 고정
-   `--episode <에피소드 수>`: 실제 대회 진행 시 `100` 으로
-   `--load_model <모델 체크포인트 파일>`:

    -   `./agents/rl` 폴더 기준임
    -   기본 모델로 진행시: `actor_1500.pth`

-   `--gui <true|false>`: pygame GUI 사용 여부

-   **(optional)** `--map <원하는 맵|all>`:

    > default: all

    -   1~11 중 선택, 랜덤하게 하려면 해당 옵션을 쓰지 말거나, `all`로
    -   대회 진행시 `all` 로

-   **(optional)** `--strategy <전략>`

    -   agent 에 행동 전략 선택
    -   `전략`: constants.py 에 _STRATEGY_ 상수에 정의 되있는 Key값
    -   **`--diff-strategy` 옵션 사용 시 사용 하지 말것!**

-   **(optional)** `--diff-strategy`

    -   constants.py 에 _MAP_STRATEGY_ 상수에 정의된 맵 별 agent 행동 전략을 사용
    -   **`--strategy ` 옵션 사용 시 사용 하지 말것!**

-   **(optional)** `--repeat <반복 횟수>`:

    > default: 0

    -   게임 진행 횟수, 무한반복=0

## 모델 학습

> Linux 환경에서는 `start_train.sh` 실행하면 됨

```bash
python rl_trainer/main.py --map all --gui false --train --max_episodes 1500
```

### 옵션 설명

-   `--map <원하는 맵|all>`:

    -   학습할 맵
    -   모든 맵을 `max_episodes` 만큼 순회하여 학습하고 싶다면 `all` 로

-   `--gui <true|false>`: pygame GUI 사용 여부

-   **(optional)** `--train`:

    -   학습 사용 선언
    -   만약 단순히 모델 테스트만 하고 싶은 경우 해당 옵션을 쓸 필요 없음

-   **(optional)** `--max_episodes <최대 에피소드 수>`:

    > default: 1500

    -   한 맵당 학습할 에피소드 수

-   **(optional)** `--load_model`:

    -   모델 체크포인트 불러오기 허용 선언
    -   **해당 옵션을 사용하면 반드시 `--actor_path`와 `--actor_path` 옵션도 추가 해야한다**

-   **(optional)** `--actor_path <actor 체크포인트 경로>`:

    -   `actor` 모델 체크포인트 불러오기 (`--load_model` 옵션과 함깨 사용)

    -   `./rl_trainer/models/olympics-running` 폴더 기준임

-   **(optional)** `--critic_path <actor 체크포인트 경로>`:

    -   `critic` 모델 체크포인트 불러오기 (`--load_model` 옵션과 함깨 사용)

    -   `./rl_trainer/models/olympics-running` 폴더 기준임

## 참고

### CUDA 사용 여부 설정

-   `constants.py` 에서 _DEVICE_ 상수 값을 `"CUDA"` 또는 `"CPU"` 로 설정
