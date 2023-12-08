FROM openjdk:8

RUN \
  apt-get update && \
  apt-get install -y software-properties-common && \
# Install Git
  apt-get install -y git && \
# Install python
  apt-get update && \
  apt-get install -y python python-dev python3-pip python3-virtualenv && \
  rm -rf /var/lib/apt/lists/* && \
# Install misc
  apt-get update && \
  apt-get install -y sudo && \
  apt-get install -y vim && \
  apt-get install -y wget && \
  apt-get install -y zip unzip

RUN \
# Install Maven and other dependencies for supported projects
  apt-get update && \
  apt-get install -y maven && \
  apt-get install -y build-essential autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev && \
# Install Protobuf
  apt-get update && \
  cd /usr/local/src/  && \
  wget https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz  && \
  tar xvf protobuf-2.5.0.tar.gz  && \
  cd protobuf-2.5.0  && \
  ./autogen.sh  && \
  ./configure --prefix=/usr  && \
  make  && \
  make install
 
RUN \
  useradd -m ctestuser

USER ctestuser
# RUN cd /home/ctestuser && \
#   git clone https://github.com/xlab-uiuc/openctest.git

WORKDIR /home/ctestuser

ENTRYPOINT ["tail", "-f", "/dev/null"]