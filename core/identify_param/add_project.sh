#!/bin/bash

function setup_hadoop() {
    [ ! -d "app/ctest-hadoop" ] && git clone https://github.com/xlab-uiuc/hadoop.git app/ctest-hadoop
    cd app/ctest-hadoop
    git fetch && git checkout ctest-logging
    home_dir=$PWD
    cd $home_dir/hadoop-common-project/hadoop-common
    mvn clean install -DskipTests
    cd $home_dir/hadoop-hdfs-project/hadoop-hdfs-client
    mvn clean install -DskipTests
    cd $home_dir/hadoop-hdfs-project/hadoop-hdfs
    mvn package -DskipTests
}

function setup_hbase() {
    old_dir=$PWD
    [ ! -d "app/ctest-hadoop" ] && git clone https://github.com/xlab-uiuc/hadoop.git app/ctest-hadoop
    cd app/ctest-hadoop
    git fetch && git checkout ctest-logging
    cd hadoop-common-project/hadoop-common
    mvn clean install -DskipTests
    cd $old_dir

    [ ! -d "app/ctest-hbase" ] && git clone https://github.com/xlab-uiuc/hbase.git app/ctest-hbase
    cd app/ctest-hbase
    git fetch && git checkout ctest-logging
    home_dir=$PWD
    cd $home_dir/hbase-common
    mvn clean install -DskipTests
    cd $home_dir/hbase-server
    mvn package -DskipTests
}

function setup_zookeeper() {
    [ ! -d "app/ctest-zookeeper" ] && git clone https://github.com/xlab-uiuc/zookeeper.git app/ctest-zookeeper
    cd app/ctest-zookeeper
    git fetch && git checkout ctest-logging
    mvn clean package -DskipTests
}

function setup_alluxio() {
    [ ! -d "app/ctest-alluxio" ] && git clone https://github.com/xlab-uiuc/alluxio.git app/ctest-alluxio
    cd app/ctest-alluxio
    git fetch && git checkout ctest-logging
    cd core
    mvn clean install -DskipTests -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true
}

function setup_rocketmq() {
    [ ! -d "app/ctest-rocketmq" ] && git clone https://github.com/Stranger3333/rocketmq.git app/ctest-rocketmq
    cd app/ctest-rocketmq
    git fetch && git checkout ctest-intercept
    cd acl
    mvn clean install -DskipTests -Dcheckstyle.skip -Dlicense.skip -Dfindbugs.skip -Dmaven.javadoc.skip=true
}

function usage() {
    echo "Usage: add_project.sh <main project>"
    exit 1
}

project=$1
function main() {
    if [ -z $project ]
    then
        usage
    else
        case $project in
            hadoop) setup_hadoop ;;
            hbase) setup_hbase ;;
            zookeeper) setup_zookeeper ;;
            alluxio) setup_alluxio ;;
            rocketmq) setup_alluxio ;;
            *) echo "Unexpected project: $project - only support hadoop, hbase, zookeeper and alluxio, rocketmq." ;;
        esac
    fi
}

main
