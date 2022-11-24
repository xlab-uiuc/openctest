import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(CUR_DIR, "app")
RUN_CTEST_DIR = CUR_DIR

CTEST_HADOOP_DIR = os.path.join(APP_DIR, "ctest-hadoop")
CTEST_HBASE_DIR = os.path.join(APP_DIR, "ctest-hbase")
CTEST_ZOOKEEPER_DIR = os.path.join(APP_DIR, "ctest-zookeeper")
CTEST_ALLUXIO_DIR = os.path.join(APP_DIR, "ctest-alluxio")
CTEST_CASSANDRA_DIR = os.path.join(APP_DIR, "cassandra")

HCOMMON = "hadoop-common"
HDFS = "hadoop-hdfs"
HBASE = "hbase-server"
ZOOKEEPER = "zookeeper-server"
ALLUXIO = "alluxio-core"
CASSANDRA = "cassandra"

PROJECT_DIR = {
    HCOMMON: CTEST_HADOOP_DIR,
    HDFS: CTEST_HADOOP_DIR,
    HBASE: CTEST_HBASE_DIR,
    ZOOKEEPER: CTEST_ZOOKEEPER_DIR,
    ALLUXIO: CTEST_ALLUXIO_DIR,
    "cassandra": CTEST_CASSANDRA_DIR
}

# the module of the project we experimented on
MODULE_SUBDIR = {
    HCOMMON: "hadoop-common-project/hadoop-common",
    HDFS: "hadoop-hdfs-project/hadoop-hdfs",
    HBASE: "hbase-server",
    ZOOKEEPER: "zookeeper-server",
    ALLUXIO: "core",
    "cassandra": ""
}


SRC_SUBDIR = {
    "hadoop-common": "hadoop-common-project/hadoop-common",
    "hadoop-hdfs": "hadoop-hdfs-project/hadoop-hdfs",
    "hbase-server": "hbase-server",
    "zookeeper-server": "zookeeper-server",
    "alluxio-core": "core",
    "cassandra": ""
}

MVN_TEST_PATH = {
    "hadoop-common": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-common"]),
    "hadoop-hdfs": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-hdfs"]),
    "hbase-server": os.path.join(CTEST_HBASE_DIR, SRC_SUBDIR["hbase-server"]),
    "zookeeper-server": os.path.join(CTEST_ZOOKEEPER_DIR, SRC_SUBDIR["zookeeper-server"]),
    "alluxio-core": os.path.join(CTEST_ALLUXIO_DIR, SRC_SUBDIR["alluxio-core"]),
    "cassandra": os.path.join(CTEST_CASSANDRA_DIR, SRC_SUBDIR["cassandra"])
}

LOCAL_CONF_PATH = {
    "hadoop-common": "results/hadoop-common/conf_params.txt",
    "hadoop-hdfs": "results/hadoop-hdfs/conf_params.txt",
    "hbase-server": "results/hbase-server/conf_params.txt",
    "zookeeper-server": "results/zookeeper-server/conf_params.txt",
    "alluxio-core": "results/alluxio-core/conf_params.txt",
    "cassandra": "results/cassandra/conf_params.txt"
}

SUREFIRE_SUBDIR = "target/surefire-reports/*"
SUREFIRE_XML = "TEST-{}.xml" # slot is the classname

SUREFIRE_DIR = {
    HCOMMON: [os.path.join(CTEST_HADOOP_DIR, MODULE_SUBDIR[HCOMMON], SUREFIRE_SUBDIR)],
    HDFS: [os.path.join(CTEST_HADOOP_DIR, MODULE_SUBDIR[HDFS], SUREFIRE_SUBDIR)],
    HBASE: [os.path.join(CTEST_HBASE_DIR, MODULE_SUBDIR[HBASE], SUREFIRE_SUBDIR)],
    ZOOKEEPER: [os.path.join(CTEST_ZOOKEEPER_DIR, MODULE_SUBDIR[ZOOKEEPER], SUREFIRE_SUBDIR)],
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
    "cassandra": [
        os.path.join(CTEST_CASSANDRA_DIR, 'build/test/output')
    ]
}

CTEST_SUREFIRE_PATH = {
    "hadoop-common": [
        os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-common"], SUREFIRE_SUBDIR)
    ],
    "hadoop-hdfs": [
        os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-hdfs"], SUREFIRE_SUBDIR)
    ],
    "hbase-server": [
        os.path.join(CTEST_HBASE_DIR, "hbase-server", SUREFIRE_SUBDIR)
    ],
    "zookeeper-server": [
        os.path.join(CTEST_ZOOKEEPER_DIR, "zookeeper-server", SUREFIRE_SUBDIR)
    ],
    "alluxio-core": [
        os.path.join(CTEST_ALLUXIO_DIR, "core/base", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/client/fs", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/client/hdfs", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/common", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/server/common", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/server/proxy", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/server/worker", SUREFIRE_SUBDIR),
        os.path.join(CTEST_ALLUXIO_DIR, "core/server/master", SUREFIRE_SUBDIR)
    ],
    "cassandra": [
        os.path.join(CTEST_CASSANDRA_DIR, "build/test/output/*")
    ]
}

LOCAL_SUREFIRE_SUFFIX = "surefire-reports/*"

LOCAL_SUREFIRE_PATH = {
    "hadoop-common": [
        os.path.join("surefire-reports/common/hadoop-common", LOCAL_SUREFIRE_SUFFIX)
    ],
    "hadoop-hdfs": [
        os.path.join("surefire-reports/hdfs/hadoop-hdfs", LOCAL_SUREFIRE_SUFFIX)
    ],
    "hbase-server": [
        os.path.join("surefire-reports/hbase/hbase-server", LOCAL_SUREFIRE_SUFFIX)
    ],
    "zookeeper-server": [
        os.path.join("surefire-reports/zk/zookeeper-server", LOCAL_SUREFIRE_SUFFIX)
    ],
    "alluxio-core": [
        os.path.join("surefire-reports/alluxio-core", LOCAL_SUREFIRE_SUFFIX)
    ],
    "cassandra": [
        os.path.join("surefire-reports/cassandra", LOCAL_SUREFIRE_SUFFIX)
    ]
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
        os.path.join(CTEST_ZOOKEEPER_DIR, "zookeeper-server/ctest.cfg")
    ],
    ALLUXIO: [
        os.path.join(CTEST_ALLUXIO_DIR, "core/alluxio-ctest.properties")
    ],
    "cassandra": [
        os.path.join(CTEST_CASSANDRA_DIR, "test/conf/ctest-injection.yaml")
    ]
}