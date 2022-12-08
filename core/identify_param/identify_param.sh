#!/bin/bash

function usage() {
  echo "Usage: identify_param.sh project"
  exit 1
}

project=$1
function main() {
    if [ -z $project ]
    then
      usage
    else
        case $project in
            hadoop-common | hadoop-hdfs | hbase-server | zookeeper-server | alluxio-core) python3 runner.py $project; python3 collector.py $project ;;
            -h | --help) usage ;;
            *) echo "Unexpected project: $project - only support hadoop-common, hadoop-hdfs, hbase-server, zookeeper-server and alluxio-core." ;;
        esac
    fi
}

main