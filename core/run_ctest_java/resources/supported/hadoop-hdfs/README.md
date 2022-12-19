# How to set up hadoop-hdfs for CTest
Prerequisites:
- Java 11
- Maven 3

Steps:
1. run setup script, `./setup.sh`
2. (Optional) go to hadoop directory and verify setup, `mvn -pl hadoop-hdfs-project/hadoop-hdfs test -Dtest=org.apache.hadoop.hdfs.TestEncryptionZonesWithKMS#testIsEncryptedMethod`

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
