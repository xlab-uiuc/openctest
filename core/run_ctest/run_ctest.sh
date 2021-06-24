#!/bin/bash

# please specify data input in program_input.py before running this script

ctestname=$1
function main() {
    if [ -z $ctestname ]
    then 
        python3 main.py 
    else
        python3 main.py $ctestname
    fi
}

main
