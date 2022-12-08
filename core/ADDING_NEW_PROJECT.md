
# Adding New Project

If you want to add a new project into the `openctest` framework. You need to do the following steps.

## 1. Instrument Target Project


**Because intercepting and logging the configuration APIs are for two independent purposes -- and their outcome are independent of each other, it is **highly recommended** to create a separate Git branch for each case.**

### 1.1 Intercept Configuration API (Paper Section 4.1)

Intercept the configuration API to overwrite configuration values in the final step of configuration loading. 

Specifically, create empty configuration file(s) in the project directory, and make sure the configuration API reads it in the final step of configuration loading. So when the test reads configuration values from the APIs, the values come from the configurations maintained by the ctest infrastructure. 

Intercept example in Hadoop: 
- [override configuration loading](https://github.com/xlab-uiuc/hadoop/commit/72a9e108e4c2bed13b43d8b4fbd3aa32e690447c#diff-16e961a312f55e9abdc96aa97dec8b284b79ab6d10ca6f2332c66a3f8aa96529)
- [the configuration file created for overriding](https://github.com/xlab-uiuc/hadoop/commit/72a9e108e4c2bed13b43d8b4fbd3aa32e690447c#diff-ad606c23074a9dff0050b0e57746fa6865c2151bcf940fda692d540dfde9b74f)

*This instrumentation is for generating and running ctests, and is needed by the `generate_ctest` and `run_ctest`.*

### 1.2 Logging Configuration API (Paper Section 4.2)

Identify and instrument the configuration GET and SET APIs which read and write configuration values. 

The instrumentation should log the GET and SET API usage on each exercised configuration parameter in a specific format.  So the ctest infrastructure can identify the parameters exercised in each test by running the tests and parsing the test logs.

GET instrumentation example: [hadoop-common](https://github.com/xlab-uiuc/hadoop/commit/cd8c6d5a2a11298731355c399a1e563234713e97#diff-16e961a312f55e9abdc96aa97dec8b284b79ab6d10ca6f2332c66a3f8aa96529R1104)

SET instrumentation example: [hadoop-common](https://github.com/xlab-uiuc/hadoop/commit/cd8c6d5a2a11298731355c399a1e563234713e97#diff-16e961a312f55e9abdc96aa97dec8b284b79ab6d10ca6f2332c66a3f8aa96529R1275)

*This instrumentation is for identifying parameters exercised by tests, and is needed by `identify_param`.* 


## 2. Add Supporting Code in `openctest`

### *2.0 Modify Maven pom.xml

The `maven-surefire-plugin` controls how the testing result is generated. Errors may be caused by discrepancies in the plugin version or test report format. It is important to ensure all supporting projects at least use the same plugin version. To do so, please modify the `pom.xml` in new project.

Sometimes, the locations that need to be changed maybe in multiple `pom` files. For example, for supporting project `hadoop-common`:
- `maven-surefire-plugin` version in [hadoop-common-project/hadoop-common/pom.xml](https://github.com/xlab-uiuc/hadoop/commit/cd8c6d5a2a11298731355c399a1e563234713e97#diff-32126fb088c541b420c68ba15eacf1f1a78d842f71595ba9ed1cbf25c530fa07 "hadoop-common-project/hadoop-common/pom.xml")
- `maven-surefire-plugin` report format in [pom.xml](https://github.com/xlab-uiuc/hadoop/commit/72a9e108e4c2bed13b43d8b4fbd3aa32e690447c#diff-9c5fb3d1b7e3b0f54bc5c4182965c4fe1f9023d449017cece3005d3f90e8e4d8 "pom.xml")

### 2.1 Collect Configuration Parameters and Tests

*First*, collect the name, default value (empty if no default value) and description of each configuration parameters in the project. Store the information in a `tsv` file in `default_configs`. For example: [hadoop-common-default.tsv](https://github.com/xlab-uiuc/openctest/blob/main/core/default_configs/hadoop-common-default.tsv).
 
 *Second*, collect the list of configuration parameter names and put them in `openctest/core/identify_param/results/<project>/conf_params.list`. 

*Third*, collect the list of exsiting tests in the project in the format of `testClass#testCase`. Put them in `openctest/core/identify_param/results/<project>/test_method_list.json`


### 2.2 Collect Deprecated Configuration Parameters

Collect a mapping from the deprecated parameter name to the new parameter name. Store the information in a `tsv` file in `deprecated_configs`. The format should be the deprecated parameter name followed by the new parameter name. For example: [hadoop.list](https://github.com/xlab-uiuc/openctest/blob/main/core/deprecated_configs/hadoop.list "hadoop.list")


### 2.3 Automate Project Installation

*First*, in `add_project.sh`, add a bash function for cloning, installing, and building the instrumented new project. And it should also automatically switch to the branch with instrumented code for *1.1 Intercept Configuration API*.

Example for the `hadoop-common` module in Hadoop:

```Bash
function setup_hadoop() {
  [ ! -d "app/ctest-hadoop" ] && git clone git@github.com:xlab-uiuc/hadoop.git app/ctest-hadoop
  cd app/ctest-hadoop
  git fetch && git checkout ctest-logging
  home_dir=$PWD
  cd $home_dir/hadoop-common-project/hadoop-common
  mvn clean install -DskipTests
  cd $home_dir/hadoop-hdfs-project/hadoop-hdfs-client
  mvn clean install -DskipTests
  cd $home_dir/hadoop-hdfs-project/hadoop-hdfs
  mvn package -DskipTests
}
```

*Second*, in `identify_param/add_project.sh`, add a bash function for cloning, installing, and building the instrumented new project. And it should also automatically switch to the branch with instrumented code for *1.2 Logging Configuration API*.

Using `hadoop-common` as an example, the difference is just:

```Bash
  ...
  git fetch && git checkout ctest-injection
  ...
```

### 2.3 Add Project Specific Constants

*First*, add project-specific constants to `ctest_const.py` for generating and running ctests. This constant file is used by `generate_ctest` and `run_ctest`. The constants include but not limited to 
- project name, like `hadoop-common`, `hadoop-hdfs`, etc 
- target project directory
- path(s) to generated surefire report
- path to default configuration parameters file (2.1)
- path to deprecated configuration parameters file (2.2)
- path(s) to configuration files that are used to intercept the configuration API (1.1), like [this](https://github.com/xlab-uiuc/openctest/blob/554fff9c017b99f482da8240f16a000cfd4eb82d/core/ctest_const.py#L82)

*Second*, add project-specific constants to `identify_param/constant.py` for identifying parameters exercised by tests. This constant file is used by `identify_param`. 
