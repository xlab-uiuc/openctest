package uiuc.xlab.openctest.runctest.utils;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class CTestUtil {
    /**
     * Filter out those tests that are not affected by the modified configuration
     * values.
     *
     * @return a set of affected tests.
     */
    public static Set<String> filterUnaffectedTest(JSONObject paramTestMapping,
            Map<String, String> modifiedConfig, Set<String> toBeTestedTest) {
        Map<String, Set<String>> paramTestMap = new HashMap<>();
        modifiedConfig.keySet().forEach(param -> {
            JSONArray tests = (JSONArray) paramTestMapping.get(param);

            if (tests == null) {
                return;
            }

            for (Object test : tests) {
                paramTestMap.computeIfAbsent(param, k -> new HashSet<String>()).add(test.toString());
            }
        });

        Set<String> affectedTest = new HashSet<>();
        paramTestMap.values().forEach(tests -> {
            Set<String> associatedTest = new HashSet<>(toBeTestedTest);
            associatedTest.retainAll(tests);
            affectedTest.addAll(associatedTest);
        });

        // Set<String> unaffectedTest = new HashSet<>(toBeTestedTest);
        // unaffectedTest.removeAll(affectedTest);

        return affectedTest;
    }
}
