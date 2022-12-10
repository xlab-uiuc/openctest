import os

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.join(CUR_DIR, "app")

CTEST_HADOOP_DIR = os.path.join(APP_DIR, "ctest-hadoop")
CTEST_HBASE_DIR = os.path.join(APP_DIR, "ctest-hbase")
CTEST_ZOOKEEPER_DIR = os.path.join(APP_DIR, "ctest-zookeeper")
CTEST_ALLUXIO_DIR = os.path.join(APP_DIR, "ctest-alluxio")
CTEST_KYLIN_DIR = os.path.join(APP_DIR, "ctest-kylin")

MODULE_PATH = {
    "hadoop-common": CTEST_HADOOP_DIR,
    "hadoop-hdfs": CTEST_HADOOP_DIR,
    "hbase-server": CTEST_HBASE_DIR,
    "alluxio-core": CTEST_ALLUXIO_DIR,
    "kylin-common": CTEST_KYLIN_DIR,
    "kylin-tool": CTEST_KYLIN_DIR,
    "kylin-storage": CTEST_KYLIN_DIR,
    "kylin-cube": CTEST_KYLIN_DIR,
}

SRC_SUBDIR = {
    "hadoop-common": "hadoop-common-project/hadoop-common",
    "hadoop-hdfs": "hadoop-hdfs-project/hadoop-hdfs",
    "hbase-server": "hbase-server",
    "zookeeper-server": "zookeeper-server",
    "alluxio-core": "core",
    "kylin-common": "",
    "kylin-tool": "",
    "kylin-storage": "",
    "kylin-cube": "",

}

MVN_TEST_PATH = {
    "hadoop-common": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-common"]),
    "hadoop-hdfs": os.path.join(CTEST_HADOOP_DIR, SRC_SUBDIR["hadoop-hdfs"]),
    "hbase-server": os.path.join(CTEST_HBASE_DIR, SRC_SUBDIR["hbase-server"]),
    "zookeeper-server": os.path.join(CTEST_ZOOKEEPER_DIR, SRC_SUBDIR["zookeeper-server"]),
    "alluxio-core": os.path.join(CTEST_ALLUXIO_DIR, SRC_SUBDIR["alluxio-core"]),
    "kylin-common":  os.path.join(CTEST_KYLIN_DIR, SRC_SUBDIR["kylin-common"]),
    "kylin-tool":  os.path.join(CTEST_KYLIN_DIR, SRC_SUBDIR["kylin-tool"]),
    "kylin-storage":  os.path.join(CTEST_KYLIN_DIR, SRC_SUBDIR["kylin-storage"]),
    "kylin-cube":  os.path.join(CTEST_KYLIN_DIR, SRC_SUBDIR["kylin-cube"]),
}

LOCAL_CONF_PATH = {
    "hadoop-common": "results/hadoop-common/conf_params.txt",
    "hadoop-hdfs": "results/hadoop-hdfs/conf_params.txt",
    "hbase-server": "results/hbase-server/conf_params.txt",
    "zookeeper-server": "results/zookeeper-server/conf_params.txt",
    "alluxio-core": "results/alluxio-core/conf_params.txt",
    "kylin-common": "results/kylin-common/conf_params.txt",
    "kylin-tool": "results/kylin-tool/conf_params.txt",
    "kylin-storage": "results/kylin-storage/conf_params.txt",
    "kylin-cube": "results/kylin-cube/conf_params.txt"
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
    "kylin-common":  [
        os.path.join(CTEST_KYLIN_DIR, SUREFIRE_SUBDIR)
    ],
    "kylin-tool":  [
        os.path.join(CTEST_KYLIN_DIR, SUREFIRE_SUBDIR)
    ],
    "kylin-storage":  [
        os.path.join(CTEST_KYLIN_DIR, SUREFIRE_SUBDIR)
    ],
    "kylin-cube":  [
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
    "kylin-common": [
        os.path.join("surefire-reports/kylin-common", LOCAL_SUREFIRE_SUFFIX)
    ],
    "kylin-tool": [
        os.path.join("surefire-reports/kylin-tool", LOCAL_SUREFIRE_SUFFIX)
    ],
    "kylin-storage": [
        os.path.join("surefire-reports/kylin-storage", LOCAL_SUREFIRE_SUFFIX)
    ],
    "kylin-cube": [
        os.path.join("surefire-reports/kylin-cube", LOCAL_SUREFIRE_SUFFIX)
    ]
}
