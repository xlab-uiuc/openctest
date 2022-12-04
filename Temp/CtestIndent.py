import json
j = json.load(open("opensource-hadoop-hdfs-rbf.json"))
w = open("../core/generate_ctest/hadoop-hdfs-rbf.tsv", "w")
for p in open("hadoop-hdfs-rbf-generated-values.tsv").readlines():
    key = p.split("\t")[0]
    if key in j.keys() and (len(j[key]) < 50):
        w.write(p)

# import json
# j = json.load(open("opensource-hadoop-hdfs-rbf.json"))
# c = {}
# for p in open("hadoop-hdfs-rbf-generated-values.tsv").readlines():
#     key = p.split("\t")[0]
#     if (key in j.keys()):
#         c.update({key: len(j[key])})
# print(p)
# with open("counts.txt", "w") as outfile:
#     for k in c.keys():
#         if c[k] < 50:
#             outfile.write(str(c[k])+"\t"+k+"\n")