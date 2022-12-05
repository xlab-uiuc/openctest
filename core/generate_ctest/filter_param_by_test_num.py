## By Oscar Chen and Chris Shen from CS527, Fall 2022 
## This program will filter the params with number of test reference in between min and max
## The selected params will be saved in {project}.tsv in same directory
## Fill free to modify min and max to what you need
## File required: openctest/data/ctest_mapping/opensource-{project}.json
##                openctest/core/generate_value/{project}-generated-values.tsv
import json
from program_input import p_input
min = 0
max = 50
j = json.load(open("../../data/ctest_mapping/opensource-"+p_input["project"]+".json"))
w = open(p_input["project"]+".tsv", "w")
for p in open("../generate_value/"+p_input["project"]+"-generated-values.tsv").readlines():
    key = p.split("\t")[0]
    if key in j.keys() and (len(j[key]) >= min) and (len(j[key]) < max):
        w.write(p)