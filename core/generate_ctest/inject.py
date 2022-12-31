"""inject parameter, values into sw config"""

import fileinput
import shutil
import sys
import xml.etree.ElementTree as ET
import yaml

sys.path.append("..")
from ctest_const import *

from program_input import p_input

project = p_input["project"]

def inject_config(param_value_pairs):
    for p, v in param_value_pairs.items():
        print(">>>>[ctest_core] injecting {} with value {}".format(p, v))

    if project in [ZOOKEEPER, ALLUXIO]:
        for inject_path in INJECTION_PATH[project]:
            print(">>>>[ctest_core] injecting into file: {}".format(inject_path))
            file = open(inject_path, "w")
            for p, v in param_value_pairs.items():
                file.write(p + "=" + v + "\n")
            file.close()
    elif project in [HCOMMON, HDFS, HBASE]:
        conf = ET.Element("configuration")
        for p, v in param_value_pairs.items():
            prop = ET.SubElement(conf, "property")
            name = ET.SubElement(prop, "name")
            value = ET.SubElement(prop, "value")
            name.text = p
            value.text = v
        for inject_path in INJECTION_PATH[project]:
            print(">>>>[ctest_core] injecting into file: {}".format(inject_path))
            file = open(inject_path, "wb")
            file.write(str.encode("<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n"))
            file.write(ET.tostring(conf))
            file.close()
    elif project in [DROPWIZARD]:
        health_path = INJECTION_PATH[DROPWIZARD][0]
        health_check_path = INJECTION_PATH[DROPWIZARD][1]
        health_check_java_class_path = INJECTION_PATH[DROPWIZARD][2]
        schedule_path = INJECTION_PATH[DROPWIZARD][3]

        health_conf = yaml.full_load(open(health_path, "r"))
        health_check_conf = yaml.full_load(open(health_check_path, "r"))
        schedule_conf = yaml.full_load(open(schedule_path, "r"))

        for p, v in param_value_pairs.items():
            p_expanded = p.split(".")

            if len(p_expanded) == 2:
                # inject health.param_name
                print(">>>>[ctest_core] injecting into file: {}".format(health_path))
                param_name_idx = 1
                health_conf[p_expanded[param_name_idx]] = v
            elif len(p_expanded) == 3:
                # inject health.healthChecks.param_name
                print(">>>>[ctest_core] injecting into file: {}".format(health_check_path))
                param_name_idx = 2
                health_conf['healthChecks'][0][p_expanded[param_name_idx]] = v
                health_check_conf[p_expanded[param_name_idx]] = v
                
                print(">>>>[ctest_core] injecting into file: {}".format(health_check_java_class_path))
                code_injection_line_number = INJECTION_LINE_NUMBER[DROPWIZARD][p]
                if code_injection_line_number is not None:
                    for line in fileinput.input(health_check_java_class_path, inplace=True):
                        if fileinput.filelineno() == code_injection_line_number:
                            format_string = INJECTION_CODE_FORMAT[DROPWIZARD][p]
                            if p_expanded[param_name_idx] == "type":
                                if v == "ready":
                                    sys.stdout.write(format_string.format("HealthCheckType.READY"))
                                else:
                                     sys.stdout.write(format_string.format("HealthCheckType.ALIVE"))
                            else:
                                sys.stdout.writelines(format_string.format(v))
                        else:
                            sys.stdout.write(line)
            elif len(p_expanded) == 4:
                # inject health.healthChecks.schedule.param_name
                print(">>>>[ctest_core] injecting into file: {}".format(schedule_path))
                param_name_idx = 3
                health_conf['healthChecks'][0]['schedule'] = dict()
                health_conf['healthChecks'][0]['schedule'][p_expanded[param_name_idx]] = v
                schedule_conf[p_expanded[param_name_idx]] = v
            else:
                print(">>>>[ctest_core] parameter {} with value {} is not recognized".format(p, v))
                
        with open(health_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(health_conf, sort_keys=False))
        
        with open(health_check_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(health_check_conf, sort_keys=False))

        with open(schedule_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(schedule_conf, sort_keys=False))
    else:
        sys.exit(">>>>[ctest_core] value injection for {} is not supported yet".format(project))


def clean_conf_file(project):
    print(">>>> cleaning injected configuration from file")
    if project in [ZOOKEEPER, ALLUXIO]:
        for inject_path in INJECTION_PATH[project]:
            file = open(inject_path, "w")
            file.write("\n")
            file.close()
    elif project in [HCOMMON, HDFS, HBASE]:
        conf = ET.Element("configuration")
        for inject_path in INJECTION_PATH[project]:
            file = open(inject_path, "wb")
            file.write(str.encode("<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n"))
            file.write(ET.tostring(conf))
            file.close()
    elif project in [DROPWIZARD]:
        health_default_path = INJECTION_CLEAN_UP_PATH[DROPWIZARD][0]
        health_injection_path = INJECTION_PATH[DROPWIZARD][0]

        health_check_default_path = INJECTION_CLEAN_UP_PATH[DROPWIZARD][1]
        health_check_injection_path = INJECTION_PATH[DROPWIZARD][1]

        health_check_java_class_default_path = INJECTION_CLEAN_UP_PATH[DROPWIZARD][2]
        health_check_java_class_injection_path = INJECTION_PATH[DROPWIZARD][2]

        schedule_default_path = INJECTION_CLEAN_UP_PATH[DROPWIZARD][3]
        schedule_injection_path = INJECTION_PATH[DROPWIZARD][3]

        health_default_conf = yaml.full_load(open(health_default_path, "r"))
        health_check_default_conf = yaml.full_load(open(health_check_default_path, "r"))
        schedule_default_conf = yaml.full_load(open(schedule_default_path, "r"))

        with open(health_injection_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(health_default_conf, sort_keys=False))
        
        with open(health_check_injection_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(health_check_default_conf, sort_keys=False))
        
        shutil.copy(health_check_java_class_default_path, health_check_java_class_injection_path)

        with open(schedule_injection_path, 'w') as injection_conf:
            injection_conf.write(yaml.dump(schedule_default_conf, sort_keys=False))
    else:
        sys.exit(">>>>[ctest_core] value injection for {} is not supported yet".format(project))
