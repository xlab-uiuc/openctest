"""parse the param / value to inject"""

import json, sys, re
import xml.etree.ElementTree as ET

sys.path.append("..")
from ctest_const import *

from program_input import p_input

project = p_input["project"]

def parse_value_file(path):
    """return param: [(value type, value)]"""
    data = {}
    samples = [x.strip("\n").split("\t") for x in open(path)]
    for row in samples:
        parameter = row[0]
        values = [x for x in row[1:] if x != SKIP_VAL]
        if values != []:
            if parameter not in data:
                data[parameter] = []
            data[parameter] += values
    return data


def parse_mapping(path):
    print(">>>>[ctest_core] loading mapping {}".format(path))
    return json.load(open(path))

