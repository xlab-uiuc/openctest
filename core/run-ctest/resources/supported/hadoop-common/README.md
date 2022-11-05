# How to set up hadoop-common for CTest
Prerequisites:
- Java 11
- Maven 3

Steps:
1. clone hadoop, `git clone https://github.com/apache/hadoop.git ../../../app/hadoop && cd ../../../app/hadoop`
2. checkout commit, `git checkout a585a73`
3. apply injection patch, `git apply ../../resources/supported/hadoop-common/ctest-injection.patch`
4. build the project, `mvn -pl hadoop-common-project/hadoop-common -am install -DskipTests`
5. verify setup, `mvn -pl hadoop-common-project/hadoop-common test -Dtest=org.apache.hadoop.crypto.TestCryptoStreams#testAvailable`

# Additional Parameters For CTest
For running CTest, please refer to [doc](../../../README.md#how-to-run-ctest)

## project.props
- `use.surefire=true`
    - highly recommended
    - set the Maven goal to be `surefire:test` to avoid recompiling the modules

## project.args
- `-q`
    - recommended
    - suppress INFO level log