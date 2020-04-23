FROM centos

RUN mkdir -p /usr/local/hasker \
    && yum -y install make

WORKDIR /usr/local/hasker

EXPOSE 8000

