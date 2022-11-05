# How to set up Cassandra for CTest
Prerequisites:
- Java 11
- Ant 1.10.7

Steps:
1. clone cassandra, `git clone https://github.com/apache/cassandra.git ../../../app/cassandra && cd ../../../app/cassandra`
2. checkout commit, `git checkout 4e1d31e`
3. apply injection patch, `git apply ../../resources/supported/cassandra/ctest-injection.patch`
4. build the project, `ant -Duse.jdk11=true`
5. verify setup, `ant testsome -Dtest.name=org.apache.cassandra.hints.HintsCatalogTest -Dtest.methods=deleteHintsTest -Duse.jdk11=true`

# Additional Parameters For CTest
For running CTest, please refer to [doc](../../../README.md#how-to-run-ctest)

## project.props
- `use.jdk11=true`
    - required

## project.args
- `-q`
    - recommended
    - suppress INFO level log