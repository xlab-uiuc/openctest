# Generating Parameter Sets for Apache Skywalking

**generate_ctest is used to automatically generate ctests**

```shell
# Switch to the generate_ctest/skywalking directory
cd <openctest dir>/core/generate_ctest/skywalking

# Build the project to generate the target/ctest-runner-1.0-SNAPSHOT-jar-with-dependencies.jar
mvn clean package 

# Switch to the instrumented apache skywalking directory
cd /home/skywalking

# Run the jar by providing the following inputs
# 1. temp directory which will contain the files needed for this run 
# 2. File core/identify_param/results/skywalking/test_to_param_flat.json from the execution of the core/identify_param/skywalking step
# 3. File skywalking-generated-values.tsv from the execution of the core/generate_value step
# 4. Result directory which will contain the results of the execution
java -jar <openctest dir>/core/generate_ctest/skywalking/target/ctest-runner-1.0-SNAPSHOT-jar-with-dependencies.jar <dir>/tmp <dir>/test-to-config-flat.txt <dir>/skywalking-generated-values.tsv <dir>/resultDir
```

## Results 

2 files are generated as a result of this run 

1. Generates the `core/generate_ctest/ctest_mapping/ctests-skywalking.json` file
```json
{
  "configuration.apollo.period": [
    "org.apache.skywalking.oap.server.configuration.apollo.ITApolloConfigurationTest#shouldReadUpdated",
    "org.apache.skywalking.oap.server.configuration.apollo.ITApolloConfigurationTest#shouldReadUpdated4Group"
  ],
  "configuration.zookeeper.maxRetries": [
    "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated",
    "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated4GroupConfig"
  ],
  "configuration.zookeeper.period": [
    "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated",
    "org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated4GroupConfig"
  ]...
}

```

2. Execution results for each case in the tab separated format
   
Param Test Value p/f Time_in_ns
```json
services[0].duration    org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testDefaultSampleRateNotify     15000   p       9188519779
services[0].duration    org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testDefaultSampleRateNotify     60000   p       9179170267
```
