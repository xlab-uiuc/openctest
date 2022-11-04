## Prerequisite
- Java 11
- Maven 3

```
mvn exec:java -q \
-Dproject.name=hadoop-common \
-Dproject.path=app/hadoop/hadoop-common-project/hadoop-common \
-Dmapping.path=resources/supported/hadoop-common/param_unset_getter_map.json \
-Dconf.pairs=hadoop.security.crypto.jce.provider=SunJCE,hadoop.security.crypto.cipher.suite=AES/CTR/NoPadding \
-Dtest.methods=org.apache.hadoop.crypto.TestCryptoStreams#testAvailable,org.apache.hadoop.crypto.TestCryptoStreamsNormal#testSkip,org.apache.hadoop.ha.TestZKFailoverController#testCedeActive \
-Dproject.props=maven.antrun.skip=true,use.surefire=true \
-Dproject.args=-q
```

```
mvn exec:java -q \
-Dproject.name=hadoop-hdfs \
-Dproject.path=app/hadoop/hadoop-hdfs-project/hadoop-hdfs \
-Dmapping.path=resources/supported/hadoop-hdfs/param_unset_getter_map.json \
-Dconf.file=examples/modified-config.properties \
-Dtest.file=examples/to-be-tested-tests.txt \
-Dproject.props=use.surefire=true \
-Dproject.args=-q
```