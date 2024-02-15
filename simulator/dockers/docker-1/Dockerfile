FROM ubuntu:latest

# Update apt sources
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

# Instal basic packages
RUN apt-get update \
    && apt-get install -y sudo \
    && apt install -y gcc g++

# SSH Server
RUN apt-get install -y openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config \
    && mkdir /run/sshd

EXPOSE 22

# Start the game
CMD ["/usr/sbin/sshd","-D"]
