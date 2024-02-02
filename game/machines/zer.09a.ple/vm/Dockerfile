FROM ubuntu:latest

# Init users
RUN echo "root:plee666@unbreakable" | chpasswd \
    && useradd -ms /bin/bash guest \
    && useradd -ms /bin/bash PLee && adduser PLee sudo \
    && echo 'guest:guest' | chpasswd\
    && echo 'PLee:plee666@unbreakable' | chpasswd

# Install & Config SSH Server
RUN apt-get update && apt-get install -y openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config \
    && echo 'AllowUsers guest PLee' >> /etc/ssh/sshd_config

# Init files
COPY ./files /

EXPOSE 22

# Start the game
CMD ["/usr/sbin/sshd","-D"]
