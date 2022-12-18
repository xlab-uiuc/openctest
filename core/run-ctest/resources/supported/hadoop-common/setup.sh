APP_PATH=$(git rev-parse --show-toplevel)
[ ! -d "$APP_PATH/core/run-ctest/app/hadoop" ] && git clone git@github.com:CornDavid5/hadoop.git "$APP_PATH/core/run-ctest/app/hadoop"
cd "$APP_PATH/core/run-ctest/app/hadoop"
git fetch && git checkout hadoop-common-injection
mvn -pl hadoop-common-project/hadoop-common -am install -DskipTests