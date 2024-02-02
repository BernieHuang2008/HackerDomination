FROM ubuntu:latest

# Create users
RUN useradd -ms /bin/bash guest \
    && useradd -ms /bin/bash PLee \
    && echo 'PLee:plee666@unbreakable' | chpasswd

# Root password
ARG ROOT_PASSWORD
RUN echo "root:THISISROOTPASSWORDANDITISSECRETDONOTTRYTOUSEITBECAUSEIWANTYOUTOBEHONEST" | chpasswd

COPY ./files /


