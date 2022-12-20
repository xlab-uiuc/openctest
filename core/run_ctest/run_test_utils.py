import re, sys

sys.path.append("..")
from constant import *

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

def ant_cmd(affected_tests):
    # affected_tests example: {'org.apache.cassandra.hints.HintsCatalogTest#deleteHintsTest'}
    for test in affected_tests:
        test_name, test_method = test.split('#')
        cmd = ['ant', 'testsome', "-Dtest.name={}".format(test_name), "-Dtest.methods={}".format(test_method)]
        print(">>>>[ctest_core] command: " + " ".join(cmd))
    return cmd

def strip_ansi(s):
    return ansi_escape.sub('', s)


def join_test_string(tests):
    classname_method_dict = group_test_by_cls(tests)
    ret = ""
    for clsname, methods in classname_method_dict.items():
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

def encode_signature(params, affected_params):
    signature = ""
    for i in range(len(params)):
        param = params[i]
        if param in affected_params:
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

def split_tests(param_test_dict):
    """split test to rule out value assumption interference"""
    test_param_dict = reverse_map(param_test_dict)
    params = sorted(list(param_test_dict.keys()))
    group_map = {}
    for test in test_param_dict.keys():
        param_sign = encode_signature(params, test_param_dict[test])
        if param_sign not in group_map.keys():
            group_map[param_sign] = set()
        group_map[param_sign].add(test)

    res = {}
    for sig in group_map.keys():
        affected_params = decode_signature(params, sig)
        # group_map[sig] = (affected_params, group_map[sig])
        res[sig] = (affected_params, group_map[sig])

    return list(res.values())
