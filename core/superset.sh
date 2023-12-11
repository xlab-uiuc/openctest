#!/bin/bash

if [ -z "$1" ]
then
    echo "Please provide a version number as an argument."
    exit 1
fi

VERSION=$1

REPO_URL="https://github.com/apache/superset.git"

git clone $REPO_URL
cd superset
git checkout tags/$VERSION -b $VERSION-branch

cd superset-websocket

if ! command -v npm &> /dev/null
then
    echo "npm could not be found. Please install it."
    exit 1
fi

npm install

cd ..