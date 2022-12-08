"""generate ctests for a parameter by removing the hardcoded tests based on 
test result from config_injection"""

import glob, json, os, re, sys

sys.path.append("..")
from ctest_const import *

from program_input import p_input

project = p_input["project"]

def identify_ctest(project):
    test_result_dir = os.path.join(GENCTEST_TR_DIR, project)
    ctest_file = os.path.join(CTESTS_DIR, CTESTS_FILE.format(project=project))
    try:
        ctests = json.load(open(ctest_file, "r"))
        ctest_file.close()
    except:
        ctests = {}

    for result_file in glob.glob(os.path.join(test_result_dir, "*.tsv")):
        print(">>>>[ctest_core] processing test result file {}".format(result_file))
        testresult = [x.strip("\n").split("\t") for x in open(result_file)]
        
        testinfo = {}
        for row in testresult:
            param, test, value, result, mvntime = row[:6]
            if param not in testinfo:
                testinfo[param] = {"good_values": set(), "tests": {}}
            testinfo[param]["good_values"].add(value)

            # record good values this test passed
            if result == PASS:
                if test not in testinfo[param]["tests"]:
                    testinfo[param]["tests"][test] = set()
                testinfo[param]["tests"][test].add(value)

        # ctest should pass all good value
        for param, info in testinfo.items():
            ctests[param] = []
            good_values = testinfo[param]["good_values"]
            for test, pass_good_values in testinfo[param]["tests"].items():
                if len(good_values) == len(pass_good_values):
                    ctests[param].append(test)
            print(">>>>[ctest_core] param {} has {} ctests".format(
                param, len(ctests[param])))

    print(">>>>[ctest_core] project: {}, test result dir: {}, #params: {}".format(
        project, test_result_dir, len(ctests)))
    ctest_outf = open(ctest_file, "w")
    json.dump(ctests, ctest_outf)
    ctest_outf.close()


if __name__ == '__main__':
    identify_ctest(project)
