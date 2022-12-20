# Running CTest
Using this module to run generated ctests against configuration files of supported projects.

It will do the following:
- extract configuration diff `D` of the specified configuration file.
- select the mapped ctests for configuration parameters in `D`.
- run selected ctests against configuration values in `D`.
- collect the test result for the specified configuration file.

## Prerequisite
- Java 11
- Maven 3

## How To Set Up Target Project
Check out setup instructions and more general information for specific project in [here](./resources/supported/README.md)

## How To Run CTest
To run the CTest, you need to pass following parameters:

`project.name`
- required
- the name of the target project, check out [here](./resources/supported/README.md)

`project.path`
- required
- the relative or absolute path to the target project.
- note: if the target project is a submodule of a larger parent project, you have to specify the path to the submodule not the parent project. For example, if the target project is the hadoop-common module in the hadoop, use `.../hadoop/hadoop-common-project/hadoop-common`

`mapping.path`
- required
- the relative or absolute path to the `param_unset_getter_map.json` or `ctests-<project>.json`

`conf.pairs`
- a list of modified configuration parameter-value pairs, separated by `,`
- note: if `conf.file` is not specified, this parameter must be set.
- note: for target projects accepting complex configurations, such as nested values, you need to use the `conf.file` parameter

`conf.file`
- the relative or absolute path to a `YAML` file containing modified configuration values
- note: if `conf.pairs` is not specified, this parameter must be set

`test.methods`
- a list of tests that you want to test, separated by `,`
- note: if `test.file` is not specified, this parameter must be set

`test.file`
- the relative or absolute path to a `TXT` file containing all tests that you want to test, separated by new line
- note: if `test.methods` is not specified, this parameter must be set

`project.props`
- a list of command line properties that you want to pass to the target project, separated by `,`
- note: generally optional, please check the `README` of specific project for required command line properties

`project.args`
- a list of command line arguments that you want to pass to the target project, separated by `,`
- note: generally optional, please check the `README` of specific project for required command line arguments

### Command Examples
Example with 2 Success and 1 Skip. `testCedeActive` is skipped because it is not affected by the modified configuration.
```
mvn exec:java -q \
-Dproject.name=hadoop-common \
-Dproject.path=app/hadoop/hadoop-common-project/hadoop-common \
-Dmapping.path=resources/supported/hadoop-common/param_unset_getter_map.json \
-Dconf.pairs=hadoop.security.crypto.jce.provider=SunJCE,hadoop.security.crypto.cipher.suite=AES/CTR/NoPadding \
-Dtest.methods=org.apache.hadoop.crypto.TestCryptoStreams#testAvailable,org.apache.hadoop.crypto.TestCryptoStreamsNormal#testSkip,org.apache.hadoop.ha.TestZKFailoverController#testCedeActive \
-Dproject.props=use.surefire=true \
-Dproject.args=-q
```

Example with 1 Success and 1 Fail. `testCqlBatch_MultipleTablesAuditing` is failed because `num_tokens must be >= 1`
```
mvn exec:java -q \
-Dproject.name=cassandra \
-Dproject.path=app/cassandra \
-Dmapping.path=resources/supported/cassandra/param_unset_getter_map.json \
-Dconf.file=examples/example-config.yaml \
-Dtest.file=examples/example-test.txt \
-Dproject.props=use.jdk11=true
```

## How To Support New Project
Check out instructions in [here](./docs/Support-New-Project.md)
