package uiuc.xlab.openctest.runctest.supported;

import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;

public class CTestSupported {
    public static CTestRunnable getCTestRunner(String project) {
        switch (project.toLowerCase()) {
            case "hadoop-common":
                return new HadoopCommon();
            case "hadoop-hdfs":
                return new HadoopHDFS();
            case "cassandra":
                return null;
            default:
                return null; // TODO: raise exception
        }
    }
}
