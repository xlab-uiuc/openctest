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
     */
    public void setProjectRootPath(Path rootPath);

    /**
     * Inject modified configuration values into the target project.
     *
     * @param updatedConfig a map of updated configurations given by user.
     */
    public void injectConfig(Map<String, String> updatedConfig);

    /**
     * Run test methods.
     *
     * @param context      a map of additional context for running tests. It will
     *                     contain two keys, 'args' and 'props'. For example, you
     *                     can pass `-q` to `args` or `maven.antrun.skip=true` to
     *                     `props`.
     * @param affectedTest a list of the full name of the test methods. Test format:
     *                     testclassname#testmethodname
     */
    public void runCTest(Map<String, String> context, Set<String> affectedTest);

    /**
     * Parse result of test methods.
     *
     * @param affectedTest a list of the full name of the test methods. format:
     *                     testclassname#testmethodname
     *
     * @return a pair of mapping of successful test name and execution duration and
     *         mapping of failed test name and error message. Test format:
     *         testclassname#testmethodname
     */
    public Pair<Map<String, String>, Map<String, String>> parseResult(Set<String> affectedTest);
}
