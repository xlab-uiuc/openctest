package uiuc.xlab.openctest.runctest;

import java.util.Map;
import java.util.Set;

import org.javatuples.Pair;
import org.json.simple.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;
import uiuc.xlab.openctest.runctest.utils.CTestUtil;
import uiuc.xlab.openctest.runctest.utils.InputParser;

public class CTestMain {
    private static final Logger logger = LoggerFactory.getLogger(CTestMain.class);

    public static void main(String[] args) {
        // get objects based on command line input
        Set<String> toBeTestedTest = InputParser.getToBeTestedTest();
        JSONObject paramTestMapping = InputParser.getParamTestMappingJSON();
        Map<String, String> modifiedConfig = InputParser.getModifiedConfig();
        logger.info("The number of configs that are modified: {}", modifiedConfig.size());

        // get ctest runner and set up project path
        CTestRunnable ctestRunner = InputParser.getCTestRunner();
        ctestRunner.setProjectRootPath(InputParser.getTargetProjectRootPath());

        // filter out unaffected test that are not affected
        Set<String> affectedTest = CTestUtil.filterUnaffectedTest(paramTestMapping, modifiedConfig,
                toBeTestedTest);
        logger.info("The number of tests that are affected: {}", affectedTest.size());

        // inject modified configuration
        ctestRunner.injectConfig(modifiedConfig);

        // run CTest
        Map<String, String> additionalCtx = InputParser.getCMDParamForTargetProject();
        ctestRunner.runCTest(additionalCtx, affectedTest);

        // parse result
        Pair<Map<String, String>, Map<String, String>> results = ctestRunner.parseResult(affectedTest);
        Map<String, String> successfulTest = results.getValue0();
        Map<String, String> failedTest = results.getValue1();

        // // print out results
        // logger.info("Result");
        // toBeTestedTest.forEach(test -> {
        //     if (successfulTest.containsKey(test)) {
        //         logger.info("SUCCESS - {}, execution duration: {}", test, successfulTest.get(test));
        //     } else if (failedTest.containsKey(test)) {
        //         logger.info("FAIL - {}", test);
        //     } else {
        //         logger.info("SKIP - {}", test);
        //     }
        // });

        logger.info("Result Overview");
        logger.info("Success: {}", successfulTest.size());
        logger.info("Fail: {}", failedTest.size());
        logger.info("Skip: {}", toBeTestedTest.size() - successfulTest.size() - failedTest.size());
    }
}
