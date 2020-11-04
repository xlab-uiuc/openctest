import re
import random
import config
import sys

NONE = "NOTYPE"
INT = "INT"
FLOAT = "FLOAT"
BOOL = "BOOL"
FILEPATH = "FILEPATH"
IP = "IP"
PORT = "PORT"
IPPORT = "IPPORT"
CLASSNAME = "CLASSNAME"
DIRPATH = "DIRPATH"
INTLIST = "INTLIST"
STRLIST = "STRLIST"
TIME = "TIME"
DATA = "DATA"
PM = "PM"
PC = "PC"
ZKDIR = "ZKDIR"
ZKPORT = "ZKPORT"
ZKPORTADDRESS = "ZKPORTADDRESS"
ZKLIMIT = "ZKLIMIT"
ZKSIZE = "ZKSIZE"
ALGO = "ALGORITHM"
USER = "USER"
GROUP = "GROUP"
NAMESERVICES = "NAMESERVICES"
INTERFACE = "INTERFACE"
POTENTIALFLOAT = "POTENTIALFLOAT"

timeunits = ["ms", "millisecond", "s", "sec", "second", "m", "min", "minute", "h", "hr", "hour", "d", "day"]
datasize = ["MB"]
ALPHABETS = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 
]

# guess from value
def isBool(s):
    if s.lower() == "true" or s.lower() == "false":
        return True
    else:
        return False

def isPort(name, value):
    if value == "" and name.endswith(".port"):
        return True
    if isInt(value) and name.endswith(".port"):
        return True
    return False

def isPermissionMask(name, value):
    if len(value) == 3 and "umask" in name:
        try:
            _ = int("0o" + value, base=8)
            return True
        except ValueError:
            return False

def isPermissionCode(s):
    if len(s) == 9:
        m = re.match(r"^[rwx]+$", s)
        if m:
            return True
    return False

def isInt(s):
    try:
        _ = int(s)
        return True
    except ValueError:
        return False

def isFloat(s):
    m = re.match(r"^\d+\.\d+[fF]$", s)
    if m:
        s = s[:-1]
    try:
        _ = float(s)
        return True
    except ValueError:
        return False

def isIpAddr(s):
    m = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", s)
    return m is not None

def isIpPortAddr(s):
    m = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$", s)
    return m is not None

def isClassName(s):
    return s.startswith("org.apache.hadoop") or s.startswith("alluxio.")

def isFilePath(s):
    # extend, ${} and "/" in dvalue
    if re.match(r"\$\{.*\}", s) and "/" in s:
        return True
    elif s.startswith("/"):
        return True
    else:
        return 

def isIntList(s):
    elements = s.split(",")
    res = True
    for ele in elements:
        res &= isInt(ele)
    return res

def isStringList(s):
    return s.count(",") > 0

def isTime(s):
    for unit in timeunits:
        if s.endswith(unit):
            t = s[:s.find(unit)]
            if isInt(t):
                return True
    return False

def isDataSize(s):
    for unit in datasize:
        if s.endswith(unit):
            t = s[:s.find(unit)]
            if isInt(t):
                return True
    return False

def isAlgorithm(s):
    return s.endswith(".algorithm")

# guess from name
def isFilePath2(name):
    return name.endswith(".conf") or name.endswith('.path')

def isFilePath3(name):
    return name.endswith(".file") or name.endswith(".file.name") or name.endswith("keytab")

def isDirPath(name):
    return name.endswith(".dir")

def isAddr(name):
    return name.endswith(".addr") or name.endswith(".addresses") or name.endswith(".hostname") or name.endswith("address")

def isClassName2(name):
    return name.endswith(".class") or name.endswith(".classes")

def isUser(name):
    return name.endswith("user") or name.endswith("users")

def isGroup(name):
    return name.endswith("group") or name.endswith("groups")

def isNameservices(name):
    return name.endswith("nameservices")

def isInterface(name):
    return name.endswith("interface") or name.endswith("interfaces")

def isPotentialFloat(name):
    return name.endswith("limit") or name.endswith("size")

# guess from semantics
def isFilePath4(semantics):
    return "relative path" in semantics or "directory" in semantics or "folder" in semantics

def genBool(param):
    upcnt = 0
    lowcnt = 0
    for char in param.dvalue:
        if char.isupper():
            upcnt += 1
        elif char.islower():
            lowcnt += 1
    ret = "True"
    if param.dvalue.lower() == "true":
        ret = "False"
    elif param.dvalue.lower() == "false":
        ret = "True"
    if upcnt == 0:
        return [ret.lower()]
    elif lowcnt == 0:
        return [ret.upper()]
    else:
        return [ret]

def genPermissionMask(param):
    return config.PERMISSIONMASKS

def genPermissionCode(param):
    return config.PERMISSIONCODES

def genInt(param):
    val = int(param.dvalue)
    sign = 1
    if val < 0:
        sign = -1
        val = -1 * val
    if val == 1:
        return [0, sign*2]
    elif val == 0:
        return [1, -1]
    else:
        if val <= 10:
            return [sign*1, sign*2*val]
        else:
            return [sign*val//2, sign*val*2]

def genIntList(param):
    vals = param.dvalue.split(",")
    l1 = []
    l2 = []
    for val in vals:
        l1.append(int(val)//2)
        l2.append(int(val)*2)
    return [l1, l2]

def genStringList(param):
    vals = param.dvalue.split(",") # /, ;
    assert len(vals) >= 2
    return [vals[0], vals[1]]

def genFloat(param):
    s = param.dvalue
    m = re.match(r"^\d+\.\d+[fF]$", s)
    if m:
        s = s[:-1]
    val = float(s)
    if val == 0.0:
        return [1.0, -1.0]
    else:
        return [val/2, val*2]

def genPort(param):
    return config.PORTS

def genIPPort(param):
    s = param.dvalue
    s = s[:s.find(":")]
    return [s + ":" + str(config.PORTS[0]), s + ":"  + str(config.PORTS[1])]

def genIP(param):
    return config.IPS

def genFilePath(param):
    return config.FILEPATHS

def genDirPath(param):
    return config.DIRPATHS

def genTime(param):
    s = param.dvalue
    for unit in timeunits:
        if s.endswith(unit):
            t = s[:s.find(unit)]
            if isInt(t):
                t = int(t)
                if t == 0:
                    return ["1" + unit, "2" + unit]
                elif t == 1:
                    return ["10" + unit, "2" + unit]
                return ["1" + unit, str(2*t) + unit]

def genData(param):
    s = param.dvalue
    for unit in datasize:
        if s.endswith(unit):
            t = s[:s.find(unit)]
            if isInt(t):
                t = int(t)
                if t == 0:
                    return ["1" + unit, "2" + unit]
                elif t == 1:
                    return ["10" + unit, "2" + unit]
                return ["1" + unit, str(2*t) + unit]

def genUser(param):
    return config.USERS

def genGroup(param):
    return config.GROUPS

def genNameservices(param):
    return config.NAMESERVICES

def genInterface(param):
    return config.INTERFACES

def genAlgorithm(param):
    return semanticExtractionNoType(param)

def genPotentialFloat(param):
    return [0.1, 0.5]

def semanticExtractionClassName(param):
    # strategies
    # replace "/" in semantics with " "
    semantics = param.description + " "
    # extract words after key phrases from semantics
    arrs = [[], [], []]
    for phrase in config.key_phrases_plural:
        if phrase in semantics:
            parts = semantics.split(phrase)
            raw = parts[1].split(".")[0]
            raw = raw.replace(",", " ")
            raw = raw.replace(" and ", " ")
            raw = raw.replace(" or ", " ")
            raw = raw.strip()
            arrs[0] = raw.split()
            break
    for phrase in config.key_phrases_singular:
        if phrase in semantics:
            parts = semantics.split(phrase)
            tmp = parts[1].split(".")[0]
            tmp = tmp.strip()
            arrs[1] = [tmp]
            break
    # select ,from arr1, arr2 the one containing least non word characters
    # break tie by selecting the one with more values other than SKIP
    nonword = re.compile('\W')
    selected = 0
    mincnt = sys.maxsize
    for idx, arr in enumerate(arrs):
        match = nonword.findall("".join(arr))
        match = [x != "," for x in match]
        if mincnt > len(match):
            selected = idx
            mincnt = len(match)
        elif mincnt == len(match):
            if len(arrs[selected]) < len(arr):
                selected = idx
    arr = []
    hasCapital = False
    for char in param.dvalue:
        if char.isupper():
            hasCapital = True
            break
    for word in arrs[selected]:
        if word == param.dvalue:
            continue
        elif hasCapital:
            for char in word:
                if char.isupper():
                    arr.append(word)
                    break
    if len(arr) != 0:
        return arr[0:2]
    return []

def semanticExtractionNoType(param):
    # strategies
    # replace "/" in semantics with " "
    semantics = param.description + " "
    arrs = [[], [], []]
    for phrase in config.key_phrases_plural:
        if phrase in semantics:
            parts = semantics.split(phrase)
            raw = parts[1].split(".")[0]
            
            if "." not in parts[1] and len(parts) == 2:
                raw = parts[1]
            raw = raw.replace(",", " ")
            raw = raw.replace(":", " ")
            raw = raw.replace(" and ", " ")
            raw = raw.replace(" or ", " ")
            raw = raw.strip()
            arrs[0] = raw.split()
            break
    for phrase in config.key_phrases_singular:
        if phrase in semantics:
            parts = semantics.split(phrase)
            tmp = parts[1].split(".")[0]
            tmp = tmp.strip()
            arrs[1] = [tmp]
            break
    # select ,from arr1, arr2 the one containing least non word characters
    # break tie by selecting the one with more values other than SKIP
    nonword = re.compile('\W')
    selected = 0
    mincnt = sys.maxsize
    for idx, arr in enumerate(arrs):
        match = nonword.findall("".join(arr))
        match = [x != "," for x in match]
        if mincnt > len(match):
            selected = idx
            mincnt = len(match)
        elif mincnt == len(match):
            if len(arrs[selected]) < len(arr):
                selected = idx
    arr = []
    hasCapital = False
    for char in param.dvalue:
        if char.isupper():
            hasCapital = True
            break
    for word in arrs[selected]:
        if word == param.dvalue:
            continue
        elif hasCapital:
            for char in word:
                if char.isupper():
                    arr.append(word)
                    break
        else:
            allLower = True
            for char in word:
                if not char.islower():
                    allLower = False
            if allLower:
                arr.append(word)
    if len(arr) != 0:
        return arr[0:2]
    # map out all capital words
    tmpWord = ""
    skipChars = []
    specialChars = []
    arr = []
    for char in param.dvalue:
        if char not in ALPHABETS:
            skipChars.append(char)
    for char in semantics:
        if char.isupper() or char in skipChars:
            tmpWord += char
        elif char != " " and char not in ALPHABETS:
            tmpWord += char
            specialChars.append(char)
        elif len(tmpWord) > 2:
            if tmpWord[0] not in ALPHABETS:
                tmpWord = tmpWord[1:]
            if tmpWord[-1] not in ALPHABETS:
                tmpWord = tmpWord[0:-1]
            if tmpWord != param.dvalue:
                for schar in specialChars:
                    if schar in tmpWord:
                        tmpWord = ""
                if tmpWord != "":
                    arr.append(tmpWord)
            tmpWord = ""
        else:
            tmpWord = ""
    
    capcnt = 0
    for char in param.dvalue:
        if char.isupper() or char in skipChars:
            capcnt += 1
    if capcnt != len(param.dvalue) or capcnt == 0:
        arr = []
    if len(arr) != 0:
        return arr[0:2]
    return []

def genClassName(param):
    return semanticExtractionClassName(param)

def genNoType(param):
    return semanticExtractionNoType(param)

# for zk only

def isZKDirPath(name):
    return name.endswith("Dir")

def isZKLimit(name):
    return name.endswith("Limit")

def isZKPort(name):
    return name.endswith("Port")

def isZKPortAddress(name):
    return name.endswith("PortAddress")

def isZKSize(name):
    return name.endswith("size")

def genZKDir(param):
    return config.DIRPATHS

def genZKPort(param):
    return config.PORTS

def genZKPortAddress(param):
    return config.ZKPORTADDRS

def genZKLimit(param):
    return config.ZKLIMIT

def genZKSize(param):
    return config.ZKSIZE
