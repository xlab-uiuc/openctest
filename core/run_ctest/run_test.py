"""take meta argument and run the injection infrastructure"""

import os, time, sys
from subprocess import Popen, PIPE, TimeoutExpired

sys.path.append("..")
from constant import *

from program_input import p_input
from inject import inject_config, clean_conf_file
from parse_output import *
import run_test_utils

display_mode = p_input["display_mode"]
project = p_input["project"]
cmd_timeout = p_input["cmd_timeout"]
testing_dir = os.path.join(PROJECT_DIR[project], MODULE_SUBDIR[project])


def run_test_batch(param_value_dict, param_test_dict):
    print(">>>>[ctest_core] start running ctests for {} parameters".format(len(param_test_dict)))
    param_test_group = run_test_utils.split_tests(param_test_dict)
    print(">>>>[ctest_core] splitting into {} ctest group".format(len(param_test_group)))
    for index, group in enumerate(param_test_group):
        print(">>>>[ctest_core] group {}, tested_params: {}, group size: {}".format(index, ",".join(group[0]), len(group[1])))
    start_time = time.time()
    tr = run_test_utils.TestResult(ran_tests_and_time=set(), failed_tests=set())
    for index, group in enumerate(param_test_group):
        # # do injection for different test group and chdir for testing everytime
        affected_params, affected_tests = group
        inject_config({p: param_value_dict[p] for p in affected_params})
        print(">>>>[ctest_core] running group {} where {} params shares {} ctests".format(index, len(affected_params), len(affected_tests)))
        os.chdir(testing_dir)
        print(">>>>[ctest_core] chdir to {}".format(testing_dir))

        cmd = run_test_utils.ant_cmd(affected_tests)
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
                print(">>>>[ctest_core] ant cmd timeout {}".format(e))
                test = affected_tests.pop()
                tr.ran_tests_and_time.add(test + "\t" + str(cmd_timeout))
                tr.failed_tests.add(test)
                continue
        else:
            stdout, stderr = process.communicate()
        os.chdir(RUN_CTEST_DIR)
        print(">>>>[ctest_core] chdir to {}".format(RUN_CTEST_DIR))

        print_output = run_test_utils.strip_ansi(stdout.decode("ascii", "ignore"))
        print(print_output)
        classname_method_dict = run_test_utils.group_test_by_cls(affected_tests)
        for clsname, methods in classname_method_dict.items():
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

