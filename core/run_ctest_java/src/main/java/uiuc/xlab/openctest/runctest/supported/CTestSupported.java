package uiuc.xlab.openctest.runctest.supported;

import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;

public final class CTestSupported {
    private CTestSupported() {
        throw new IllegalStateException("Utility class cannot be instantiated");
    }

    /**
     * Return a CTestRunnable instance for a specific target project.
     *
     * @param project the name of the target project.
     * @return a CTestRunnable instance.
     */
    public static CTestRunnable getCTestRunner(final String project) {
        switch (project.toLowerCase()) {
            case "hadoop-common":
                return new HadoopCommon();
            case "hadoop-hdfs":
                return new HadoopHDFS();
            case "cassandra":
                return new Cassandra();
            default:
                throw new IllegalStateException(String.format(
                        "run-ctest doesn't support %s", project));
        }
    }
}
