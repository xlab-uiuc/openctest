#!/usr/bin/python3
import sys, json

def main(argv):
    mapping = json.load(open("../../data/ctest_mapping/opensource-zookeeper-server.json"))
    count = 0
    for key, value in mapping.items():
        if argv[1] in value:
            count += 1
            print("p", count," ", key, sep='')
    print("Number of parameter(s) is", count)

if __name__ == "__main__":
    main(sys.argv)   