"""take meta argument and run the injection infrastructure"""

import os, sys, time, glob
sys.path.append("..")

from program_input import p_input
from ctest_const import *
from parse_input import *
from inject import inject_config
from run_test import run_test_batch

run_mode = p_input["run_mode"]
mapping = parse_mapping(p_input["mapping_path"])
project = p_input["project"]


def main():
    print(">>>>[ctest_core] running project {}".format(project))
    s = time.time()
    os.makedirs(os.path.join(RUNCTEST_TR_DIR, project), exist_ok=True)
    if run_mode == "run_ctest":
        for conf_file_path in sorted(glob.glob(os.path.join(p_input["conf_file_dir"], "*"))):
            print(">>>>[ctest_core] input conf file: {}".format(conf_file_path))
            test_input = extract_conf_diff(conf_file_path)
            test_conf_file(conf_file_path, test_input)
    else:
        sys.exit(">>>>[ctest_core] invalid run_mode")
    print(">>>>[ctest_core] total time: {} seconds".format(time.time() - s))

def test_conf_file(conf_file_path, test_input):
    fbase = os.path.splitext(os.path.basename(conf_file_path))[0]
    params = test_input.keys()
    associated_test_map, associated_tests = extract_mapping(mapping, params)
    print(">>>>[ctest_core] # parameters associated with the run: {}".format(len(params)))
    print(">>>>[ctest_core] # ctests to run in total: {}".format(len(associated_tests)))
    tr_file = open(os.path.join(RUNCTEST_TR_DIR, project, TR_FILE.format(id=fbase)), "w")
    mt_file = open(os.path.join(RUNCTEST_TR_DIR, project, MT_FILE.format(id=fbase)), "w")
    if len(associated_tests) != 0:
        tr = run_test_batch(test_input, associated_test_map)
        ran_tests = set()
        for tup in tr.ran_tests_and_time:
            test, mvntime = tup.split("\t")
            ran_tests.add(test)
            result = FAIL if test in tr.failed_tests else PASS
            row = [test, result, str(mvntime)]
            tr_file.write("\t".join(row) + "\n")
            tr_file.flush()
        mt_file.write(">>>>[ctest_core] missing ctest for {}\n".format(fbase))
        for test in associated_tests:
            if test not in ran_tests:
                mt_file.write("{}\n".format(test))
        mt_file.flush()
        print(">>>>[ctest_core] conf file {} failed {} ctests".format(conf_file_path, len(tr.failed_tests)))
    else:
        print(">>>>[ctest_core] no ctest for changed params in conf file {}".format(conf_file_path))
    tr_file.close()
    mt_file.close()


if __name__ == '__main__':
    main()
