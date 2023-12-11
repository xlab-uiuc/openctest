import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(CUR_DIR, "app")

CTEST_HADOOP_DIR = os.path.join(APP_DIR, "ctest-hadoop")
CTEST_HBASE_DIR = os.path.join(APP_DIR, "ctest-hbase")
CTEST_ZOOKEEPER_DIR = os.path.join(APP_DIR, "ctest-zookeeper")
CTEST_ALLUXIO_DIR = os.path.join(APP_DIR, "ctest-alluxio")
CTEST_HIVE_DIR = os.path.join(APP_DIR, "ctest-hive")
CTEST_NIFI_DIR = os.path.join(APP_DIR, "ctest-nifi")
CTEST_FLINK_DIR = os.path.join(APP_DIR, "ctest-flink")
CTEST_CAMEL_DIR = os.path.join(APP_DIR, "ctest-camel")
CTEST_KYLIN_DIR = os.path.join(APP_DIR, "ctest-kylin")

MODULE_PATH = {
    "hadoop-common": CTEST_HADOOP_DIR,
    "hadoop-hdfs": CTEST_HADOOP_DIR,
    "hbase-server": CTEST_HBASE_DIR,
    "alluxio-core": CTEST_ALLUXIO_DIR,
    "hive-common": CTEST_HIVE_DIR,
    "nifi-common": CTEST_NIFI_DIR,
    "flink-core": CTEST_FLINK_DIR,
    "camel-core": CTEST_CAMEL_DIR,
    "hadoop-yarn-common": CTEST_HADOOP_DIR,
    "kylin-common": CTEST_KYLIN_DIR,
}

SRC_SUBDIR = {
    "hadoop-common": "hadoop-common-project/hadoop-common",
    "hadoop-hdfs": "hadoop-hdfs-project/hadoop-hdfs",
    "hbase-server": "hbase-server",
    "zookeeper-server": "zookeeper-server",
    "alluxio-core": "core",
    "hive-common":"common",
    "nifi-common": "",
    "flink-core": "flink-core",
    "camel-core": "core/camel-core",
    "hadoop-yarn-common": "hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common",
    "kylin-common": "",

}

MVN_TEST_PATH = {
    "hadoop-common": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-common"]),
    "hadoop-hdfs": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-hdfs"]),
    "hbase-server": os.path.join(CTEST_HBASE_DIR, SRC_SUBDIR["hbase-server"]),
    "zookeeper-server": os.path.join(CTEST_ZOOKEEPER_DIR, SRC_SUBDIR["zookeeper-server"]),
    "alluxio-core": os.path.join(CTEST_ALLUXIO_DIR, SRC_SUBDIR["alluxio-core"]),
    "hive-common": os.path.join(CTEST_HIVE_DIR, SRC_SUBDIR["hive-common"]),
    "nifi-common":os.path.join(CTEST_NIFI_DIR, SRC_SUBDIR["nifi-common"]),
    "flink-core": os.path.join(CTEST_FLINK_DIR, SRC_SUBDIR["flink-core"]),
    "camel-core": os.path.join(CTEST_CAMEL_DIR, SRC_SUBDIR["camel-core"]),
    "hadoop-yarn-common": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-yarn-common"]),
    "kylin-common":  os.path.join(CTEST_KYLIN_DIR, SRC_SUBDIR["kylin-common"]),
}

LOCAL_CONF_PATH = {
    "hadoop-common": "results/hadoop-common/conf_params.txt",
    "hadoop-hdfs": "results/hadoop-hdfs/conf_params.txt",
    "hbase-server": "results/hbase-server/conf_params.txt",
    "zookeeper-server": "results/zookeeper-server/conf_params.txt",
    "alluxio-core": "results/alluxio-core/conf_params.txt",
    "hive-common": "results/hive-common/conf_params.txt",
    "nifi-common": "results/nifi-commons/conf_params.txt",
    "flink-core": "results/flink-core/conf_params.txt",
    "camel-core": "results/camel-core/conf_params.txt",
    "hadoop-yarn-common": "results/hadoop-yarn-common/conf_params.txt",
    "kylin-common": "results/kylin-common/conf_params.txt",
}

SUREFIRE_SUBDIR = "target/surefire-reports/*"

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
    "hive-common": [
        os.path.join(CTEST_HIVE_DIR, SRC_SUBDIR["hive-common"], SUREFIRE_SUBDIR)
    ],
    "nifi-common": [
        os.path.join(CTEST_NIFI_DIR, "nifi-commons/nifi-properties", SUREFIRE_SUBDIR)
    ],
    "flink-core": [
        os.path.join(CTEST_FLINK_DIR, "flink-core", SUREFIRE_SUBDIR)
    ],
    "camel-core": [
        os.path.join(CTEST_CAMEL_DIR, "core/camel-core", SUREFIRE_SUBDIR)
    ],
    "hadoop-yarn-common": [
        os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-yarn-common"], SUREFIRE_SUBDIR)
    ],
    "kylin-common":  [
        os.path.join(CTEST_KYLIN_DIR, SUREFIRE_SUBDIR)
    ],
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
    "hive-common": [
        os.path.join("surefire-reports/hive/hive-common", LOCAL_SUREFIRE_SUFFIX)
    ],
    "nifi-common":[
        os.path.join("surefire-reports/nifi/nifi-commons", LOCAL_SUREFIRE_SUFFIX)
    ],
    "flink-core": [
        os.path.join("surefire-reports/flink-core", LOCAL_SUREFIRE_SUFFIX)
    ],
    "camel-core": [
        os.path.join("surefire-reports/camel-core", LOCAL_SUREFIRE_SUFFIX)
    ],    
    "hadoop-yarn-common": [
        os.path.join("surefire-reports/yarn/hadoop-yarn", LOCAL_SUREFIRE_SUFFIX)
    ],
    "kylin-common": [
        os.path.join("surefire-reports/kylin-common", LOCAL_SUREFIRE_SUFFIX)
    ],
}
