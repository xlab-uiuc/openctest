package uiuc.xlab.openctest.runctest.utils;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public final class CTestUtil {
    private CTestUtil() {
        throw new IllegalStateException("Utility class cannot be instantiated");
    }

    /**
     * Filter out those tests that are not affected by the
     * modified configuration values.
     *
     * @param paramTestMapping a map of parameters and test methods.
     * @param modifiedConfig   a map of config and its modified value.
     * @param toBeTestedTest   a set of tests to be tested.
     * @return a set of affected tests.
     */
    public static Set<String> filterUnaffectedTest(
            final JSONObject paramTestMapping,
            final Map<String, Object> modifiedConfig,
            final Set<String> toBeTestedTest) {
        Map<String, Set<String>> paramTestMap = new HashMap<>();
        modifiedConfig.keySet().forEach(param -> {
            JSONArray tests = (JSONArray) paramTestMapping.get(param);

            if (tests == null) {
                return;
            }

            for (Object test : tests) {
                paramTestMap.computeIfAbsent(
                        param, k -> new HashSet<String>()).add(test.toString());
            }
        });

        Set<String> affectedTest = new HashSet<>();
        paramTestMap.values().forEach(tests -> {
            Set<String> associatedTest = new HashSet<>(toBeTestedTest);
            associatedTest.retainAll(tests);
            affectedTest.addAll(associatedTest);
        });

        return affectedTest;
    }
}
