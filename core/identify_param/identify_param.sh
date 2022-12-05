#!/bin/bash

function usage() {
  echo "Usage: identify_param.sh project"
  exit 1
}

function setup_netty_udt() {
    [ ! -d "app/ctest-netty-udt" ] && git clone https://github.com/HongxuMeng/netty.git app/ctest-netty-udt
    cd app/ctest-netty-udt
    git fetch && git checkout ctest-logging
    home_dir=$PWD
    cd $home_dir/transport-udt
    mvn clean install -DskipTests
}

project=$1
function main() {
    if [ -z $project ]
    then
      usage
    else
        case $project in
            hadoop-common | hadoop-hdfs | hbase-server | zookeeper-server | alluxio-core | netty-transport-udt) python3 runner.py $project; python3 collector.py $project ;;
            -h | --help) usage ;;
            *) echo "Unexpected project: $project - only support hadoop-common, hadoop-hdfs, hbase-server, zookeeper-server, alluxio-core and netty-transport-udt." ;;
        esac
    fi
}

main