FROM ubuntu:latest

# Instal basic packages
RUN apt-get update && apt-get install -y sudo

# SSH Server
RUN apt-get install -y openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config \
    && mkdir /run/sshd

EXPOSE 22

# Start the game
CMD ["/usr/sbin/sshd","-D"]
