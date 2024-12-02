# cuda 12.1 이미지 베이스
FROM da864268/conda:ubuntu-22.04-cuda12.1

LABEL maintainer="da864268@naver.com"
LABEL description="Competition"

# bash 로 변경
SHELL ["/bin/bash", "-c"]

WORKDIR "/root/"

# Competition_Olympics-Running clone
RUN git clone https://github.com/Lseoksee/Competition_Olympics-Running.git
WORKDIR "/root/Competition_Olympics-Running"

# conda 가상환경 만들고 활성화
RUN conda env create -f environment.yml && \
source ~/miniconda3/etc/profile.d/conda.sh && \
conda activate competition_cuda

# python docker logs 출력대응
ENV PYTHONUNBUFFERED 1

# 컨테이너 시작시 start.sh 파일 실행
CMD ["/bin/bash", "start.sh"]