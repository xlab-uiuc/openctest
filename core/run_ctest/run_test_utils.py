import re, sys

sys.path.append("..")
from ctest_const import *

from program_input import p_input

maven_args = p_input["maven_args"]
use_surefire = p_input["use_surefire"]
ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

class TestResult:
    def __init__(self, ran_tests_and_time=set(), failed_tests=set()):
        self.failed_tests = failed_tests
        self.ran_tests_and_time = ran_tests_and_time


def maven_cmd(test, add_time=False):
    # surefire:test reuses test build from last compilation
    # if you modified the test and want to rerun it, you must use `mvn test`
    test_mode = "surefire:test" if use_surefire else "test"
    cmd = ["mvn", test_mode, "-Dtest={}".format(test)] + maven_args
    if add_time:
        cmd = ["time"] + cmd
    print(">>>>[ctest_core] command: " + " ".join(cmd))
    return cmd


def strip_ansi(s):
    return ansi_escape.sub('', s)


def join_test_string(tests):
    test_by_cls = group_test_by_cls(tests)
    ret = ""
    for clsname, methods in test_by_cls.items():
        ret += clsname
        ret += "#"
        ret += "+".join(list(methods))
        ret += ","
    return ret

def group_test_by_cls(tests):
    d = {}
    for t in tests:
        clsname, method = t.split("#")
        if clsname not in d:
            d[clsname] = set()
        d[clsname].add(method)
    return d

def reverse_map(map):
    # test -> params
    r_map = {}
    for param in map.keys():
        for test in map[param]:
            if test not in r_map.keys():
                r_map[test] = set()
            r_map[test].add(param)
    return r_map

def encode_signature(params, tested_params):
    signature = ""
    for i in range(len(params)):
        param = params[i]
        if param in tested_params:
            signature = signature + "1"
        else:
            signature = signature + "0"
    assert len(signature) == len(params)
    return signature

def decode_signature(params, signature):
    assert len(signature) == len(params)
    tested_params = set()
    for i in range(len(signature)):
        if signature[i] == "1":
            tested_params.add(params[i])
    return tested_params

def split_tests(associated_test_map):
    """split test to rule out value assumption interference"""
    reversed_map = reverse_map(associated_test_map)
    params = sorted(list(associated_test_map.keys()))
    group_map = {}
    for test in reversed_map.keys():
        signature = encode_signature(params, reversed_map[test])
        if signature not in group_map.keys():
            group_map[signature] = set()
        group_map[signature].add(test)
    
    for sig in group_map.keys():
        tested_params = decode_signature(params, sig)
        group_map[sig] = (tested_params, group_map[sig])

    return list(group_map.values())
