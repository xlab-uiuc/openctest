"""inject parameter, values into sw config"""

import sys
import xml.etree.ElementTree as ET

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
    else:
        sys.exit(">>>>[ctest_core] value injection for {} is not supported yet".format(project))
