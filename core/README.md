





# Ctest Core

## Overview

A prototype for generating and running ctests. Below are the projects we currently support:

- Hadoop 2.8.5: `hadoop-common`, `hadoop-hdfs`.
- Hbase 2.2.2: `hbase-server`.
- ZooKeeper 3.5.6: `zookeeper-server`.
- Alluxio 2.1.0: `core`.
- Superset 3.0.2: `superset-websocket`.

We also provided our instrumented versions of the above projects:

- Hadoop 2.8.5: https://github.com/xlab-uiuc/hadoop
- Hbase 2.2.2: https://github.com/xlab-uiuc/hbase
- ZooKeeper 3.5.6: https://github.com/xlab-uiuc/zookeeper
- Alluxio 2.1.0: https://github.com/xlab-uiuc/alluxio
- Superset 3.0.2: https://github.com/ishitakarna/superset

Our instrumented version projects have two branches: 
- `ctest-injection`: branch with "Intercept Configuration API" instrumentation (See `ADDING_NEW_PROJECT.md`). This branch is used by `generate_ctest` and `run_ctest`.
- `ctest-logging`: branch with "Logging Configuration API" instrumentation (See `ADDING_NEW_PROJECT.md`). This branch is used by `identify_param`.

**If you want to use `openctest` on a new project, please refer to `ADDING_NEW_PROJECT.md`**

## Setup

### 1. Environment

There are two options to set up the environment for the currently supported projects.
You can either run ctests in the docker container provided by us, or directly set up your local environment.
Steps are shown below.

#### Option 1. Docker Container

After installing Docker, run `docker build --tag openctest .` to build the image.

Then, run `docker run -it openctest` to start the container from built the image.

In the container, you can generate and run ctests as shown below.

#### Option 2. Linux Ubuntu 18.04

Run `./setup_ubuntu.sh` or `sudo ./setup_ubuntu.sh`.

### 2. Target Project

To generate ctests or run ctest, you need to first clone the target project. 

**To add a new project**, please refer to `ADDING_NEW_PROJECT.md`.

**To use our currently supported projects**, do the following:

1. In `openctest/core`, run `./add_project.sh <main project>` to clone the project, switch to and build the branch `ctest-injection`. This branch will be later used by `generate_ctest` and `run_ctest`.
2. In `openctest/core/identify_param`, run `./add_project.sh <main project>` to clone the project, switch to and build the branch `ctest-logging`. This branch will be later used by `identify_param`.

`<main project>` can be `hadoop`, `hbase`, `zookeeper`, `alluxio`, or `superset`.

## Usage

### 1. Generating Ctests

To generate ctests for the target project,  follow the steps below:

#### 1.1 Identifying Parameters Exercised in Tests

Use **identify_param** to identify configuration parameters exercised by tests in the target project. It will do the following:

1. run tests in the instrumented target project.
2. parse the test log to identify parameters exercised in each test.
3. for each configuration parameter `p`, identify tests that reset the value of `p`, and exclude `p` from these tests' exercised parameter set.
4. generate a mapping where the keys are parameters, and values are lists of tests which exercise but not reset the parameters.

Please refer to the [identify_param](https://github.com/xlab-uiuc/openctest/tree/main/core/identify_param "identify_param") folder for instructions.

#### 1.2 Generating Parameter Sets for Ctests

*First*, use **generate_value** to automatically generate up to three different valid values for each parameter. The generated valid values are used to exclude tests hardcoded to specific parameter values (These tests cannot be transformed into ctests as they will fail on any other valid but different values), Please refer to the [generate_value](https://github.com/xlab-uiuc/openctest/tree/main/core/generate_value "generate_value") folder for instructions.

*Second*, use **generate_ctest** to automatically generate ctests. It will do the following:

1. for each parameter identified in **1.1**, run the mapped tests against generated valid values.
2. parse test result for each parameter into `tsv` files.
3. automatically identify ctests (tests that passed on all valid values) for each parameter from the test result.
4. output the generated "parameters -> ctests" mapping into a `json` file.

Please refer to the [generate_ctest](https://github.com/xlab-uiuc/openctest/tree/main/core/generate_ctest "generate_ctest") folder for instructions.

### 2. Running Ctests

Use **run_ctest** to run generated ctests against configuration files. It will do the following:

 1. extract configuration diff `D` of the specified configuration file.
 2. select the mapped ctests for configuration parameters in `D`.
 3. run selected ctests against configuration values in `D`.
 4. collect the test result for the specified configuration file.

Please refer to the [run_ctest](https://github.com/xlab-uiuc/openctest/tree/main/core/run_ctest "run_ctest") folder for instructions.
