"""parse the test result from surefire"""

import sys
import xml.etree.ElementTree as ET

sys.path.append("..")
from constant import *

from run_test_utils import *
from program_input import p_input

project = p_input["project"]

def parse_surefire(clsname, expected_methods):
    """method expected to show up in surefire"""
    tests = list(expected_methods)
    test_name = tests[0]
    expected_methods = set(expected_methods)
    times = {}
    errors = {}
    try:
        fpath = None
        for surefire_path in SUREFIRE_DIR[project]:
            if project == 'cassandra':
                xml_path = os.path.join(surefire_path, SUREFIRE_XML.format(clsname + '-' + test_name))
            else:
                xml_path = os.path.join(surefire_path, SUREFIRE_XML.format(clsname))
            if os.path.exists(xml_path):
                print(">>>>[ctest_core] surefire report path: " + xml_path)
                fpath = open(xml_path)
        tree = ET.parse(fpath)
        root = tree.getroot()
        tsinfo = root.attrib
        print(">>>>[ctest_core] test class outcome: {}".format(tsinfo))
        for tc in tree.iter(tag="testcase"):
            print(">>>>[ctest_core] unit test outcome: {}".format(tc.attrib))
            tname = tc.attrib["name"]
            ttime = tc.attrib["time"]
            times[tname] = str(ttime)
            for error in tc.iter(tag="error"):
                errors[tname] = strip_ansi(error.text)
            for failure in tc.iter(tag="failure"):
                errors[tname] = strip_ansi(failure.text)

        # failed before executing test 1) test failed, but recorded as init method name
        # failed before executing test 2) test failed, but recorded as cls name
        # if there are more than one upexpected method recorded,
        # this way cannot match noshow tests with recorded failed methods
        unexpected = set(times.keys()) - expected_methods
        if len(unexpected) > 1:
            print(">>>>[ctest_core] [strange] there are more than one unexpected tests")
        expected_noshow = expected_methods - set(times.keys())
        for u in unexpected:
            for e in expected_noshow:
                times[e] = times[u]
                if u in errors:
                    errors[e] = errors[u]
        for u in unexpected:
            times.pop(u, None)
            errors.pop(u, None)

        # assertion
        if int(tsinfo["errors"]) + int(tsinfo["failures"]) != len(errors):
            print(">>>>[ctest_core] [strange] error count doesn't add up")
        if int(tsinfo["tests"]) != len(expected_methods):
            print(">>>>[ctest_core] [strange] # tests run doesn't add up")
        if set(times.keys()) != expected_methods:
            print(">>>>[ctest_core] [strange] tests run not the same as expected tests")
    except Exception as e:
        print(">>>>[ctest_core] failed to parse surefire file: {}".format(e))

    # pretty printing
    print(">>>>[ctest_core] result to be return:")
    for t in times:
        fulltname = clsname + "#" + t
        if t in errors:
            print(fulltname + " with running time " + times[t] + " failed")
            print(">>>>[ctest_core] failed test output: {}".format(errors[t]))
        else:
            print(fulltname + " with running time " + times[t] + " passed")
    return times, errors