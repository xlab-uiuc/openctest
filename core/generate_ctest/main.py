"""take meta argument and run the injection infrastructure"""

import os, sys, time, glob

sys.path.append("..")
from ctest_const import *

from program_input import p_input
from parse_input import *
from inject import inject_config
from run_test import run_test_seperate

run_mode = p_input["run_mode"]
mapping = parse_mapping(p_input["mapping_path"])
project = p_input["project"]


def main():
    print(">>>>[ctest_core] running project {}".format(project))
    s = time.time()
    os.makedirs(os.path.join(GENCTEST_TR_DIR, project), exist_ok=True)
    if run_mode == "generate_ctest":
        test_input = parse_value_file(p_input["param_value_tsv"])
        test_value_pair(test_input)
    else:
        sys.exit(">>>>[ctest_core] invalid run_mode")
    print(">>>>[ctest_core] total time: {} seconds".format(time.time() - s))


def test_value_pair(test_input):
    for param, values in test_input.items():
        tr_file = open(os.path.join(GENCTEST_TR_DIR, project, TR_FILE.format(id=param)), "w")
        mt_file = open(os.path.join(GENCTEST_TR_DIR, project, MT_FILE.format(id=param)), "w")

        associated_tests = mapping[param] if param in mapping else []
        if len(mapping[param]) != 0:
            for value in values:
                tr = run_test_seperate(param, value, associated_tests)
                
                ran_tests = set()
                for tup in tr.ran_tests_and_time:
                    test, mvntime = tup.split("\t")
                    ran_tests.add(test)
                    result = FAIL if test in tr.failed_tests else PASS
                    row = [param, test, value, result, str(mvntime)]
                    tr_file.write("\t".join(row) + "\n")
                    tr_file.flush()
                subheader = [project, param, value]
                mt_file.write(">>>>[ctest_core] missing test for {}\n".format("\t".join(subheader)))
                for test in associated_tests:
                    if test not in ran_tests:
                        mt_file.write("{}\n".format(test))
                mt_file.flush()
                print(">>>>[ctest_core] param {} failed {} tests with value {}".format(param, len(tr.failed_tests), value))
        else:
            print(">>>>[ctest_core] no test for param {} in mapping {}".format(param, p_input["mapping_path"]))
        tr_file.close()
        mt_file.close()


if __name__ == '__main__':
    main()
