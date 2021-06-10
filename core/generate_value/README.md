
# Generating Valid Values for Configuration Parameters

### Introduction

See [Generating Ctests - generating valid values](https://github.com/xlab-uiuc/openctest/blob/main/core/README.md#12-generating-parameter-sets-for-ctests).

### Instruction


*First*, prepare a `tsv` file containing the name, default value and description of each configuration parameter in the target project in `../default_configs/<project>-default.tsv`. The format is

```
parameter1	value1	desc1
parameter2	value2	desc2
```

This will be used for generating new valid values. We have provided such files for our supported projects.


*Second*, run `python3 value_generation.py <project>`. This script will generate 1-2 non-default values for each parameter based on information from `<project>-default.tsv`.

For example, you can generate values for parameters in `hadoop-common` with

```
python3 value_generation.py hadoop-common
```

Example standard output:
```
hadoop-common:
covered parameters: 67
values generated: 200
total params: 90
coverage: 0.7444444444444445
```

### Result

The generated value result will be in `<project>-generated-values.tsv` (tab-seperated), which looks like

```
hadoop.http.filter.initializers	SKIP	SKIP
hadoop.security.group.mapping	SKIP	SKIP
hadoop.security.dns.log-slow-lookups.threshold.ms	500	2000
hadoop.security.groups.cache.secs	150	600
hadoop.security.groups.cache.warn.after.ms	2500	10000
hadoop.security.groups.cache.background.reload.threads	1	6
```
Note that `SKIP` is a placeholder where we cannot generate a valid value. 


### [Optional] Configure the script

For some parameter types, users can change the candidate values for different parameter types by editing `config.py`. 

For example, to change the candidate values for `port` type parameters, users can modify
```
PORTS = ["3000", "3001"] # put the port values you want to test
```

Then the script will use port numbers provided by users to generate valid values for port parameters.


### Directory Structure

- value_generation.py: generate values for configuration parameters
- config.py: modify this to customize the generated values
