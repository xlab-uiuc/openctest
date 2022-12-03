# Run Ctest
The module is used to run the ctest against Cassandra 4.0.

## Description
See [Running Ctest](../README.md#2-running-ctests)

## Prerequisites
- Java 11
- Ant 1.10.7

## How to run ctest
Run single test with modified configuration value:

`python run_single_ctest.py TESTNAME MODIFIEDCONF`

Example command:

`python run_single_ctest.py org.apache.cassandra.hints.HintsCatalogTest#deleteHintsTest storage_port=8080`