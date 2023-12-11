#!/bin/bash

# set up env for Linux ubuntu
sudo apt-get install openjdk-8-jdk
sudo apt-get install openjdk-11-jdk
sudo update-alternatives --config java
sudo apt-get install maven
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
