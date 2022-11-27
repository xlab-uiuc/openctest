"""specify the program input"""

p_input = {
    # run mode
    "run_mode": "generate_ctest", # string
    # name of the project, i.e. hadoop-common, hadoop-hdfs, see constant.py
    "project": "kafka-core", # string
    # path to param -> tests json mapping
    "mapping_path": "../../data/ctest_mapping/opensource-kafka-core.json", # string
    # good values of params tests will be run against
    "param_value_tsv": "sample-kafka-core.tsv", # string
    # display the terminal output live, without saving any results
    "display_mode": False, # bool
    # Add a new boolean to handle gradle projects. If this is true, it will ignore the mvn related fields.
    "is_gradle": True, # bool
    # whether to use mvn test or mvn surefire:test
    "use_surefire": True, # bool
    # additional maven options to pass to `mvn surefire:test -Dtest=...`
    "maven_args": [], # list of strings, each element is an option
    # timeout on the mvn test command
    "cmd_timeout": None, # int
}

assert p_input["project"] \
    and p_input["mapping_path"] \
    and p_input["param_value_tsv"], ">>>>[ctest_core] please specify input"
assert p_input["run_mode"] == "generate_ctest", ">>>>[ctest_core] please specify run_mode"
