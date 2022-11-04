# Support New Project
Using the following instructions to add support for new project.

## Gather Param_Test Mapping
- If you have not generated the `param_unset_getter_map.json`, please refer to `identify_param` submodule to generate it.
- Create a new directory under [supported](../resources/supported/) named after the target project.
    - If the target project is a submodule of a larger project, it is recommended to name the directory as `ParentModule-SubModule`, for example, `redisson-redisson`. Unless, the name of submodule is unique and self-explanatory, for example, `hadoop-hdfs`.
- Put a copy of `param_unset_getter_map.json` in the new created directory.

## Instrument Target Project
- You are required to modify the target project, so the target project will load the modified configuration values when the project is running.
    - One way is to use the project build-in function to load modified configuration files during runtime. Check out example [git patch](../resources/supported/hadoop-common/ctest-injection.patch).
    - Another way is to load the modified configuration files as a Map object during runtime, and merge it with default configuration Map object, then pass the merged one into downstream operation. Check out example [git patch](../resources/supported/cassandra/ctest-injection.patch)

## Implement CTest Logic
- Create a new java file under [supported](../src/main/java/uiuc/xlab/openctest/runctest/supported/) directory.
- Create new entry in [CTestSupported](../src/main/java/uiuc/xlab/openctest/runctest/supported/CTestSupported.java) class.
- Inherit from `CTestRunnable` and implement required methods.
- Note on implementing `runCTest` method
    - One way is to use third-party framework to run the tests in the target project. For example, [maven-invoker](https://mvnrepository.com/artifact/org.apache.maven.shared/maven-invoker) for maven-based project, such as `Hadoop`, or [ant](https://mvnrepository.com/artifact/org.apache.ant/ant) for ant-based project, such as `Cassandra`.
    - Another way is to create additional process and run command directly using Java's `Process` class.