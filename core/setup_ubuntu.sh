#!/bin/bash

function setup_j8_mvn_proto() {
    # set up env for Linux ubuntu
    sudo apt-get install openjdk-8-jdk
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
}

function setup_j11_ant() {
    # set up env for Linux ubuntu
    sudo apt-get install openjdk-11-jdk
    sudo apt-get install ant
    sudo apt-get install build-essential
}

function usage() {
    echo "Usage: setup_ubuntu.sh <main project>"
    exit 1
}

project=$1
function main() {
    if [ -z $project ]
    then
        usage
    else
        case $project in
            hadoop) setup_j8_mvn_proto ;;
            hbase) setup_j8_mvn_proto ;;
            zookeeper) setup_j8_mvn_proto ;;
            alluxio) setup_j8_mvn_proto ;;
            cassandra) setup_j11_ant ;;
            *) echo "Unexpected project: $project - only support hadoop, hbase, zookeeper, alluxio, or cassandra." ;;
        esac
    fi
}

main