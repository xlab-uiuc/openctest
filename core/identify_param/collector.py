import constant
import utils
import os
import sys
import subprocess
import json
import argparse
import time
import copy
from optparse import OptionParser

class Collector:

    def __init__(self, module):
        self.module = module
        self.getter_record_file = "results/%s/logs/getter-record" % (module)
        self.setter_record_file = "results/%s/logs/setter-record" % (module)

        self.param_getter_map = {}
        self.param_setter_map = {}
        self.param_unset_getter_map = {}
        self.params = utils.get_default_params_from_file(self.module)
        print("total number of configuration parameters: " + str(len(self.params)))

    def parse_getter_record_file(self):
        for line in open(self.getter_record_file).readlines():
            line = line.strip("\n")
            class_pound_method = line.split(" ")[0]
            param = line.split(" ")[1]
            assert param in self.params, "wrong parameter"

            if param not in self.param_getter_map.keys():
                self.param_getter_map[param] = set()
            self.param_getter_map[param].add(class_pound_method)        

    def parse_setter_record_file(self):
        for line in open(self.setter_record_file).readlines():
            line = line.strip("\n")
            class_pound_method = line.split(" ")[0]
            param = line.split(" ")[1]
            assert param in self.params, "wrong parameter"

            if param not in self.param_setter_map.keys():
                self.param_setter_map[param] = set()
            self.param_setter_map[param].add(class_pound_method)
            
    def generate_unset_getter_mapping(self):
        for key in self.param_getter_map.keys():
            self.param_unset_getter_map[key] = copy.deepcopy(self.param_getter_map[key])
            if key in self.param_setter_map.keys():
                self.param_unset_getter_map[key].difference_update(self.param_setter_map[key])
            if len(self.param_unset_getter_map[key]) == 0:
                del self.param_unset_getter_map[key]

    def generate_mapping(self):
        print ("============================================================")
        print ("start reading getter record file")
        self.parse_getter_record_file()
        print ("finish reading getter record file")
        print ("============================================================")
        print ("start reading setter record file")
        self.parse_setter_record_file()
        print ("finish reading setter record file")
        print ("============================================================")
        print( "size of param_getter_map: " + str(len(self.param_getter_map)))
        print( "size of param_setter_map: " + str(len(self.param_setter_map)))
        self.generate_unset_getter_mapping()
        print( "size of param_unset_getter_map: " + str(len(self.param_unset_getter_map)))

    def sanity_check(self):
        for key in self.param_unset_getter_map.keys():
            assert key in self.params, "error"
            if key not in self.param_setter_map.keys():
                assert self.param_unset_getter_map[key] == self.param_getter_map[key]
            else:
                assert self.param_unset_getter_map[key] == self.param_getter_map[key].difference(self.param_setter_map[key])

    def output_mapping(self):
        for key in self.param_getter_map.keys():
            self.param_getter_map[key] = list(self.param_getter_map[key])
        for key in self.param_unset_getter_map.keys():
            self.param_unset_getter_map[key] = list(self.param_unset_getter_map[key])
        for key in self.param_setter_map.keys():
            self.param_setter_map[key] = list(self.param_setter_map[key])
        json.dump(self.param_getter_map, open("results/%s/param_getter_map.json" % self.module, "w"), indent=2)
        json.dump(self.param_unset_getter_map, open("results/%s/param_unset_getter_map.json" % self.module, "w"), indent=2)
        json.dump(self.param_setter_map, open("results/%s/param_setter_map.json" % self.module, "w"), indent=2)

if __name__ == "__main__":
    s = time.time()
    usage = "usage: python3 collector.py project"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    module = args[0]
    collector = Collector(module)
    collector.generate_mapping()
    collector.sanity_check()
    collector.output_mapping()
    print("total time: {} mins".format((time.time() - s) / 60))
