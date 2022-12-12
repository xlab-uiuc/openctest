package org.uiuc;

import java.util.HashMap;
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
    }
  };

  String ERROR_MSG = "Error on exec() method";
}
