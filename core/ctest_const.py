# constant for ctest generation

import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(CUR_DIR, "app")
GEN_CTEST_DIR = os.path.join(CUR_DIR, "generate_ctest")
RUN_CTEST_DIR = os.path.join(CUR_DIR, "run_ctest")

HCOMMON = "hadoop-common"
HDFS = "hadoop-hdfs"
HBASE = "hbase-server"
ZOOKEEPER = "zookeeper-server"
ALLUXIO = "alluxio-core"
DROPWIZARD = "dropwizard-health"

CTEST_HADOOP_DIR = os.path.join(APP_DIR, "ctest-hadoop")
CTEST_HBASE_DIR = os.path.join(APP_DIR, "ctest-hbase")
CTEST_ZK_DIR = os.path.join(APP_DIR, "ctest-zookeeper")
CTEST_ALLUXIO_DIR = os.path.join(APP_DIR, "ctest-alluxio")
CTEST_DROPWIZARD_DIR = os.path.join(APP_DIR, "ctest-dropwizard")

PROJECT_DIR = {
    HCOMMON: CTEST_HADOOP_DIR,
    HDFS: CTEST_HADOOP_DIR,
    HBASE: CTEST_HBASE_DIR,
    ZOOKEEPER: CTEST_ZK_DIR,
    ALLUXIO: CTEST_ALLUXIO_DIR,
    DROPWIZARD: CTEST_DROPWIZARD_DIR,
}


# the module of the project we experimented on
MODULE_SUBDIR = {
    HCOMMON: "hadoop-common-project/hadoop-common",
    HDFS: "hadoop-hdfs-project/hadoop-hdfs",
    HBASE: "hbase-server",
    ZOOKEEPER: "zookeeper-server",
    ALLUXIO: "core",
    DROPWIZARD: "dropwizard-health"
}


# surefire report
SUREFIRE_SUBDIR = "target/surefire-reports/"
SUREFIRE_XML = "TEST-{}.xml" # slot is the classname
SUREFIRE_TXT = "{}.txt" # testclass
SUREFIRE_OUTTXT = "{}-output.txt" #testclass 

SUREFIRE_DIR = {
    HCOMMON: [os.path.join(CTEST_HADOOP_DIR, MODULE_SUBDIR[HCOMMON], SUREFIRE_SUBDIR)],
    HDFS: [os.path.join(CTEST_HADOOP_DIR, MODULE_SUBDIR[HDFS], SUREFIRE_SUBDIR)],
    HBASE: [os.path.join(CTEST_HBASE_DIR, MODULE_SUBDIR[HBASE], SUREFIRE_SUBDIR)],
    ZOOKEEPER: [os.path.join(CTEST_ZK_DIR, MODULE_SUBDIR[ZOOKEEPER], SUREFIRE_SUBDIR)],
    ALLUXIO: [
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "base", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "client/fs", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "client/hdfs", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "common", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "server/common", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "server/proxy", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "server/worker", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, MODULE_SUBDIR[ALLUXIO], "server/master", SUREFIRE_SUBDIR),
    ],
    DROPWIZARD: [
        os.path.join(CTEST_DROPWIZARD_DIR, MODULE_SUBDIR[DROPWIZARD], SUREFIRE_SUBDIR)
    ]
}

# default or deprecate conf path
DEPRECATE_CONF_DIR = os.path.join(CUR_DIR, "deprecated_configs")
DEFAULT_CONF_DIR = os.path.join(CUR_DIR, "default_configs")

DEPRECATE_CONF_FILE = {
    HCOMMON: os.path.join(DEPRECATE_CONF_DIR, "hadoop.list"),
    HDFS: os.path.join(DEPRECATE_CONF_DIR, "hadoop.list")
}

DEFAULT_CONF_FILE = {
    HCOMMON: os.path.join(DEFAULT_CONF_DIR, HCOMMON + "-default.tsv"),
    HDFS: os.path.join(DEFAULT_CONF_DIR, HDFS + "-default.tsv"),
    HBASE: os.path.join(DEFAULT_CONF_DIR, HBASE + "-default.tsv"),
    ALLUXIO: os.path.join(DEFAULT_CONF_DIR, ALLUXIO + "-default.tsv"),
    ZOOKEEPER: os.path.join(DEFAULT_CONF_DIR, ZOOKEEPER + "-default.tsv"),
    DROPWIZARD: os.path.join(DEFAULT_CONF_DIR, DROPWIZARD + "-default.tsv")
}


# injecting config file location
INJECTION_PATH = {
    HCOMMON: [
        os.path.join(CTEST_HADOOP_DIR, "hadoop-common-project/hadoop-common/target/classes/core-ctest.xml")
    ],
    HDFS: [
        os.path.join(CTEST_HADOOP_DIR, "hadoop-hdfs-project/hadoop-hdfs/target/classes/core-ctest.xml"),
        os.path.join(CTEST_HADOOP_DIR, "hadoop-hdfs-project/hadoop-hdfs/target/classes/hdfs-ctest.xml")
    ],
    HBASE: [
        os.path.join(CTEST_HBASE_DIR, "hbase-server/target/classes/core-ctest.xml"),
        os.path.join(CTEST_HBASE_DIR, "hbase-server/target/classes/hbase-ctest.xml")
    ],
    ZOOKEEPER: [
        os.path.join(CTEST_ZK_DIR, "zookeeper-server/ctest.cfg")
    ],
    ALLUXIO: [
        os.path.join(CTEST_ALLUXIO_DIR, "core/alluxio-ctest.properties")
    ],
    DROPWIZARD: [
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/health-ctest.yml"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/healthCheck-ctest.yml"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/main/java/io/dropwizard/health/HealthCheckConfiguration.java"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/schedule-ctest.yml"),
    ],
}

# line number of the configuration
INJECTION_LINE_NUMBER = {
    DROPWIZARD: {
        "health.healthChecks.name" : 20,
        "health.healthChecks.type" : 24,
        "health.healthChecks.critical": 27,
        "health.healthChecks.initialState": 30,
    },
}

# code format of the configuration
INJECTION_CODE_FORMAT = {
    DROPWIZARD: {
        "health.healthChecks.name" : "\tprivate String name = \"{}\";\n",
        "health.healthChecks.type" : "\tprivate HealthCheckType type = {};\n",
        "health.healthChecks.critical": "\tprivate boolean critical = {};\n",
        "health.healthChecks.initialState": "\tprivate boolean initialState = {};\n",
    },
}

# files being used in the clean_conf_file step
INJECTION_CLEAN_UP_PATH = {
    DROPWIZARD: [
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/health.yml"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/healthCheck.yml"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/main/java/io/dropwizard/health/HealthCheckConfiguration.java.default"),
        os.path.join(CTEST_DROPWIZARD_DIR, "dropwizard-health/src/test/resources/yml/schedule.yml")
    ],
}


# constants for ctest generation -- generated test result file
GENCTEST_TR_DIR = os.path.join(GEN_CTEST_DIR, "test_result") # test result directory
os.makedirs(GENCTEST_TR_DIR, exist_ok=True)
TR_FILE = "test_result_{id}.tsv"
MT_FILE = "missing_test_{id}.list"
FAIL = "f" # test failed
PASS = "p" # test passed
GOOD_VAL = "GOOD"
BAD_VAL = "BAD"
SKIP_VAL = "SKIP"

CTESTS_DIR = os.path.join(GEN_CTEST_DIR, "ctest_mapping")
os.makedirs(CTESTS_DIR, exist_ok=True)
CTESTS_FILE = "ctests-{project}.json"

# constants for running ctests
RUNCTEST_TR_DIR = os.path.join(RUN_CTEST_DIR, "run_ctest_result") # test result directory
os.makedirs(RUNCTEST_TR_DIR, exist_ok=True)