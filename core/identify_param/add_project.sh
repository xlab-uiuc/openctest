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
    cd $home_dir/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common
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

function setup_hive(){
    [ ! -d "app/ctest-hive" ] && git clone https://github.com/lilacyl/hive.git app/ctest-hive
    cd app/ctest-hive
    git fetch && git checkout ctest-logging
    cd common
    mvn clean install -DskipTests
}

function setup_nifi(){
    [ ! -d "app/ctest-nifi" ] && git clone https://github.com/lilacyl/nifi.git app/ctest-nifi
    cd app/ctest-nifi
    git fetch && git checkout ctest-logging
    mvn clean install -pl nifi-commons/ -DskipTest

}

function setup_flink() {
    [ ! -d "app/ctest-flink" ] && git clone https://github.com/jessicahuang523/flink.git app/ctest-flink
    cd app/ctest-flink
    git fetch && git checkout ctest-get-set
    cd flink-core
}

function setup_camel() {
    [ ! -d "app/ctest-camel" ] && git clone https://github.com/wenhsinghuang/camel.git app/ctest-camel
    cd app/ctest-camel
    git fetch && git checkout ctest-injection
    mvn clean install -DskipTests
}

function setup_kylin(){
  [ ! -d "app/ctest-kylin" ] && git clone https://github.com/rtao6/kylin.git app/ctest-kylin
  cd app/ctest-kylin
  git fetch && git checkout ctest-logging
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
            hive) setup_hive ;;
            nifi) setup_nifi ;;
            flink) setup_flink ;;
            camel) setup_camel;;
            kylin) setup_kylin ;;
            *) echo "Unexpected project: $project - only support hadoop, hbase, zookeeper, hive, alluxio, nifi, flink, kylin and camel." ;;
        esac
    fi
}

main
