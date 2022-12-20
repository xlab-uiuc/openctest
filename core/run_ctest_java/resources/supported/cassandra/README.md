# How to set up Cassandra for CTest
Prerequisites:
- Java 11
- Ant 1.10.7

Steps:
1. run setup script, `./setup.sh`
2. (Optional) go to cassandra directory and verify setup, `ant testsome -Dtest.name=org.apache.cassandra.hints.HintsCatalogTest -Dtest.methods=deleteHintsTest -Duse.jdk11=true`

# Additional Parameters For CTest
For running CTest, please refer to [doc](../../../README.md#how-to-run-ctest)

## project.props
- `use.jdk11=true`
    - required

## project.args
- `-q`
    - recommended
    - suppress INFO level log
