"""take meta argument and run the injection infrastructure"""

import os, re, time, sys
from subprocess import Popen, PIPE, TimeoutExpired

sys.path.append("..")
from ctest_const import *

from program_input import p_input
from inject import inject_config, clean_conf_file
from parse_output import parse_surefire
import run_test_utils

display_mode = p_input["display_mode"]
project = p_input["project"]
cmd_timeout = p_input["cmd_timeout"]
testing_dir = os.path.join(PROJECT_DIR[project], MODULE_SUBDIR[project])


def run_test_seperate(param, value, associated_tests):
    print(">>>>[ctest_core] running {} tests seperately".format(len(associated_tests)))
    inject_config({param: value})
    tr = run_test_utils.TestResult(ran_tests_and_time=set(), failed_tests=set())
    os.chdir(testing_dir)
    print(">>>>[ctest_core] chdir to {}".format(testing_dir))
    start_time = time.time()
    for test in associated_tests:
        cmd = run_test_utils.maven_cmd(test)
        if display_mode:
            os.system(" ".join(cmd))
            continue

        process = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout = ""
        stderr = ""
        if cmd_timeout:
            try:
                stdout, stderr = process.communicate(timeout=int(cmd_timeout))
            except TimeoutExpired as e:
                # test hanged, treated as failure.
                process.kill()
                print(">>>>[ctest_core] maven cmd timeout {}".format(e))
                clsname, testname = test.split("#")
                tr.ran_tests_and_time.add(test + "\t" + str(cmd_timeout))
                tr.failed_tests.add(test)
                continue
        else:
            stdout, stderr = process.communicate()

        print_output = run_test_utils.strip_ansi(stdout.decode("ascii", "ignore"))
        print(print_output)
        clsname, testname = test.split("#")
        times, errors = parse_surefire(clsname, [testname])
        if testname in times:
            tr.ran_tests_and_time.add(test + "\t" + times[testname])
            if testname in errors:
                tr.failed_tests.add(test)
    duration = time.time() - start_time
    os.chdir(CUR_DIR)
    print(">>>>[ctest_core] chdir to {}".format(CUR_DIR))
    print(">>>>[ctest_core] python-timed for running config pair: {}".format(duration))
    clean_conf_file(project)
    return tr
