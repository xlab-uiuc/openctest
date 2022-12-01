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

function setup_shenyu_common() {
    # /home/kejiawu2/project/openctest/core/identify_param/app/ctest-shenyu/shenyu/shenyu-common/
    [ ! -d "app/ctest-shenyu" ] && git clone https://github.com/KobeNorris/shenyu.git app/ctest-shenyu
    cd app/ctest-shenyu
    git fetch && git checkout ctest
    home_dir=$PWD
    cd $home_dir/shenyu-common/
    mvn package -DskipTests
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
            shenyu-common) setup_shenyu_common ;;
            *) echo "Unexpected project: $project - only support hadoop, hbase, zookeeper, alluxio and shenyu-common." ;;
        esac
    fi
}

main
