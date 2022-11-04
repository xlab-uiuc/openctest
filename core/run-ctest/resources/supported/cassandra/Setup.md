# How to set up Cassandra for CTest
Prerequisites:
- Java 11
- Ant 1.10.7

Steps:
1. clone cassandra, `git clone https://github.com/apache/cassandra.git ../../../app/cassandra && cd ../../../app/cassandra`
2. checkout commit, `git checkout 4e1d31e`
3. apply injection patch, `git apply ../../resources/supported/cassandra/ctest-injection.patch`
4. build the project, `CASSANDRA_USE_JDK11=true ant`
5. verify setup, `CASSANDRA_USE_JDK11=true ant testsome -Dtest.name=org.apache.cassandra.hints.HintsCatalogTest -Dtest.methods=deleteHintsTest`