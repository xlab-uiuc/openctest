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


def run_test_batch(param_values, associated_test_map):
    print(">>>>[ctest_core] start running ctests for {} parameters".format(len(associated_test_map)))
    param_test_group = run_test_utils.split_tests(associated_test_map)
    print(">>>>[ctest_core] splitting into {} ctest group".format(len(param_test_group)))
    for index, group in enumerate(param_test_group):
        print(">>>>[ctest_core] group {}, tested_params: {}, group size: {}".format(index, ",".join(group[0]), len(group[1])))
    start_time = time.time()
    tr = run_test_utils.TestResult(ran_tests_and_time=set(), failed_tests=set())
    for index, group in enumerate(param_test_group):
        # # do injection for different test group and chdir for testing everytime
        tested_params, tests = group
        inject_config({p: param_values[p] for p in tested_params})
        print(">>>>[ctest_core] running group {} where {} params shares {} ctests".format(index, len(tested_params), len(tests)))
        test_str = run_test_utils.join_test_string(tests)
        os.chdir(testing_dir)
        print(">>>>[ctest_core] chdir to {}".format(testing_dir))

        cmd = run_test_utils.maven_cmd(test_str)
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
        os.chdir(RUN_CTEST_DIR)
        print(">>>>[ctest_core] chdir to {}".format(RUN_CTEST_DIR))

        print_output = run_test_utils.strip_ansi(stdout.decode("ascii", "ignore"))
        print(print_output)
        test_by_cls = run_test_utils.group_test_by_cls(tests)
        for clsname, methods in test_by_cls.items():
            times, errors = parse_surefire(clsname, methods)
            for m in methods:
                if m in times:
                    tr.ran_tests_and_time.add(clsname + "#" + m + "\t" + times[m])
                    if m in errors:
                        tr.failed_tests.add(clsname + "#" + m)
    duration = time.time() - start_time
    os.chdir(RUN_CTEST_DIR)
    print(">>>>[ctest_core] chdir to {}".format(RUN_CTEST_DIR))
    print(">>>>[ctest_core] python-timed for running config file: {}".format(duration))
    clean_conf_file(project)
    return tr

