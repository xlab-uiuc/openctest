## By Oscar Chen and Chris Shen from CS527, Fall 2022 
## This program will generate a "{project}_test_num_on_param.txt" file in same directory that records the number of test methods related to each param.
## In each line of the generated file, the number of tests methods always comes before the param name
## File required: openctest/data/ctest_mapping/opensource-{project}.json
##                openctest/core/generate_value/{project}-generated-values.tsv
import json
from program_input import p_input
j = json.load(open("../../data/ctest_mapping/opensource-"+p_input["project"]+".json"))
c = {}
for p in open("../generate_value/"+p_input["project"]+"-generated-values.tsv").readlines():
    key = p.split("\t")[0]
    if (key in j.keys()):
        c.update({key: len(j[key])})
with open(p_input["project"]+"_test_num_on_param.txt", "w") as outfile:
    for k in c.keys():
        outfile.write(str(c[k])+"\t"+k+"\n")