#!/usr/bin/python3
import sys, time

from program_input import p_input
from main import test_conf_file
from parse_input import *

project = p_input["project"]
mapping = parse_mapping(p_input["mapping_path"])
from run_test import run_test_batch

def main(argv):
    print(">>>>[ctest_core] running project {}".format(project))
    s = time.time()
    ctestname = argv[1]
    param_value_dict = {}
    for i in range(2, len(argv)):
        param, value = argv[i].split('=')
        param_value_dict[param] = value
    test_input = extract_conf_diff_from_pair(param_value_dict)
    test_conf_file(test_input, ctestname)
    print(">>>>[ctest_core] total time: {} seconds".format(time.time() - s))

def test_conf_file(test_input, ctestname):
    params = test_input.keys()
    associated_test_map = {p: [ctestname] for p in params if ctestname in mapping[p]}
    print(">>>>[ctest_core] # parameters associated with the run: {}".format(len(params)))
    tr = run_test_batch(test_input, associated_test_map)
    tup = tr.ran_tests_and_time.pop()
    test, _ = tup.split("\t")
    if test in tr.failed_tests:
        print(">>>>[ctest_core] The single ctest FAIL")
    else:
        print(">>>>[ctest_core] The single ctest PASS")

if __name__ == "__main__":
    main(sys.argv)  