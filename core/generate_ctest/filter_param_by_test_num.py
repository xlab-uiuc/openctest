## This program will automatically filter the params with number of test reference in between min and max
## Fill free to modify min and max to what you need
import json
from program_input import p_input
count = 30
min = 0
max = 32
j = json.load(open("../../data/ctest_mapping/opensource-"+p_input["project"]+".json"))
w = open(p_input["project"]+".tsv", "w")
for p in open("../generate_value/"+p_input["project"]+"-generated-values.tsv").readlines():
    key = p.split("\t")[0]
    if key in j.keys() and (len(j[key]) >= min) and (len(j[key]) < max) and count > 0:
        w.write(p)
        count -= 1
