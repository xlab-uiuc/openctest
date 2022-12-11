#!/bin/bash

# set up env for Linux ubuntu
sudo apt-get install openjdk-8-jdk
sudo tar xzf apache-maven-3.8.6-bin.tar.gz -C /opt 
sudo ln -s /opt/apache-maven-3.8.6 /opt/maven 
sudo apt-get install scala
# sudo nano /etc/profile.d/maven.sh
# Add the following lines to the maven.sh file:
# export JAVA_HOME=/usr/lib/jvm/default-java
# export M2_HOME=/opt/maven
# export MAVEN_HOME=/opt/maven
# export PATH=${M2_HOME}/bin:${PATH}
sudo apt-get install build-essential autoconf automake libtool cmake zlib1g-dev pkg-config libssl-dev

# install protobuf 2.5
curdir=$PWD
cd /usr/local/src/
wget https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.tar.gz
tar xvf protobuf-2.5.0.tar.gz
cd protobuf-2.5.0
./autogen.sh
./configure --prefix=/usr
make
make install
protoc --version

cd $curdir
