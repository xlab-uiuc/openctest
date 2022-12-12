package org.uiuc;

import java.util.Arrays;
import java.util.List;

public interface AppConstants {

  List<String> testCases = Arrays.asList(
          "oap-server/server-starter>org.apache.skywalking.oap.server.starter.config.ApplicationConfigLoaderTestCase#testLoadConfig",
          "oap-server/server-starter>org.apache.skywalking.oap.server.starter.config.ApplicationConfigLoaderTestCase#testLoadStringTypeConfig",
          "oap-server/server-starter>org.apache.skywalking.oap.server.starter.config.ApplicationConfigLoaderTestCase#testLoadIntegerTypeConfig",
          "oap-server/server-starter>org.apache.skywalking.oap.server.starter.config.ApplicationConfigLoaderTestCase#testLoadBooleanTypeConfig",
          "oap-server/server-starter>org.apache.skywalking.oap.server.starter.config.ApplicationConfigLoaderTestCase#testLoadSpecialStringTypeConfig",
          "oap-server/server-library/library-module>org.apache.skywalking.oap.server.library.module.ApplicationConfigurationTest#testBuildConfig",
          "oap-server/server-configuration/configuration-apollo>org.apache.skywalking.oap.server.configuration.apollo.ITApolloConfigurationTest#shouldReadUpdated",
          "oap-server/server-configuration/configuration-apollo>org.apache.skywalking.oap.server.configuration.apollo.ITApolloConfigurationTest#shouldReadUpdated4Group",
          "oap-server/server-configuration/configuration-consul>org.apache.skywalking.oap.server.configuration.consul.ITConsulConfigurationTest#shouldReadUpdated",
          "oap-server/server-configuration/configuration-consul>org.apache.skywalking.oap.server.configuration.consul.ITConsulConfigurationTest#shouldReadUpdated4Group",
          "oap-server/server-configuration/configuration-etcd>org.apache.skywalking.oap.server.configuration.etcd.ITEtcdConfigurationTest#shouldReadUpdated",
          "oap-server/server-configuration/configuration-etcd>org.apache.skywalking.oap.server.configuration.etcd.ITEtcdConfigurationTest#shouldReadUpdated4Group",
          "oap-server/server-configuration/configuration-zookeeper>org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated",
          "oap-server/server-configuration/configuration-zookeeper>org.apache.skywalking.oap.server.configuration.zookeeper.it.ITZookeeperConfigurationTest#shouldReadUpdated4GroupConfig",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testStaticConfigInit",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testTraceLatencyThresholdDynamicUpdate",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testTraceLatencyThresholdNotify",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testDefaultSampleRateDynamicUpdate",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testDefaultSampleRateNotify",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testServiceSampleRateDynamicUpdate",
          "oap-server/analyzer/agent-analyzer>org.apache.skywalking.oap.server.analyzer.provider.trace.TraceSamplingPolicyWatcherTest#testServiceSampleRateNotify",
          "oap-server/server-configuration/configuration-nacos>org.apache.skywalking.oap.server.configuration.nacos.ITNacosConfigurationTest#shouldReadUpdated",
          "oap-server/server-configuration/configuration-nacos>org.apache.skywalking.oap.server.configuration.nacos.ITNacosConfigurationTest#shouldReadUpdatedGroup",
          "oap-server/server-configuration/configuration-nacos>org.apache.skywalking.oap.server.configuration.nacos.NacosConfigWatcherRegisterTest#shouldReadConfigs"
  );


  String ERROR_MSG = "Error on exec() method";

  String CTEST_MODULE = "[CTEST][getModuleConfiguration]";
  String CTEST_PROVIDER = "[CTEST][getProviderConfiguration]";

  String CTEST_PROPERTY_WRAPPER = "[CTEST][PropertiesWrapper]";

  String CTEST_PROPERTY_RESET_WRAPPER = "[CTEST][PropertiesWrapper -reset]";

  String CTEST_SUB_PROPERTY_WRAPPER = "[CTEST][SubPropertiesWrapper]";

  String CTEST_SUB_PROPERTY_RESET_WRAPPER = "[CTEST][SubPropertiesWrapper -reset]";

  String CTEST_SETTINGS_MAP = "[CTest SETTINGS MAP]";
  String SEPARATOR = "###";
  String SEPARATOR_ASTERISK = "***";
}
