import glob
import constant
import utils
import xml.etree.ElementTree as ET
import os
import sys
import subprocess
import json
import time
import shutil
from optparse import OptionParser

class Runner:

    def __init__(self, module, aggressive=False):
        self.module = module
        self.run_list = "results/" + module + "/test_method_list.json"

        self.other_list = []
        self.no_report_list = []
        self.failure_list = []
        self.setter_list = []
        self.getter_list = []
        self.aggressive = aggressive

        self.params = utils.get_default_params_from_file(self.module)
        print("num of params: " + str(len(self.params)))

        os.makedirs("results/%s/logs/" % (self.module), exist_ok=True)

        self.getter_record = open("results/%s/logs/getter-record" % (self.module), "w")
        self.setter_record = open("results/%s/logs/setter-record" % (self.module), "w")
        self.time_record = open("results/%s/logs/time-record" % (self.module), "w")

    def get_full_report_path(self, suffix):
        all_reports = utils.get_ctest_surefire_report(self.module)
        for report in all_reports:
                if report.endswith(suffix):
                    return report
        return "none"

    def traceInTestCode(self, trace):
        if "Test" in trace:
            return True
        if self.module == "hadoop-common" or self.module == "hadoop-hdfs" or self.module == "hbase-server":
            if "MiniDFSCluster" in trace:
                return True
            if "MiniZKFCCluster" in trace:
                return True
            if "MiniJournalCluster" in trace:
                return True
            if "MiniQJMHACluster" in trace:
                return True
            if "MiniHBaseCluster" in trace:
                return True
            if "MockFileSystem" in trace:
                return True
        if self.module == "alluxio-core":
            if "alluxio.ConfigurationRule" in trace:
                return True
        return False

    def skipTrace(self, trace):
        if trace == "java.lang.Thread":
            return True
        if "sun.reflect" in trace:
            return True
        if self.module == "hadoop-common" or self.module == "hadoop-hdfs" or self.module == "hbase-server":
            if "org.apache.hadoop.conf" in trace and "Test" not in trace:
                return True
            if "org.mockito" in trace:
                return True
        if self.module == "zookeeper-server":
            if "org.apache.zookeeper.server.quorum.QuorumPeerConfig" in trace:
                return True
            if "org.apache.zookeeper.server.ServerConfig" in trace:
                return True
        if self.module == "alluxio-core":
            if "alluxio.conf" in trace and "Test" not in trace:
                return True
        return False

    def setInTest(self, stacktrace):
        traces = stacktrace.split("\t")
        for trace in traces:
            if self.skipTrace(trace):
                continue
            else:
                if self.traceInTestCode(trace):
                    return True
                else:
                    return False

    def parse(self, lines, method):
        is_getter = False
        is_setter = False
        for line in lines:
            line = line.strip("\n")
            if "[CTEST][GET-PARAM]" in line:
                line = line[line.find("[CTEST][GET-PARAM]"):]
                assert line.startswith("[CTEST][GET-PARAM] "), "wrong line: " + line
                assert line.split(" ")[0] == "[CTEST][GET-PARAM]"
                assert line.count(" ") == 1, "more than one whitespace in " + line
                param_name = line.split(" ")[1]
                if param_name in self.params:
                    is_getter = True 
                    self.getter_record.write(method + " " + param_name + "\n")
                    self.getter_record.flush()
            elif "[CTEST][SET-PARAM]" in line:
                line = line[line.find("[CTEST][SET-PARAM]"):]
                assert line.startswith("[CTEST][SET-PARAM] "), "wrong line: " + line
                assert line.split(" ")[0] == "[CTEST][SET-PARAM]"
                assert line.count(" ") == 2, "more than one whitespace in " + line
                param_name = line.split(" ")[1]
                if param_name in self.params:
                    if self.aggressive or self.setInTest(line.split(" ")[2]):
                        is_setter = True
                        self.setter_record.write(method + " " + param_name + "\n")
                        self.setter_record.flush()

        if is_getter or is_setter:
            if is_getter:
                print(method + " is a getter")
                self.getter_list.append(method)
            if is_setter:
                print(method + " is a setter")
                self.setter_list.append(method)
        else:
            self.other_list.append(method)

    def test_pass_or_not(self, log_content):
        if "BUILD SUCCESS" in log_content:
            return True
        elif "BUILD FAILURE" in log_content:
            return False
        else:
            assert False, "wrong log content"

    def persist_list(self, method_list, file_name):
        json_file = open("results/%s/logs/%s.json" % (self.module, file_name), "w")
        json.dump(method_list, json_file)
        json_file.close()

    def run_individual_testmethod(self):
        all_test_methods = json.load(open("%s" % (self.run_list)))
        length = len(all_test_methods)
        print ("number of all test methods: " + str(length))

        old_path = os.getcwd()
        print (old_path)
        os.chdir(constant.MVN_TEST_PATH[self.module])
        print("change to " + constant.MVN_TEST_PATH[self.module])

        out_dir = old_path + "/" + self.module + "-mvn-test-output/"
        report_dir = old_path + "/" + self.module + "-mvn-test-reports/"
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(report_dir, exist_ok=True)

        for method in all_test_methods:
            print("==================================================================================")
            assert method.count("#") == 1, "there should be only one #, but actually you have: " + method

            method_out = open(out_dir + method + "-log.txt", "w+")
            method_report_path = report_dir + method + "-report.txt"
            start_time_for_this_method = time.time()
            if self.module == "alluxio-core":
                cmd = ["mvn", "surefire:test", "-Dtest=" + method, "-DfailIfNoTests=false"]
            else:
                cmd = ["mvn", "surefire:test", "-Dtest=" + method]
            print ("mvn surefire:test -Dtest="+method)
            child = subprocess.Popen(cmd, stdout=method_out, stderr=method_out)
            child.wait()

            finish_time_for_this_method = time.time()
            time_elapsed = finish_time_for_this_method - start_time_for_this_method
            print("time elapsed: " + str(time_elapsed))
            method_out.seek(0)
            pass_or_not = self.test_pass_or_not(method_out.read())
            method_out.close()
            self.time_record.write(method + " " + str(time_elapsed) + "\n")

            if pass_or_not:
                print(method + " success")
            else:
                print(method + " failure")
                self.failure_list.append(method)
                continue

            class_name = method.split("#")[0]
            suffix_filename_to_check = class_name + "-output.txt"
            full_path = self.get_full_report_path(suffix_filename_to_check)
            if full_path == "none":
                print("no report for " + method)
                self.no_report_list.append(method)     
            else:
                shutil.copy(full_path, method_report_path)
                self.parse(open(full_path, "r").readlines(), method)

        shutil.rmtree(out_dir)
        shutil.rmtree(report_dir)
        os.chdir(old_path)

        self.getter_record.close()
        self.setter_record.close()
        self.time_record.close()

        self.persist_list(self.setter_list, "setter")
        self.persist_list(self.getter_list, "getter")
        self.persist_list(self.other_list, "other")
        self.persist_list(self.no_report_list, "no_report")
        self.persist_list(self.failure_list, "failure")

if __name__ == "__main__":
    s = time.time()
    usage = "usage: python3 runner.py project [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-a", action="store_true", dest="aggressive", default=False,
                  help="Be aggressive when looking for setters and ignore stacktrace.")
    (options, args) = parser.parse_args()
    module = args[0]
    aggr = options.aggressive
    runner = Runner(module, aggr)
    runner.run_individual_testmethod()
    print("total time: {} mins".format((time.time() - s) / 60))
