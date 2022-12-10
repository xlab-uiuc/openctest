"""inject parameter, values into sw config"""

import shutil
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
    elif project in [SPARK]:
        for inject_path in INJECTION_PATH[project]:
            back_up = inject_path + "/back_up.xml"
            inject_path = inject_path + "/pom.xml"
            shutil.copyfile(inject_path, back_up)
            print(">>>>[ctest_core] injecting into file: {}".format(inject_path))
            tree = ET.parse(inject_path)
            pom = tree.getroot()
            namespace = pom.tag.split('{')[1].split('}')[0]
            # for reading
            namespace_mapping = {'mvnns': namespace}
            # for writing: otherwise 'xmlns:ns0' will be used instead of the standard xml namespace 'xmlns'
            ET.register_namespace('', namespace)
            ns = "{http://maven.apache.org/POM/4.0.0}"
            for child in pom.findall("%sbuild/%spluginManagement/%splugins/%splugin" % (ns, ns, ns, ns)):
                gid = child.find("%sgroupId" % ns)
                if gid.text == "org.scalatest":
                    child = child.find("%sconfiguration/%ssystemProperties" % (ns, ns))
                    for p, v in param_value_pairs.items():
                        sub = ET.SubElement(child, '%s%s' % (ns, p))
                        sub.text = v
            tree.write(inject_path, encoding='utf-8')
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
    elif project in [SPARK]:
        for inject_path in INJECTION_PATH[project]:
            back_up = inject_path + "/back_up.xml"
            inject_path = inject_path + "/pom.xml"
            shutil.copyfile(back_up, inject_path)
    else:
        sys.exit(">>>>[ctest_core] value injection for {} is not supported yet".format(project))
