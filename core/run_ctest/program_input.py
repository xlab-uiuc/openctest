"""specify the program input"""

p_input = {
    # run mode
    "run_mode": "run_ctest", # string
    # name of the project, i.e. hadoop-common, hadoop-hdfs
    "project": "cassandra", # string
    # path to param -> tests json mapping
    "mapping_path": "../identify_param/results/cassandra/param_unset_getter_map.json", # string
    # input directory hosting configuration files to be test, target-project-format specific
    "conf_file_dir": "test_cassandra", # string
    # display the terminal output live, without saving any results
    "display_mode": False, # bool
    # whether to use mvn test or mvn surefire:test
    "use_surefire": False, # bool
    # additional maven options to pass to `mvn surefire:test -Dtest=...`
    "maven_args": [], # list of strings, each element is an option
    # timeout on the mvn test command
    "cmd_timeout": None, # int
}

assert p_input["project"] \
    and p_input["mapping_path"] \
    and p_input["conf_file_dir"], ">>>>[ctest_core] please specify input"
assert p_input["run_mode"] == "run_ctest", ">>>>[ctest_core] please specify run_mode"
