package uiuc.xlab.openctest.runctest.supported;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.javatuples.Pair;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;

public class Cassandra implements CTestRunnable {
    static final Logger logger = LoggerFactory.getLogger(Cassandra.class);
    private static String JUNIT_OUTPUT_XML = "TEST-@-#.xml";

    Path rootPath;
    Path resultPath;
    Path configInjectionPath;

    @Override
    public void setProjectRootPath(Path rootPath) {
        this.rootPath = rootPath;
        resultPath = Path.of(rootPath.toString(), "build/test/output");
        configInjectionPath = Path.of(rootPath.toString(), "test/conf", "ctest-injected.yaml");
    }

    @Override
    public void injectConfig(Map<String, String> updatedConfig) {
        // cassandra using yaml to store configuration
        try {
            // delete old ctest-injected.yaml file
            Files.deleteIfExists(configInjectionPath);

            // write out
            FileWriter fw = new FileWriter(configInjectionPath.toFile());
            for (Map.Entry<String, String> conf : updatedConfig.entrySet()) {
                fw.write(String.format("%s: %s\n", conf.getKey(), conf.getValue()));
            }
            fw.close();

            logger.info("Injected modified config into: {}", configInjectionPath.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void runCTest(Map<String, String> context, Set<String> affectedTest) {
        Map<String, String> classTestMap = getClassTestMap(affectedTest);
        String cassandraBuildFile = rootPath.resolve("build.xml").toAbsolutePath().toString();
        String antArgs = getAntArgs(context);
        String antProps = getAntProps(context);

        try {
            for (Map.Entry<String, String> classTest : classTestMap.entrySet()) {
                String className = classTest.getKey();
                String testStr = classTest.getValue();
                String cmd = String.format("ant %s %s -buildfile %s testsome -Dtest.name=%s -Dtest.methods=%s", antArgs,
                        antProps,
                        cassandraBuildFile, className, testStr);

                Process process = Runtime.getRuntime().exec(cmd);

                // redirect ant output to standard output
                String line = null;
                BufferedReader is = new BufferedReader(new InputStreamReader(process.getInputStream()));

                while ((line = is.readLine()) != null) {
                    System.out.println(line);
                }

                process.waitFor();
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public Pair<Map<String, String>, Map<String, String>> parseResult(Set<String> affectedTest) {
        Map<String, String> successfulTest = new HashMap<>();
        Map<String, String> failedTest = new HashMap<>();

        for (String test : affectedTest) {
            String[] cm = test.split("#");
            String className = cm[0];
            String methodName = cm[1];

            String resultFileName = JUNIT_OUTPUT_XML.replace("@", className).replace("#", methodName);
            Path resultFilePath = Path.of(resultPath.toString(), resultFileName);
            if (!resultFilePath.toFile().exists()) {
                logger.info("Cannot locate surefile report file in: {}", resultFilePath.toString());
                return new Pair<Map<String, String>, Map<String, String>>(successfulTest, failedTest);
            }
            logger.info("Reading result from {}", resultFilePath.toString());

            // parse result xml file
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            try {
                DocumentBuilder db = dbf.newDocumentBuilder();
                Document doc = db.parse(resultFilePath.toFile());

                // get testsuite node
                Element testsuite = doc.getDocumentElement();

                // get testcase nodes
                NodeList testcases = testsuite.getElementsByTagName("testcase");
                if (testcases.getLength() != 1) {
                    logger.info("Cannot find result for test: {}", test);
                    continue;
                }

                // get individual testcase node
                Node testcaseNode = testcases.item(0);
                if (testcaseNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element testcase = (Element) testcaseNode;
                    String executionDuration = testcase.getAttribute("time");
                    String testedMethodName = testcase.getAttribute("name");

                    // in the report file, some failed tests methods have different names
                    // than that of the original test methods. Typically, it results from the
                    // modified parameters causing the test to fail before executing the test
                    // itself. The name displayed in surefire report could be any one of the
                    // following:
                    // 1. test class initialization method name
                    // 2. test class name
                    // 3. empty string
                    if (methodName.equals(testedMethodName)) {
                        // populate runningTimes map
                        successfulTest.put(className + "#" + methodName, executionDuration);
                    } else {
                        // populate errors map
                        NodeList errorNodes = testcase.getElementsByTagName("error");
                        if (errorNodes.getLength() != 0) {
                            failedTest.put(className + "#" + methodName, errorNodes.item(0).getTextContent());
                        }
                        NodeList failureNodes = testcase.getElementsByTagName("failure");
                        if (failureNodes.getLength() != 0) {
                            failedTest.put(className + "#" + methodName, failureNodes.item(0).getTextContent());
                        }
                    }
                }
            } catch (ParserConfigurationException | SAXException | IOException e) {
                e.printStackTrace();
            }
        }

        return new Pair<Map<String, String>, Map<String, String>>(successfulTest, failedTest);
    }

    private Map<String, String> getClassTestMap(Set<String> affectedTest) {
        // Cassandra uses ant to manage the project and ant allow running multiple test
        // in the same class at once. In here, we group that together.
        Map<String, List<String>> associatedMethods = new HashMap<>();
        affectedTest.forEach(test -> {
            String[] cm = test.split("#");
            String className = cm[0];
            String methodName = cm[1];

            associatedMethods.computeIfAbsent(className, k -> new ArrayList<>()).add(methodName);
        });

        // group tests by their class to resue test fixure
        Map<String, String> testMap = new HashMap<>();
        associatedMethods.forEach((className, methods) -> {
            testMap.put(className, String.join(",", methods));
        });

        return testMap;
    }

    private String getAntArgs(Map<String, String> context) {
        Set<String> antArgs = new HashSet<>();

        if (!context.containsKey("args")) {
            return "";
        }

        String[] args = context.get("args").split(",");
        for (String a : args) {
            antArgs.add(a);
        }

        return String.join(" ", antArgs);
    }

    private String getAntProps(Map<String, String> context) {
        if (!context.containsKey("props")) {
            return "";
        }

        String[] props = context.get("props").split(",");
        StringBuilder sb = new StringBuilder();
        sb.append("-D");
        for (String prop : props) {
            sb.append(prop);
            sb.append(" ");
        }

        return sb.toString();
    }
}
