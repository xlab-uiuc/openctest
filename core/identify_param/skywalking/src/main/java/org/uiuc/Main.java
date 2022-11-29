package org.uiuc;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ValueNode;

import java.util.Iterator;


import static org.uiuc.AppConstants.*;
import static org.uiuc.UtilHelper.copy;

public class Main {

  static Map<String, Object> map = new LinkedHashMap<>();

  public static void main(String[] args) throws IOException, InterruptedException {

    String destDir = args[0];

    int initialIndex = 0;
    processMvnTest(initialIndex);

    Gson gson = new Gson();
    String json = gson.toJson(map);
    System.out.println(json);

    FileWriter writer3 = new FileWriter(destDir + "/test-to-config.txt");
    writer3.write(json);
    writer3.close();

    Map<String, String> map = new HashMap<>();
    try {
      addKeys("", new ObjectMapper().readTree(json), map);
    } catch (IOException e) {
      e.printStackTrace();
    }

    Map<String, List<String>> testToConfigList = new LinkedHashMap<>();
    map.forEach((k,v) -> {
      String[] strArr = k.split("#");
      String str = strArr[1];
      String testCase =  strArr[0] + "#" + str.substring(0, str.indexOf("."));
      String confStr = strArr[1];
      String config = confStr.substring(confStr.indexOf(".") + 1);
      if(!testToConfigList.containsKey(testCase)) {
        List<String> confList = new ArrayList<>();
        confList.add(config);
        testToConfigList.put(testCase, confList);
      } else {
        testToConfigList.get(testCase).add(config);
      }
    });

    String jsonTestToConfigList = gson.toJson(testToConfigList);
    System.out.println(jsonTestToConfigList);
    FileWriter writer1 = new FileWriter(destDir + "/test-to-config-flat.txt");
    writer1.write(jsonTestToConfigList);
    writer1.close();

    Set<String> set = new HashSet<>();
    map.forEach((k,v) -> {
      String str = k.split("#")[1];
      set.add(str.substring(str.indexOf(".") + 1) + "\t" + v + "\t" + "description");
    });

    FileWriter writer2 = new FileWriter(destDir + "/all-config.txt");
    for(String str: set) {
      writer2.write(str + System.lineSeparator());
    }
    writer2.close();
  }

  private static void processMvnTest(int index) throws IOException, InterruptedException {

    if (index == testCases.size()) {
      return;
    }

    Process p = null;
    System.out.println(map);
    String test = testCases.get(index);
    String[] split = test.split(">");
    String module = split[0];
    String testCase = split[1];
    System.out.println("Module: " + module + " Test Case: " + testCase);
    try {
      p = Runtime.getRuntime().exec("mvn test -pl " + module + " -Dtest=" + testCase + " -DfailIfNoTests=false");
    } catch (IOException e) {
      System.err.println(ERROR_MSG);
      e.printStackTrace();
    }
    OutputStream output = new OutputStream() {
      private final StringBuilder string = new StringBuilder();

      @Override
      public void write(int b) {
        this.string.append((char) b);
      }

      public String toString() {
        return this.string.toString();
      }
    };

    copy(p.getInputStream(), output);
    System.out.println(output);
    BufferedReader bufReader = new BufferedReader(new StringReader(output.toString()));
    String prev = bufReader.readLine();
    String next = bufReader.readLine();
    StringBuilder storeModule = new StringBuilder();
    StringBuilder storeProvider = new StringBuilder();
    StringBuilder storeProperty = new StringBuilder();
    Map<String, Object> configMap = new LinkedHashMap<>();

    while (next != null) {
      if (prev.contains(CTEST_MODULE) && next.contains(CTEST_PROVIDER)) {
        storeModule = new StringBuilder(prev);
        storeProvider = new StringBuilder(next);
      }
      if (next.contains(CTEST_PROPERTY_WRAPPER)) {
        storeProperty = new StringBuilder(next);
        processMapping(testCase, configMap, storeModule.toString(), storeProvider.toString(), next, null, null,
                null);
      }
      if (next.contains(CTEST_SUB_PROPERTY_WRAPPER)) {
        processMapping(testCase, configMap, storeModule.toString(), storeProvider.toString(),
                storeProperty.toString(), next, null, null);
      }
      if (next.contains(CTEST_PROPERTY_RESET_WRAPPER)) {
        processMapping(testCase, configMap, storeModule.toString(), storeProvider.toString(), null, null, next,
                null);
      }
      if (next.contains(CTEST_SUB_PROPERTY_RESET_WRAPPER)) {
        processMapping(testCase, configMap, storeModule.toString(), storeProvider.toString(),
                storeProperty.toString(), next, null, next);
      }
      if (next.contains(CTEST_SETTINGS_MAP)) {
        processSettingsMap(testCase, next);
      }
      prev = next;
      next = bufReader.readLine();
    }
    if (!map.containsKey(testCase)) {
      map.put(testCase, new HashMap<>());
    }
    index = index + 1;
    processMvnTest(index);
    p.waitFor();
  }

  private static void processMapping(String test, Map<String, Object> configMap, String module, String provider,
                                     String propKey, String subPropKey, String resetProp, String resetSubProp) {

    String moduleExtracted = (module == null || module.isEmpty()) ? null
            : module.substring(module.indexOf(SEPARATOR) + 3, module.lastIndexOf(SEPARATOR));

    String providerExtracted = (provider == null || provider.isEmpty()) ? null
            : provider.substring(provider.indexOf(SEPARATOR) + 3, provider.lastIndexOf(SEPARATOR));

    String propKeyExtracted = (propKey == null || propKey.isEmpty()) ? null
            : propKey.substring(propKey.indexOf(SEPARATOR) + 3, propKey.lastIndexOf(SEPARATOR));

    String subPropKeyExtracted = (subPropKey == null || subPropKey.isEmpty()) ? null
            : subPropKey.substring(subPropKey.indexOf(SEPARATOR) + 3, subPropKey.lastIndexOf(SEPARATOR));

    String resetPropKey = (resetProp == null || resetProp.isEmpty()) ? null
            : resetProp.substring(resetProp.indexOf(SEPARATOR) + 3, resetProp.lastIndexOf(SEPARATOR));

    String resetPropValue = (resetProp == null || resetProp.isEmpty()) ? null
            : resetProp.substring(resetProp.indexOf(SEPARATOR_ASTERISK) + 3,
            resetProp.lastIndexOf(SEPARATOR_ASTERISK));

    if (moduleExtracted == null && providerExtracted == null) {
      return;
    }

    if (resetProp != null && map.containsKey(test) && module != null && ((Map) map.get(test)).containsKey(module)
            && provider != null && ((Map) ((Map) map.get(test)).get(module)).containsKey(provider) && ((Map) ((Map) ((Map) map.get(test)).get(module))
            .get(provider)).containsKey(resetPropKey)) {
      ((Map) ((Map) ((Map) map.get(test)).get(module)).get(provider)).put(resetPropKey, resetPropValue);
      return;
    }

    String resetSubPropKey = (resetSubProp == null || resetSubProp.isEmpty()) ? null
            : resetSubProp.substring(resetProp.indexOf(SEPARATOR) + 3, resetSubProp.lastIndexOf(SEPARATOR));
    String resetSubPropValue = (resetSubProp == null || resetSubProp.isEmpty()) ? null
            : resetSubProp.substring(resetProp.indexOf(SEPARATOR_ASTERISK) + 3,
            resetSubProp.lastIndexOf(SEPARATOR_ASTERISK));

    if (resetSubPropKey != null && map.containsKey(test) && module != null && ((Map) map.get(test)).containsKey(module)
            && provider != null && ((Map) ((Map) map.get(test)).get(module)).containsKey(provider) && ((Map) ((Map) ((Map) map.get(test)).get(module))
            .get(provider)).containsKey(resetSubPropKey)) {
      ((Map) ((Map) ((Map) ((Map) map.get(test)).get(module)).get(provider)).get("properties")).put(resetSubPropKey, resetSubPropValue);
      return;
    }

    String configStr = provider.substring(provider.indexOf("{") + 1, provider.lastIndexOf("}"));

    if (configStr.contains("properties={") && propKeyExtracted.equals("properties")
            && subPropKeyExtracted != null) {
      String propertiesStr = configStr.substring(configStr.indexOf("{") + 1, configStr.indexOf("}"));
      configStr = configStr.replace(propertiesStr, "").replace("properties={}", "");
      String[] innerProp = propertiesStr.split(", ");
      Map<String, String> propMap = new LinkedHashMap<>();
      for (String s : innerProp) {
        String[] eachProp = s.split("=");
        if (subPropKeyExtracted.equals(eachProp[0])) {
          propMap.put(eachProp[0], eachProp[1]);
        }
      }
      if (propMap.size() > 0) {
        configMap.put("properties", propMap);
      }
    }

    if (configStr.contains("downsampling=") && propKeyExtracted.equals("downsampling")) {
      String arrayStr = configStr.substring(configStr.indexOf("["), configStr.indexOf("]") + 1);
      configStr = configStr.replace(arrayStr, "").replace("downsampling=,", "");
      configMap.put("downsampling", arrayStr);
    }

    String[] parts = configStr.split(", ");

    for (String part : parts) {
      String[] eachConfig = part.split("=");
      if (eachConfig.length == 1 && propKeyExtracted.equals(eachConfig[0])) {
        configMap.put(eachConfig[0], "");
      } else {
        if (propKeyExtracted.equals(eachConfig[0])) {
          configMap.put(eachConfig[0], eachConfig[1]);
        }
      }
    }

    Map<String, Map<String, Object>> providerMap = new LinkedHashMap<>();
    providerMap.put(providerExtracted, configMap);
    Map<String, Map<String, Map<String, Object>>> moduleMap = new LinkedHashMap<>();
    moduleMap.put(moduleExtracted, providerMap);
    map.put(test, moduleMap);
  }

  private static void processSettingsMap(String test, String config) {
    Map<String, Object> configs = new HashMap<>();
    String extractedInitial = config.substring(config.indexOf("("), config.lastIndexOf(")"));
    String defaultPolicy = extractedInitial.substring(extractedInitial.indexOf("defaultPolicy=SamplingPolicy(") + 29, extractedInitial.indexOf("),"));
    String[] defaultPolicyArr = defaultPolicy.split(", ");
    Map<String, String> defaultPolicyMap = new HashMap<>();
    for (String s : defaultPolicyArr) {
      String[] split = s.split("=");
      defaultPolicyMap.put(split[0], split[1]);
    }
    configs.put("default", defaultPolicyMap);
    String services = extractedInitial.substring(extractedInitial.indexOf("services={") + 10, extractedInitial.indexOf("}"));

    List<String> matchList = new ArrayList<>();
    Pattern regex = Pattern.compile("\\(([^()]*)\\)");
    Matcher regexMatcher = regex.matcher(services);
    while (regexMatcher.find()) {
      matchList.add(regexMatcher.group(1));
    }

    List<String> orderedServiceList = new ArrayList<>();
    String[] serviceNames = services.replaceAll("\\s*\\([^\\)]*\\)\\s*", " ").split(" , ");
    for (String str : serviceNames) {
      orderedServiceList.add(str.split("=")[0]);
    }

    List<Object> serviceList = new ArrayList<>();
    for (int i = 0; i < matchList.size(); i++) {
      Map<String, String> servicesMap = new HashMap<>();
      servicesMap.put("name", "");
      String[] split = matchList.get(i).split(", ");
      servicesMap.put("name", orderedServiceList.get(i));
      for (String s : split) {
        String[] internalSplit = s.split("=");
        servicesMap.put(internalSplit[0], internalSplit[1]);
      }
      serviceList.add(servicesMap);
    }

    configs.put("services", serviceList);
    map.put(test, configs);
  }

  private static void addKeys(String currentPath, JsonNode jsonNode, Map<String, String> map) {
    if (jsonNode.isObject()) {
      ObjectNode objectNode = (ObjectNode) jsonNode;
      Iterator<Map.Entry<String, JsonNode>> iter = objectNode.fields();
      String pathPrefix = currentPath.isEmpty() ? "" : currentPath + ".";

      while (iter.hasNext()) {
        Map.Entry<String, JsonNode> entry = iter.next();
        addKeys(pathPrefix + entry.getKey(), entry.getValue(), map);
      }
    } else if (jsonNode.isArray()) {
      ArrayNode arrayNode = (ArrayNode) jsonNode;
      for (int i = 0; i < arrayNode.size(); i++) {
        addKeys(currentPath + "[" + i + "]", arrayNode.get(i), map);
      }
    } else if (jsonNode.isValueNode()) {
      ValueNode valueNode = (ValueNode) jsonNode;
      map.put(currentPath, valueNode.asText());
    }
  }

}