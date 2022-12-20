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
        if "java.lang.Thread" in trace:
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
        if self.module == 'cassandra':
            if 'daemonInitialization' in trace or 'toolInitialization' in trace:
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
        getter, setter = set(), set()
        for line in lines:
            line = line.strip("\n")
            if "[CTEST][GET-PARAM]" in line:
                line = line[line.find("[CTEST][GET-PARAM]"):]
                assert line.startswith("[CTEST][GET-PARAM] "), "wrong line: " + line
                comp = line.split(" ")
                assert comp[0] == "[CTEST][GET-PARAM]"
                assert len(comp) == 2, "more than one whitespace in " + line
                param_name = comp[1]
                if param_name in self.params:
                    full_name = method + " " + param_name + "\n"
                    if full_name not in getter:
                        self.getter_record.write(full_name)
                        self.getter_record.flush()
                        getter.add(full_name)
            elif "[CTEST][SET-PARAM]" in line:
                line = line[line.find("[CTEST][SET-PARAM]"):]
                assert line.startswith("[CTEST][SET-PARAM] "), "wrong line: " + line
                comp = line.split(" ")
                assert len(comp) == 3, "more than two whitespaces in " + line
                assert comp[0] == "[CTEST][SET-PARAM]"
                param_name = comp[1]
                if param_name in self.params:
                    if self.aggressive or self.setInTest(comp[2]):
                        full_name = method + " " + param_name + "\n"
                        if full_name not in setter:
                            self.setter_record.write(full_name)
                            self.setter_record.flush()
                            setter.add(full_name)

        if len(getter) or len(setter):
            if len(getter):
                print(method + " is a getter")
                self.getter_list.append(method)
            if len(setter):
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
                print ("mvn surefire:test -Dtest="+method)
            elif self.module == "cassandra":
                os.environ['CASSANDRA_USE_JDK11'] = 'true'
                class_name, method_name = method.split('#')
                cmd = ["ant", "testsome", "-Dtest.name=" + class_name, "-Dtest.methods=" + method_name]
                print ("ant testsome -Dtest.name=" + class_name, " -Dtest.methods=" + method_name)
            else:
                cmd = ["mvn", "surefire:test", "-Dtest=" + method]
                print ("mvn surefire:test -Dtest="+method)
            try:
                subprocess.run(cmd, stdout=method_out, stderr=method_out, timeout=40)
            except subprocess.TimeoutExpired:
                print(f"{method} running too slow, skip")
                self.no_report_list.append(method)
                continue

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

            if self.module == 'cassandra':
                method_name = method.split("#")[1]
                suffix_filename_to_check = method_name + ".xml"
            else:
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
