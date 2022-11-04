# How to set up hadoop-hdfs for CTest
Prerequisites:
- Java 11
- Maven 3

Steps:
1. clone hadoop, `git clone https://github.com/apache/hadoop.git ../../../app/hadoop && cd ../../../app/hadoop`
2. checkout commit, `git checkout a585a73`
3. apply injection patch, `git apply ../../resources/supported/hadoop-hdfs/ctest-injection.patch`
4. build the project, `mvn -pl hadoop-hdfs-project/hadoop-hdfs -am install -DskipTests`
5. verify setup, `mvn -pl hadoop-hdfs-project/hadoop-hdfs test -Dtest=org.apache.hadoop.net.TestNetworkTopology#testGetWeight`