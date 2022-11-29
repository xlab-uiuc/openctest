#!/bin/bash

while getopts r: flag
do
    case "${flag}" in
        r) version=${OPTARG};;
    esac
done

if [ -z "$version" ]
then
   echo "Usage : ./add_project_skywalking.sh -r <release_version>"
   exit
fi

echo $version

rm -rf app/skywalking

mkdir -p app/skywalking

cd app/skywalking

wget https://dlcdn.apache.org/skywalking/$version/apache-skywalking-apm-$version-src.tgz

tar zxvf apache-skywalking-apm-$version-src.tgz

cd apache-skywalking-apm-$version

git apply ../../../patch/skywalking/skywalking.patch

cd oap-server

mvn clean install -DskipTests

cd ..