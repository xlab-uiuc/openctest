# Generating Ctests

### Description

See **[Generating Parameter Sets for Ctests](https://github.com/xlab-uiuc/openctest/tree/main/core#12-generating-parameter-sets-for-ctests)**.

### Instruction

*First*, specify data input in `program_input.py`. For example,

```python
p_input = {
    "run_mode": "generate_ctest",
    "project": "hadoop-common",
    "mapping_path": "../../data/ctest_mapping/opensource-hadoop-common.json",
    "param_value_tsv": "sample-hadoop-common.tsv",
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

*Second*, run `./generate_ctest.sh`.

For Forem,
```
python3 gen_ctest.py <params_file> <test_cases_file> <report_file>
```


### Result

**Test result** is collected per parameter and stored in `test_result/<project>/test_reuslt_<parameter>.tsv`.  `test_result/<project>/missing_test_<parameter>.tsv` stores tests whose Maven test report was missing while the test result is being collected.

Test result file is formatted as
```
parameter	test1	value1	test_result	testcase_time	
parameter	test2	value1	test_result	testcase_time
...
parameter	test1	value2	test_result	testcase_time
...
```

`test_result` is `p` if test passed, otherwise `f`. Skipped tests should be filtered automatically in the [Identifying Parameters Exercised in Tests](https://github.com/xlab-uiuc/openctest/tree/main/core#11-identifying-parameters-exercised-in-tests) step.

**Ctest mapping** is generated based on all the test result files in `test_result/<project>`. It is stored in `ctest_mapping/ctests-<project>.json` with format:
```
{
  parameter1: [
    ctest1,
    ctest2,
    ...
  ],
  parameter2: [
    ctest3,
    ctest4,
    ...
  ],
  ...
}
```

### Directory Structure

- program_input.py: specify data input for generating ctests, i.e., "parameter -> tests" json mapping, valid-value tsv file.
- generate_ctest.sh: generate ctests for specified project.
- main.py: main function to run tests against generated valid values and collect test results
- identify.py: identify ctests from collected test results.
