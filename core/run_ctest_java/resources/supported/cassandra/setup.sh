APP_PATH=$(git rev-parse --show-toplevel)
[ ! -d "$APP_PATH/core/run_ctest_java/app/cassandra" ] && git clone https://github.com/CornDavid5/cassandra.git "$APP_PATH/core/run_ctest_java/app/cassandra"
cd "$APP_PATH/core/run_ctest_java/app/cassandra"
git fetch && git checkout ctest-injection
CASSANDRA_USE_JDK11=true ant