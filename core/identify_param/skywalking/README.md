# Building & Instrumenting Apache Skywalking project

The below steps are automated in the script `core/add_project_skywalking.sh`

1. Login to VM and create a new directory
2. Run the command
```shell
# Latest source code release can be found in https://skywalking.apache.org/downloads/
wget https://dlcdn.apache.org/skywalking/9.2.0/apache-skywalking-apm-9.2.0-src.tgz
```
3. Unzip the file
```shell
tar zxvf apache-skywalking-apm-9.2.0-src.tgz
```

4. Apply the instrumentation patch from the openctest repo (skywalking.patch contains both logging and interception instrumentation)
```shell
git apply <openctest dir>/core/patch/skywalking/skywalking.patch
```
5. Switch to the backend directory
```shell
cd oap-server
```
6. Build the project
```shell
mvn clean install -DskipTests
```


# Identifying Parameters in Apache Skywalking

**Use identify_param to identify configuration parameters exercised by tests in the target project.**

## Details
1. Run tests in the instrumented target project.
2. Parse the test log to identify parameters exercised in each test.
3. For each configuration parameter p, identify tests that reset the value of p, and exclude p from these tests' exercised parameter set.
4. Generate a mapping where the keys are parameters, and values are lists of tests which exercise but not reset the parameters.

```shell
# Switch to the identify_param/skywalking directory
cd <openctest dir>/core/identify_param/skywalking

# Build the project to generate the target/ctest-mapper-1.0-SNAPSHOT-jar-with-dependencies.jar 
mvn clean package 

# Switch to the instrumented apache skywalking directory
cd /home/skywalking

# Run the jar by providing the output directory  
java -jar <openctest dir>/core/identify_param/skywalking/target/ctest-mapper-1.0-SNAPSHOT-jar-with-dependencies.jar /home/output/
```

## Results 

3 files are generated as a result of this run 

1. Test case to config map `core/identify_param/results/skywalking/test_to_param.json`
```json
{
  "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated4GroupConfig": {
    "configuration": {
      "zookeeper": {
        "namespace": "/default",
        "hostPort": "localhost:49189",
        "period": "1",
        "baseSleepTimeMs": "1000",
        "maxRetries": "3"
      }
    }
  },
  "org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testStaticConfigInit": {
    "default": {
      "duration": "-1",
      "rate": "10000"
    },
    "services": [
      {
        "duration": "30000",
        "rate": "2000",
        "name": "name2"
      },
      {
        "duration": "20000",
        "rate": "1000",
        "name": "name1"
      }
    ]
  },...
}
```

2. Generate the test case to config flat map `core/identify_param/results/skywalking/test_to_param_flat.json`
```json
{
  "org.apache.skywalking.oap.server.configuration.apollo.ITApolloConfigurationTest#shouldReadUpdated": [
    "configuration.apollo.apolloMeta",
    "configuration.apollo.appId",
    "configuration.apollo.period",
    "configuration.apollo.apolloEnv",
    "configuration.apollo.apolloCluster"
  ],
  "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated": [
    "configuration.zookeeper.maxRetries",
    "configuration.zookeeper.period",
    "configuration.zookeeper.hostPort",
    "configuration.zookeeper.baseSleepTimeMs",
    "configuration.zookeeper.namespace"
  ]...
}
```

3. Generates the flat config `core/default_configs/skywalking-default.tsv` from skywalking's hierarchy structure which can be used by the generate_value python code. This also supports array based configs.

```
configuration.apollo.apolloEnv	DEV	description
services[1].duration	20000	description
configuration.nacos.port	49317	description
configuration.zookeeper.hostPort	localhost:49315	description
configuration.nacos.username	nacos	description
```