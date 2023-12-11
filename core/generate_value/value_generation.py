from gutil import *
import csv
import sys
from optparse import OptionParser

DEBUG = False
params = []
generators = {}
output = "-generated-values.tsv"

class Param:
    def __init__(self, name, dvalue, description):
        self.name = name
        self.dvalue = dvalue
        self.cate = NONE
        self.gvalues = []
        self.description = description

def read_tsv(module):
    params.clear()
    tsv_file = open("../default_configs/" + module + "-default.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")
    for row in read_tsv:
        params.append(Param(row[0], row[1], row[2]))
    if module == "zookeeper-server":
        assert len(params) == 32
        return 32
    elif module == "forem":
        assert len(params) == 166
        return 166 
    else:
        assert len(params) == 90
        return 90

def infer_category(param, module):
    dval = param.dvalue
    name = param.name
    # guess from value
    if isBool(dval):
        return BOOL
    if isPort(name, dval):
        return PORT
    if isPermissionMask(name, dval):
        return PM
    if isInt(dval):
        return INT
    if isFloat(dval):
        return FLOAT
    if isPermissionCode(dval):
        return PC
    if isIntList(dval):
        return INTLIST
    if isStringList(dval):
        return STRLIST
    if isIpAddr(dval):
        return IP
    if isIpPortAddr(dval):
        return IPPORT
    if isClassName(dval):
        return CLASSNAME
    if isFilePath(dval):
        return FILEPATH
    if isTime(dval):
        return TIME
    if isDataSize(dval):
        return DATA
    # guess from name
    if isDirPath(name):
        return DIRPATH
    if isAddr(name):
        return IP
    if isClassName2(name):
        return CLASSNAME
    if isFilePath2(name):
        return FILEPATH
    if isFilePath3(name):
        return FILEPATH
    if isAlgorithm(name):
        return ALGO
    if isUser(name):
        return USER
    if isGroup(name):
        return GROUP
    if isNameservices(name):
        return NAMESERVICES
    if isInterface(name):
        return INTERFACE

    if module == "zookeeper-server":
        if isZKDirPath(name):
            return ZKDIR
        if isZKPort(name):
            return ZKPORT
        if isZKPortAddress(name):
            return ZKPORTADDRESS
        if isZKLimit(name):
            return ZKLIMIT
        if isZKSize(name):
            return ZKSIZE
    if isPotentialFloat(name):
        return POTENTIALFLOAT
    return NONE

def print_params(module):
    pcnt = 0
    vcnt = 0
    unhandled = []
    f = open(module + output, "w")
    if module == "zookeeper-server":
        assert len(params) == 32
    elif module == "forem":
        assert len(params) == 166
    else:
        assert len(params) >= 90
    for param in params:
        f.write(param.name + "\t")
        tmp_cnt = 0
        if len(param.gvalues) == 0:
            if module == "forem":
                f.write(str(param.dvalue) + "\tSKIP\n")  # Write default value for forem
                tmp_cnt += 1
            else:
                if DEBUG:
                    print("----------------------")
                    print(param.name)
                    print(param.dvalue)
                    print(param.description)
                    print("----------------------")
                f.write("SKIP\tSKIP\n")
                unhandled.append(param)
        else:
            pcnt += 1
            tmp_cnt += 1 # for the default value
            tmp_cnt += len(param.gvalues)
            assert len(param.gvalues) <= 2
            if len(param.gvalues) == 1:
                f.write(str(param.gvalues[0]) + "\tSKIP\n")
            elif len(param.gvalues) == 2:
                f.write(str(param.gvalues[0]) + "\t" + str(param.gvalues[1]) + "\n")
            else:
                assert False
            assert tmp_cnt <= 3
            vcnt += tmp_cnt
    print(module + ":")
    print("covered parameters: " + str(pcnt))
    print("values generated: " + str(vcnt))
    return pcnt

def categorize(module):
    for param in params:
        param.cate = infer_category(param, module)

def generate(module):
    generators[BOOL] = genBool
    generators[INT] = genInt
    generators[FLOAT] = genFloat
    generators[FILEPATH] = genFilePath
    generators[DIRPATH] = genDirPath
    generators[IPPORT] = genIPPort
    generators[TIME] = genTime
    generators[DATA] = genData
    generators[INTLIST] = genIntList
    generators[CLASSNAME] = genClassName
    generators[IP] = genIP
    generators[PORT] = genPort
    generators[PM] = genPermissionMask
    generators[PC] = genPermissionCode
    generators[NONE] = genNoType
    generators[STRLIST] = genStringList
    generators[ALGO] = genAlgorithm
    generators[USER] = genUser
    generators[GROUP] = genGroup
    generators[NAMESERVICES] = genNameservices
    generators[INTERFACE] = genInterface
    generators[POTENTIALFLOAT] = genPotentialFloat
    if module == "zookeeper-server":
        generators[ZKDIR] = genZKDir
        generators[ZKLIMIT] = genZKLimit
        generators[ZKSIZE] = genZKSize
        generators[ZKPORT] = genZKPort
        generators[ZKPORTADDRESS] = genZKPortAddress
    for param in params:
        param.gvalues = generators[param.cate](param)

if __name__ == "__main__":
    usage = "usage: python3 value_generation.py project"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    module = args[0]
    all_params = read_tsv(module)
    categorize(module)
    generate(module)
    covered_params = print_params(module)
    print("total params: " + str(all_params))
    print("coverage: " + str(covered_params/all_params))