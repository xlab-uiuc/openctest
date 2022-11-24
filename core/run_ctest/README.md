# Run Ctest
The module is used to run the ctest against Cassandra 4.0.

## Prerequisites
- Java 11
- Ant 1.10.7

## How to set up cassandra
- clone cassandra, `git clone https://github.com/CornDavid5/cassandra.git app/ctest-cassandra && cd app/ctest-cassandra`
- checkout branch, `git fetch && git checkout ctest-injection`
- build the project, `CASSANDRA_USE_JDK11=true ant`

## How to run ctest
Run single test with modified configuration value:

`python run_single_ctest.py TESTNAME MODIFIEDCONF`

Example command:

`python run_single_ctest.py org.apache.cassandra.hints.HintsCatalogTest#deleteHintsTest storage_port=8080`