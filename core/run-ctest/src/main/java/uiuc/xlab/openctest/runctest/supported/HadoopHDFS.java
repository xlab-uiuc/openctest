package uiuc.xlab.openctest.runctest.supported;

import org.apache.maven.shared.invoker.DefaultInvocationRequest;
import org.apache.maven.shared.invoker.DefaultInvoker;
import org.apache.maven.shared.invoker.InvocationRequest;
import org.apache.maven.shared.invoker.InvocationResult;
import org.apache.maven.shared.invoker.Invoker;
import org.apache.maven.shared.invoker.MavenInvocationException;
import org.javatuples.Pair;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.ProcessingInstruction;
import org.xml.sax.SAXException;
import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.IOException;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;


public final class HadoopHDFS implements CTestRunnable {
    private static final Logger LOGGER =
            LoggerFactory.getLogger(HadoopHDFS.class);
    private static final String SUREFIRE_OUTPUT_XML = "TEST-@.xml";
    /** root path of the target project. */
    private Path rootPath;
    /** path to surefire directory. */
    private Path surefirePath;
    /** path to the ctest injected configuration file. */
    private Path configInjectionPath;

    @Override
    public void setProjectRootPath(final Path rootPath) {
        this.rootPath = rootPath;
        surefirePath = Path.of(
                this.rootPath.toString(),
                "target/surefire-reports");
        configInjectionPath = Path.of(
                this.rootPath.toString(),
                "target/classes",
                "ctest-injected.xml");
    }

    @Override
    public void injectConfig(final Map<String, Object> updatedConfig) {
        // hadoop using xml to store configuration
        try {
            // delete old ctest-injected.xml file
            Files.deleteIfExists(configInjectionPath);

            // build the whole xml
            DocumentBuilderFactory docFactory =
                    DocumentBuilderFactory.newInstance();
            DocumentBuilder docBuilder = docFactory.newDocumentBuilder();

            // root elements
            Document doc = docBuilder.newDocument();
            Element rootElement = doc.createElement("configuration");
            doc.setXmlStandalone(true);
            ProcessingInstruction pi = doc.createProcessingInstruction(
                    "xml-stylesheet",
                    "type=\"text/xsl\" href=\"configuration.xsl\"");
            doc.appendChild(rootElement);
            doc.insertBefore(pi, rootElement);

            updatedConfig.forEach((param, val) -> {
                // add xml element for each modified configuration parameters
                Element property = doc.createElement("property");
                Element name = doc.createElement("name");
                name.setTextContent(param);
                property.appendChild(name);
                Element value = doc.createElement("value");
                value.setTextContent(val.toString());
                property.appendChild(value);
                rootElement.appendChild(property);
            });

            // write out
            try (OutputStream output =
                    Files.newOutputStream(configInjectionPath)) {
                TransformerFactory transformerFactory =
                        TransformerFactory.newInstance();

                // prohibit the use of all protocols by external entities
                transformerFactory.setAttribute(
                        XMLConstants.ACCESS_EXTERNAL_DTD,
                        "");
                transformerFactory.setAttribute(
                        XMLConstants.ACCESS_EXTERNAL_STYLESHEET,
                        "");

                Transformer transformer = transformerFactory.newTransformer();
                transformer.setOutputProperty(OutputKeys.INDENT, "yes");

                DOMSource source = new DOMSource(doc);
                StreamResult result = new StreamResult(output);

                transformer.transform(source, result);
                LOGGER.info(
                        "Injected modified config into: {}",
                        configInjectionPath);
            }
        } catch (IOException
                 | TransformerException
                 | ParserConfigurationException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void runCTest(
            final Map<String, String> context,
            final Set<String> affectedTest) {
        String testStr = getTestStr(affectedTest);
        InvocationResult result = execute(context, testStr);
        if (result != null) {
            LOGGER.info("run ctest result: {}", result);
        }
    }

    @Override
    public Pair<Map<String, String>, Map<String, String>> parseResult(
            final Set<String> affectedTest) {
        Map<String, List<String>> associatedMethods =
                getAssociatedMethods(affectedTest);
        Map<String, String> successfulTest = new HashMap<>();
        Map<String, String> failedTest = new HashMap<>();

        associatedMethods.forEach((className, methodNames) -> {
            Pair<Map<String, String>, Map<String, String>> results =
                    parseResult(className, methodNames);
            if (results == null) {
                return;
            }

            results.getValue0().forEach((test, time) ->
                    successfulTest.put(className + "#" + test, time));

            results.getValue1().forEach((test, err) ->
                    failedTest.put(className + "#" + test, err));
        });

        return new Pair<>(successfulTest, failedTest);
    }

    private String getTestStr(final Set<String> affectedTest) {
        // hadoop used Maven to manage the project, and Maven supports running
        // multiple tests at once. We will build the test string in here.

        Map<String, List<String>> associatedMethods =
                getAssociatedMethods(affectedTest);

        // group tests by their class to resue test fixure
        StringBuilder sb = new StringBuilder();
        associatedMethods.forEach((className, methodNames) -> {
            sb.append(className);
            sb.append("#");
            sb.append(String.join("+", methodNames));
            sb.append(",");
        });

        return sb.toString();
    }

    private Map<String, List<String>> getAssociatedMethods(
            final Set<String> affectedTest) {
        Map<String, List<String>> associatedMethods = new HashMap<>();
        affectedTest.forEach(test -> {
            String[] cm = test.split("#");
            String className = cm[0];
            String methodName = cm[1];

            associatedMethods.computeIfAbsent(
                    className,
                    k -> new ArrayList<>()).add(methodName);
        });
        return associatedMethods;
    }

    private Set<String> getMavenArgs(final Map<String, String> context) {
        Set<String> mavenArgs = new HashSet<>();

        if (!context.containsKey("args")) {
            return mavenArgs;
        }

        String[] args = context.get("args").split(",");
        mavenArgs.addAll(Arrays.asList(args));
        return mavenArgs;
    }

    private Map<String, String> getMavenProps(
            final Map<String, String> context) {
        Map<String, String> mavenProps = new HashMap<>();

        if (!context.containsKey("props")) {
            return mavenProps;
        }

        String[] props = context.get("props").split(",");

        for (String p : props) {
            String[] pSplit = p.strip().split("=");
            mavenProps.put(pSplit[0], pSplit[1]);
        }
        return mavenProps;
    }

    private InvocationResult execute(
            final Map<String, String> context,
            final String testStr) {
        Set<String> mavenArgs = getMavenArgs(context);
        Map<String, String> mavenProps = getMavenProps(context);
        InvocationRequest request = new DefaultInvocationRequest();

        // set pom path
        Path pomPath = Path.of(rootPath.toString(), "pom.xml");
        request.setPomFile(pomPath.toFile());

        // set mvn goal
        if (Boolean.parseBoolean(
                mavenProps.getOrDefault("use.surefire", "false"))) {
            request.setGoals(List.of("surefire:test"));
        } else {
            request.setGoals(List.of("test"));
        }

        // set additional properties
        Properties props = new Properties();
        props.setProperty("test", testStr);
        mavenProps.forEach(
                props::setProperty);
        request.setProperties(props);

        // set additional raw arguments
        mavenArgs.forEach(
                request::addArg);

        // set timeout
        int timeout = Integer.parseInt(
                mavenProps.getOrDefault("mvn.timeout", "-1"));
        if (timeout > 0) {
            request.setTimeoutInSeconds(timeout);
        }

        Invoker invoker = new DefaultInvoker();
        InvocationResult result = null;
        try {
            result = invoker.execute(request);
        } catch (MavenInvocationException e) {
            e.printStackTrace();
        }

        return result;
    }

    private Pair<Map<String, String>, Map<String, String>> parseResult(
            final String className,
            final List<String> methods) {
        String resultFileName = SUREFIRE_OUTPUT_XML.replace("@", className);
        Path resultFilePath = Path.of(surefirePath.toString(), resultFileName);
        if (!resultFilePath.toFile().exists()) {
            LOGGER.info(
                    "Cannot locate surefile report file in: {}",
                    resultFilePath);
            return null;
        }

        Map<String, String> successfulTest = new HashMap<>();
        Map<String, String> failedTest = new HashMap<>();
        Set<String> expectedTest = new HashSet<>(methods);

        LOGGER.info("Reading surefire results from {}", resultFilePath);

        try {
            // parse result xml file
            DocumentBuilderFactory docFactory =
                    DocumentBuilderFactory.newInstance();

            // completely disable DOCTYPE declaration
            docFactory.setFeature(
                    "http://apache.org/xml/features/disallow-doctype-decl",
                    true);

            DocumentBuilder db = docFactory.newDocumentBuilder();
            Document doc = db.parse(resultFilePath.toFile());

            // get testsuite node
            Element testsuite = doc.getDocumentElement();

            // get testcase nodes
            NodeList testcases = testsuite.getElementsByTagName("testcase");
            if (testcases.getLength() != methods.size()) {
                LOGGER.info(
                        "[strange] The number of actual executed test does not"
                        + "match the number of expected executed tests.");
            }

            for (int i = 0; i < testcases.getLength(); i++) {
                // get individual testcase node
                Node testcaseNode = testcases.item(i);
                if (testcaseNode.getNodeType() != Node.ELEMENT_NODE) {
                    continue;
                }

                Element testcase = (Element) testcaseNode;
                String executionDuration = testcase.getAttribute("time");
                String methodName = testcase.getAttribute("name");

                // skip unexpected test methods, for more info on why there
                // may be unexpected test methods, check explain below.
                if (!expectedTest.contains(methodName)) {
                    continue;
                }

                NodeList errorNodes = testcase.getElementsByTagName("error");
                NodeList failureNodes =
                        testcase.getElementsByTagName("failure");
                if (errorNodes.getLength() != 0) {
                    failedTest.put(
                            methodName, errorNodes.item(0).getTextContent());
                } else if (failureNodes.getLength() != 0) {
                    failedTest.put(
                            methodName, failureNodes.item(0).getTextContent());
                } else {
                    // populate runningTimes map
                    successfulTest.put(methodName, executionDuration);
                }
            }

            // in the surefire report file, some failed tests methods have
            // different names than that of the original test methods.
            // Typically, it results from the modified parameters causing
            // the test to fail before executing the test itself.
            // The name displayed in surefire report could be any
            // one of the following:
            // 1. test class initialization method name
            // 2. test class name
            // 3. empty string

            // we consider those expected test methods that are not
            // showing up in the surefire report file as failed.
            Map<String, String> additionalFailedTest = new HashMap<>();
            methods.forEach(test -> {
                if (!successfulTest.containsKey(test)
                        && !failedTest.containsKey(test)) {
                    additionalFailedTest.put(test,
                            "Cannot find surefire report for this test. "
                            + "Please check the surefire file for details.");
                }
            });
            failedTest.putAll(additionalFailedTest);
        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }

        return new Pair<>(successfulTest, failedTest);
    }
}
