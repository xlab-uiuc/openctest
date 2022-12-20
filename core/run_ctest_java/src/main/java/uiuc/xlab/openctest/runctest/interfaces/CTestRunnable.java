package uiuc.xlab.openctest.runctest.interfaces;

import java.nio.file.Path;
import java.util.Map;
import java.util.Set;

import org.javatuples.Pair;

public interface CTestRunnable {
    /**
     * Pass project root path to supported project.
     *
     * @param rootPath an absolute root path of the target project.
     *
     */
    void setProjectRootPath(Path rootPath);

    /**
     * Inject modified configuration values into the target project.
     *
     * @param updatedConfig a map of updated configurations given by user.
     *
     */
    void injectConfig(Map<String, Object> updatedConfig);

    /**
     * Run test methods.
     * The context should contain two keys, 'args' and 'props'. For example:
     * you can pass `-q` to `args` or `maven.antrun.skip=true` to 'props'.
     * The test methods should be in following format:
     * testclassname#testmethodname
     *
     * @param context      a map of additional context for running tests.
     * @param affectedTest a list of the full name of the test methods.
     *
     */
    void runCTest(Map<String, String> context, Set<String> affectedTest);

    /**
     * Parse result of test methods.
     * The test methods should be in following format:
     * testclassname#testmethodname
     *
     * @param affectedTest a list of the full name of the test methods.
     * @return a pair of mapping of successful test name and execution
     * duration and mapping of failed test name and error message.
     *
     */
    Pair<Map<String, String>, Map<String, String>> parseResult(
            Set<String> affectedTest);
}
