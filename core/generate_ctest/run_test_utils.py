import re, sys
from program_input import p_input

sys.path.append("..")
from ctest_const import *

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
