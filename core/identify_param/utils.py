import constant
import glob

def get_local_surefire_report(module):
    ret = []
    report_dirs = constant.LOCAL_SUREFIRE_PATH[module]
    for report_dir in report_dirs:
        ret += glob.glob(report_dir)
    return ret

def get_ctest_surefire_report(module):
    ret = []
    report_dirs = constant.CTEST_SUREFIRE_PATH[module]
    for report_dir in report_dirs:
        ret += glob.glob(report_dir)
    return ret

def get_default_params_from_file(module):
    ret = set()
    for line in open(constant.LOCAL_CONF_PATH[module]).readlines():
        ret.add(line.strip())
    return ret


