"""specify the program input"""

p_input = {
    # run mode
    "run_mode": "generate_ctest", # string
    # name of the project, i.e. hadoop-common, hadoop-hdfs, see constant.py
    "project": "redisson", # string
    # path to param -> tests json mapping
    "mapping_path": "../../data/ctest_mapping/opensource-redisson.json", # string
    # good values of params tests will be run against
    "param_value_tsv": "../default_configs/redisson-default.tsv", # string
    # display the terminal output live, without saving any results
    "display_mode": False, # bool
    # whether to use mvn test or mvn surefire:test
    "use_surefire": True, # bool
    # additional maven options to pass to `mvn surefire:test -Dtest=...`
    "maven_args": ["-DredisBinary=/usr/bin/redis-server"], # list of strings, each element is an option
    # timeout on the mvn test command
    "cmd_timeout": None, # int
}

assert p_input["project"] \
    and p_input["mapping_path"] \
    and p_input["param_value_tsv"], ">>>>[ctest_core] please specify input"
assert p_input["run_mode"] == "generate_ctest", ">>>>[ctest_core] please specify run_mode"
