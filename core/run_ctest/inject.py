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
    elif project in [ROCKETMQ]:
        for inject_path in INJECTION_PATH[project]:
            print(">>>>[ctest_core] injecting into file: {}".format(inject_path))
            file = open(inject_path, "w")
            # '10.10.104.*','192.168.0.*'
            dict_global_addr = {'globalWhiteRemoteAddresses':[]}
            # {"accessKey":"rocketmq2","secretKey":12345678,"whiteRemoteAddress":"192.168.1.*","admin":True}
            dict_accounts = {'accounts':[{"accessKey":"rocketmq","secretKey":1234567,"whiteRemoteAddress":"192.168.0.*","admin":False}]}
    
            for p, v in param_value_pairs.items():
                if dict_accounts['accounts'][0].__contains__(p):
                    if v == 'true':
                        v = True
                    elif v == 'false':
                        v = False 
                    dict_accounts['accounts'][0][p] = v
                else:
                    if p in ['defaultTopicPerm', 'defaultGroupPerm']:
                        dict_accounts['accounts'][0][p] = v
                    elif p in ['topicPerms', 'groupPerms']:
                        dict_accounts['accounts'][0][p] = []
                        dict_accounts['accounts'][0][p].append(v)
                    elif p == 'globalWhiteAddrs':
                        dict_global_addr['globalWhiteRemoteAddresses'].append(v)
                        
            if not dict_global_addr['globalWhiteRemoteAddresses']:
                dict_global_addr['globalWhiteRemoteAddresses'] = ['10.10.103.*','192.168.0.*']
            yaml.dump(dict_global_addr, file)
            yaml.dump(dict_accounts, file)
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
    elif project in [ROCKETMQ]:
        for inject_path in INJECTION_PATH[project]:
            file = open(inject_path, "w")
            file.write("\n")
            file.close()
    else:
        sys.exit(">>>>[ctest_core] value injection for {} is not supported yet".format(project))
