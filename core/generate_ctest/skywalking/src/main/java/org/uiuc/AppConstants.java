package org.uiuc;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public interface AppConstants {

  Map<String, String> moduleToDirMap = new HashMap<String, String>() {
    {
      put("oap-server/server-starter", "./oap-server/server-starter/src/main/resources/");
      put("oap-server/server-configuration/configuration-apollo", "./oap-server/server-configuration/configuration-apollo/src/test/resources/");
      put("oap-server/server-configuration/configuration-etcd", "./oap-server/server-configuration/configuration-etcd/src/test/resources/");
      put("oap-server/server-configuration/configuration-zookeeper", "./oap-server/server-configuration/configuration-zookeeper/src/test/resources/");
      put("oap-server/analyzer/agent-analyzer", "./oap-server/analyzer/agent-analyzer/src/main/resources/");
      put("oap-server/server-configuration/configuration-nacos", "./oap-server/server-configuration/configuration-nacos/src/test/resources/");
      put("oap-server/server-configuration/configuration-consul", "./oap-server/server-configuration/configuration-consul/src/test/resources/");
    }
  };

  Map<String, String> moduleToFileNameMap = new HashMap<String, String>() {
    {
      put("oap-server/server-starter", "application2.yml");
      put("oap-server/server-configuration/configuration-apollo", "application2.yml");
      put("oap-server/server-configuration/configuration-etcd", "application2.yml");
      put("oap-server/server-configuration/configuration-zookeeper", "application2.yml");
      put("oap-server/analyzer/agent-analyzer", "trace-sampling-policy-settings2.yml");
      put("oap-server/server-configuration/configuration-nacos", "application2.yml");
      put("oap-server/server-configuration/configuration-consul", "application2.yml");
    }
  };

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
}
