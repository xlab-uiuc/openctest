"""parse the param / value to inject"""

import json, sys, re

sys.path.append("..")
from ctest_const import *

import xml.etree.ElementTree as ET
from program_input import p_input


project = p_input["project"]


def load_deprecate_config_map():
    """
    some project has deprecate configuration
    , deprecate config are config names refactored to a new config name,
    make sure to put them in a file, formatted as `deprecate param, new param`
    and add the file path to DEPRECATE_CONF_FILE in constant.py
    """
    deprecate_conf = {} # load deprecate map
    if project in DEPRECATE_CONF_FILE:
        for line in open(DEPRECATE_CONF_FILE[project]):
            deprecate_param, param = line.strip("\n").split("\t")
            deprecate_conf[deprecate_param] = param
    return deprecate_conf


def load_default_conf(path):
    """load default config, should be in /openctest/default_configs/"""
    data = [x.strip("\n").split("\t") for x in open(path)]
    conf_map = {}
    for row in data:
        param, value = row[:2]
        conf_map[param] = value
    return conf_map


def parse_conf_file(path):
    """parse config file"""
    if project in [HCOMMON, HDFS, HBASE]:
        return parse_conf_file_xml(path)
    else:
        # parsing for alluxio and zookeeper conf file format
        if "no default configuration file" in path:
            return {}
        return parse_conf_file_properties(path)


def parse_conf_file_xml(path):
    deprecate_conf = load_deprecate_config_map()
    conf_map = {}
    fd = ET.parse(path)
    for kv in fd.getroot():
        # get key value pair
        cur_value = None
        cur_key = None
        for prop in kv:
            if prop.tag == "name":
                cur_key = re.sub('\n|\t', '', re.sub(' +', ' ', prop.text))
            elif prop.tag == "value" and cur_key:
                cur_value = prop.text
            else:
                pass
        if cur_key not in conf_map:
            if cur_key in deprecate_conf:
                print(">>>>[ctest_core] {} in your input conf file is deprecated in the project,".format(cur_key)
                 + " replaced with {}".format(deprecate_conf[cur_key]))
                cur_key = deprecate_conf[cur_key]
            conf_map[cur_key] = cur_value
    return conf_map


def parse_conf_file_properties(path):
    deprecate_conf = load_deprecate_config_map()
    conf_map = {}
    for line in open(path):
        if line.startswith("#"):
            continue
        seg = line.strip("\n").split("=")
        if len(seg) == 2:
            cur_key, cur_value = [x.strip() for x in seg]
            if cur_key not in conf_map:
                if cur_key in deprecate_conf:
                    print(">>>>[ctest_core] {} in your input conf file is deprecated in the project,".format(cur_key)
                     + " replaced with {}".format(deprecate_conf[cur_key]))
                    cur_key = deprecate_conf[cur_key]
                conf_map[cur_key] = cur_value
    return conf_map


def extract_conf_diff(path):
    """get the config diff"""
    default_conf_map = load_default_conf(DEFAULT_CONF_FILE[project])
    new_conf_map = parse_conf_file(path)
    print(">>>>[ctest_core] default conf file: {}".format(DEFAULT_CONF_FILE[project]))
    print(">>>>[ctest_core] new input conf file: {} (param, value) pairs".format(len(new_conf_map.keys())))
    conf_diff = {}
    for param, value in new_conf_map.items():
        if param not in default_conf_map:
            print(">>>>[ctest_core] parameter {} in input config file is not in default config file".format(param))
        if param not in default_conf_map or new_conf_map[param] != default_conf_map[param]:
            conf_diff[param] = value
    print(">>>>[ctest_core] config diff: {} (param, value) pairs".format(len(conf_diff)))
    return conf_diff

def extract_conf_diff_from_pair(param_value_dict):
    default_conf_map = load_default_conf(DEFAULT_CONF_FILE[project]) 
    conf_diff = {}
    for param, value in param_value_dict.items():
        if param not in default_conf_map:
            print(">>>>[ctest_core] parameter {} in input config file is not in default config file".format(param))
        if param not in default_conf_map or value != default_conf_map[param]:
            conf_diff[param] = value
    return conf_diff    

def parse_mapping(path):
    print(">>>>[ctest_core] loading mapping {}".format(path))
    return json.load(open(path))


def extract_mapping(mapping, params):
    """get tests associated with a list of params from mapping"""
    data = {}
    selected_tests = []
    for p in params:
        if p in mapping:
            tests = mapping[p]
            print(">>>>[ctest_core] parameter {} has {} tests".format(p, len(tests)))
            data[p] = tests
            selected_tests = selected_tests + tests
        else:
            print(">>>>[ctest_core] parameter {} has 0 tests".format(p))
    return data, set(selected_tests)
