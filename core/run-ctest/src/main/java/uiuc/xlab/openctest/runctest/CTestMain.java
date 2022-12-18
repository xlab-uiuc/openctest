package uiuc.xlab.openctest.runctest;

import org.javatuples.Pair;
import org.json.simple.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;
import uiuc.xlab.openctest.runctest.utils.CTestUtil;
import uiuc.xlab.openctest.runctest.utils.InputParser;

import java.util.Map;
import java.util.Set;

public final class CTestMain {
    private static final Logger LOGGER =
            LoggerFactory.getLogger(CTestMain.class);

    private CTestMain() {
        throw new IllegalStateException("main class cannot be instantiated");
    }

    /**
     * The entry point of the program, it will do the following:
     * 1. extract configuration diff D of the specified configuration file.
     * 2. select the mapped ctests for configuration parameters in D.
     * 3. run selected ctests against configuration values in D.
     * 4. collect the test result for the specified configuration file.
     *
     * @param args arguments from command line
     */
    public static void main(final String[] args) {
        // get objects based on command line input
        Set<String> toBeTestedTest = InputParser.getToBeTestedTest();
        JSONObject paramTestMapping = InputParser.getParamTestMappingJSON();
        Map<String, Object> modifiedConfig = InputParser.getModifiedConfig();
        LOGGER.info("The number of configs that are modified: {}",
                modifiedConfig.size());

        // get ctest runner and set up project path
        CTestRunnable ctestRunner = InputParser.getCTestRunner();
        ctestRunner.setProjectRootPath(InputParser.getTargetProjectRootPath());

        // filter out unaffected test that are not affected
        Set<String> affectedTest = CTestUtil.filterUnaffectedTest(
                paramTestMapping,
                modifiedConfig,
                toBeTestedTest);
        LOGGER.info("The number of tests that are affected: {}",
                affectedTest.size());

        // inject modified configuration
        ctestRunner.injectConfig(modifiedConfig);

        // run CTest
        Map<String, String> additionalCtx = InputParser.
                getCMDParamForTargetProject();
        ctestRunner.runCTest(additionalCtx, affectedTest);

        // parse result
        Pair<Map<String, String>, Map<String, String>> results =
                ctestRunner.parseResult(affectedTest);
        Map<String, String> successfulTest = results.getValue0();
        Map<String, String> failedTest = results.getValue1();

        LOGGER.info("Result Overview");
        LOGGER.info("Success: {}", successfulTest.size());
        LOGGER.info("Fail: {}", failedTest.size());
        LOGGER.info("Skip: {}",
                toBeTestedTest.size()
                        - successfulTest.size()
                        - failedTest.size());
    }
}
