# Running Ctests

### Description

See **[Running Ctests](https://github.com/xlab-uiuc/openctest/tree/main/core#2-running-ctests)**.

### Instruction

*First*, specify data input in `program_input.py`. For example,

```python
p_input = {
    "run_mode": "run_ctest",
    "project": "hadoop-common",
    "mapping_path": "../../data/ctest_mapping/opensource-hadoop-common.json",
    "conf_file_dir": "sample-hadoop-common",
    "display_mode": False,
    "use_surefire": True,
    "maven_args": [],
    "cmd_timeout": None,
}
```
*For `alluxio-core`, please specify
```
"maven_args": ["-DfailIfNoTests=false"]
```

*Second*, run `./run_ctest.sh`. Each correctly formatted configuration file in the `conf_file_dir` folder will be tested sequentially.

### Result

**Test result** is collected per configuration file and stored in `run_ctest_result/<project>/test_reuslt_<conf_file_name>.tsv`.  
`run_ctest_result/<project>/missing_test_<conf_file_name>.tsv` stores ctests whose Maven test report was missing while the test result is being collected.

Test result file is formatted as
```
ctest1	test_result	testcase_time	
ctest2	test_result	testcase_time
...
```

`test_result` is `p` if ctest passed, otherwise `f`. Skipped tests should be filtered automatically during [ctest generation](https://github.com/xlab-uiuc/openctest/tree/main/core#1-generating-ctests).


### Directory Structure

- program_input.py: specify data input for generating ctests, i.e., configuration files to be tested, "parameter -> ctests" json mapping.
- run_ctest.sh: run ctests for specified project.
- main.py: main function to run ctests against configuration files and collect test results
