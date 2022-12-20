# Support New Project
Using the following instructions to add support for new project.

## Gather Param_Test Mapping
- If you have not generated the `param_unset_getter_map.json` or `ctests-<project>.json`, please refer to `identify_param` and `generate_ctest` module to generate it.
- Create a new directory under [supported](../resources/supported/) directory named after the target project.
    - If the target project is a submodule of a larger project, it is recommended to name the directory as `ParentModule-SubModule`, for example, `redisson-redisson`. Unless, the name of submodule is unique and self-explanatory, for example, `hadoop-hdfs`.
- Put a copy of `param_unset_getter_map.json` or `ctests-<project>.json` in the new created directory.

## Instrument Target Project
- You may need to modify the source code of target project, so the target project will load the modified configuration values when it is running.
    - One way is to use the project build-in function to load modified configuration files during runtime. Check out example [git patch](../../patch/hadoop-common/interception.patch).
    - Another way is to first load the default configuration values as a Map object then load the modified configuration files as another Map object, and merge them together, then pass the merged one into downstream operation.
- Pack the modification as a git patch for future reference.

## Implement CTest Logic
This framework will do the following:
- extract configuration diff `D` of the specified configuration file.
- select the mapped ctests for configuration parameters in `D`.
- run selected ctests against configuration values in `D`.
- collect the test result for the specified configuration file.

Some operations will be handled by the framework internally, but you have to implement project specific logic:
- Create a new java file under [supported](../src/main/java/uiuc/xlab/openctest/runctest/supported/) directory named after the new supported project/module.
- Create new entry in [CTestSupported](../src/main/java/uiuc/xlab/openctest/runctest/supported/CTestSupported.java) class.
- Inherit from [CTestRunnable](../src/main/java/uiuc/xlab/openctest/runctest/interfaces/CTestRunnable.java) interface and implement required methods.
- Note on implementing `runCTest` method:
    - One way is to use third-party framework to run the tests in the target project. For example, [maven-invoker](https://mvnrepository.com/artifact/org.apache.maven.shared/maven-invoker) for maven-based projects, such as `Hadoop`, or [ant](https://mvnrepository.com/artifact/org.apache.ant/ant) for ant-based projects, such as `Cassandra`.
    - Another way is to spawn additional process and run command directly using Java's `Process` class.
