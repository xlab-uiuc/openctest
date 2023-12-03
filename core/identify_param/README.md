
# Identifying Parameters Exercised in Tests

### Description

See [Identifying Parameters Exercised in Tests](https://github.com/xlab-uiuc/openctest/tree/main/core#11-identifying-parameters-exercised-in-tests)


### Instruction

*First*, clone and build the target project following *Setup  - 2. Target Project* in `../README.md`.

*Second*, run `./identify_param.sh <project>` to generate the mapping. For example, 

```
./identify_param.sh hadoop-common
``` 

For Forem,


```
python3 identify_params.py log/


python3 param_to_test.py log/
```


Generates `result_mapping.json`, `all_params.txt`, `all_test_cases.txt`, and `param_to_test_cases_mapping.json`


### Result

The mapping file is stored in `results/<project>/param_unset_getter_map.json`. The mapping maps from each parameter to a list of tests which:
- called configuration API `GET` on this parameter
- did not call configuration API `SET` which re-assigns/resets the value of this parameter in test code


#### Intermediate Result

There are intermediate results generated from `identify_param.sh`. These result will not be used later, but maybe helpful as a reference.

`results/hadoop-common/logs` shows "which test called `GET` or `SET` on which parameter".  For example, `getter-record` shows each test and the parameters which it called `GET` on, i.e.
```
test1 fs.defaultFS
test2 hadoop.security.dns.log-slow-lookups.enabled
test3 hadoop.security.dns.log-slow-lookups.threshold.ms
```
This means 
- `test1 GET fs.defaultFS`
- `test2 GET hadoop.security.dns.log-slow-lookups.enabled`
- `test3 GET hadoop.security.dns.log-slow-lookups.threshold.ms`

### Directory Structure

- add_project.sh: install the project with instrumented configuration API
- identify_param.sh: identify the parameters exercised by each test by calling `runner.py` and `collector.py`
- runner.py: run each test and generate the log of instrumented configuration API
- collector.py: parse the log and identify the parameters
