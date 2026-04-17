# Dockerfile for Paper2ARM Hackathon - Q6: Anion Optimization
# Nature Materials 22, 1507-1514 (2023)
# Compatible with DeployMaster (no COPY/ADD instructions)

FROM registry.dp.tech/dptech/ubuntu:20.04-py3.10

# 设置国内镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    openssh-server \
    supervisor \
    net-tools \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 设置pip国内镜像
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装Python依赖
RUN pip install --no-cache-dir \
    numpy==1.24.3 \
    pandas==2.0.3 \
    matplotlib==3.7.2 \
    scikit-learn==1.3.0 \
    seaborn==0.12.2

# 创建工作目录
WORKDIR /workspace

# 设置环境变量
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# 默认命令
CMD ["python", "-c", "print('Environment ready for Paper2ARM Hackathon Q6')"]
