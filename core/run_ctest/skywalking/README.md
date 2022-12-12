# Running CTests for Apache Skywalking

**core/run_ctest/skywalking is used to run a single test case against a injected config file**

```shell
# Switch to the core/run_ctest/skywalking directory
cd <openctest dir>core/run_ctest/skywalking

# Build the project to generate the target/ctest-runner-1.0-SNAPSHOT-jar-with-dependencies.jar
mvn clean package 

# Switch to the instrumented apache skywalking directory
cd /home/skywalking

# Run the jar by providing the following inputs
# 1. Source directory containing the overridden file (Example : core/run_ctest/skywalking/sample-skywalking) 
# 2. Source file name containing the overridden param values (Example : core/run_ctest/skywalking/sample-skywalking/application.yml)
# 3. Module containing the test case
# 4. Test case

java -jar <openctest dir>core/run_ctest/skywalking/target/ctest-runner-1.0-SNAPSHOT-jar-with-dependencies.jar core/run_ctest/skywalking/sample-skywalking application2.yml oap-server/server-configuration/configuration-zookeeper org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated
```

## Results 

The test case will be executed with the overridden configs present in the input file.