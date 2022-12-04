## This program helps create an indented version of ctests-{project}.json
import json
from program_input import p_input
j = json.load(open("ctest_mapping/ctests-"+p_input["project"]+".json"))
json.dump(j, open("ctest_mapping/ctests-"+p_input["project"]+"-indent.json", "w"), indent=4)