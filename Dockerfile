# ubuntu 베이스 이미지 사용
FROM da864268/my-ubuntu:22.04

LABEL maintainer="da864268@naver.com"
LABEL description="Competition"

# bash 로 변경
SHELL ["/bin/bash", "-c"]

# 패키지 설치 
RUN apt update && apt upgrade -y && apt install \
libgl1 libglib2.0-0 -y

# CUDA ToolKit 설치
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb && \
dpkg -i cuda-keyring_1.0-1_all.deb && \
apt-get update && \
apt-get install cuda-toolkit-12.1 -y && \
rm -rf cuda-keyring_1.0-1_all.deb

# CUDA Toolkit 환경변수 설정
ENV PATH "/usr/local/cuda/bin:$PATH"
ENV LD_LIBRARY_PATH "/usr/local/cuda/lib64:$LD_LIBRARY_PATH"

WORKDIR "/root/"

#Conda 설치
RUN mkdir -p ~/miniconda3 && \
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -i).sh -O ~/miniconda3/miniconda.sh && \
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
rm -rf ~/miniconda3/miniconda.sh
ENV PATH "/root/miniconda3/bin:$PATH"
RUN conda init && source ~/.bashrc

# Competition_Olympics-Running clone
RUN git clone https://github.com/Lseoksee/Competition_Olympics-Running.git
WORKDIR "/root/Competition_Olympics-Running"

# conda 가상환경 만들고 활성화
RUN conda env create -f environment.yml && \
source ~/miniconda3/etc/profile.d/conda.sh && \
conda activate competition_cuda

# 컨테이너 시작 스크립트
CMD git pull; \
source ~/miniconda3/etc/profile.d/conda.sh \
conda activate competition_cuda \
python evaluation_local.py $python_args