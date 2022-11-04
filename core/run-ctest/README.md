## Prerequisite
- Java 11
- Maven 3

## How To Set Up Target Project
Check out instructions for specific project in [here](./resources/supported/)

## How To Run CTest
To run the CTest, you need to pass following parameters:

`project.name`
- required
- the name of the target project, check out [here](./resources/supported/)

`project.path`
- required
- the relative path to the target project. If the target project is a submodule of a larger parent project, you have to specify the path to the submodule not the parent project

`mapping.path`
- required
- the relative path to the `param_unset_getter_map.json`

`conf.pairs`
- if `conf.file` is not specified, this parameter must be set
- a list of modified configuration parameter-value pairs, separated by `,`

`conf.file`
- if `conf.pairs` is not specified, this parameter must be set
- the relative path to a `.properties` file containing modified configuration parameter-value pairs

`test.methods`
- if `test.file` is not specified, this parameter must be set
- a list of tests that you want to test, separated by `,`

`test.file`
- if `test.methods` is not specified, this parameter must be set
- the relative path to a `.txt` file containing all tests that you want to test

`project.props`
- optional
- a list of command line properties that you want to pass to the target project, separated by `,`

`project.args`
- optional
- a list of command line arguments that you want to pass to the target project, separated by `,`

## Command Examples
Example with 2 Success and 1 Skip. `testCedeActive` is skipped because it is not affected by the modified configuration.
```
mvn exec:java -q \
-Dproject.name=hadoop-common \
-Dproject.path=app/hadoop/hadoop-common-project/hadoop-common \
-Dmapping.path=resources/supported/hadoop-common/param_unset_getter_map.json \
-Dconf.pairs=hadoop.security.crypto.jce.provider=SunJCE,hadoop.security.crypto.cipher.suite=AES/CTR/NoPadding \
-Dtest.methods=org.apache.hadoop.crypto.TestCryptoStreams#testAvailable,org.apache.hadoop.crypto.TestCryptoStreamsNormal#testSkip,org.apache.hadoop.ha.TestZKFailoverController#testCedeActive \
-Dproject.props=maven.antrun.skip=true,use.surefire=true \
-Dproject.args=-q
```

Example with 1 Success and 1 Fail. `testCqlBatch_MultipleTablesAuditing` is failed because `num_tokens must be >= 1`.
```
mvn exec:java -q \
-Dproject.name=cassandra \
-Dproject.path=app/cassandra \
-Dmapping.path=resources/supported/cassandra/param_unset_getter_map.json \
-Dconf.file=examples/modified-config.properties \
-Dtest.file=examples/to-be-tested-tests.txt \
-Dproject.props=use.jdk11=true
```

## How To Support New Project
Check out instructions in [here](./docs/Support-New-Project.md)