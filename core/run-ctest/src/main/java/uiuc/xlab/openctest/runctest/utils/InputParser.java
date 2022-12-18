package uiuc.xlab.openctest.runctest.utils;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.yaml.snakeyaml.Yaml;
import uiuc.xlab.openctest.runctest.interfaces.CTestRunnable;
import uiuc.xlab.openctest.runctest.supported.CTestSupported;

import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public final class InputParser {
    /** logger for this class. */
    private static final Logger LOGGER =
            LoggerFactory.getLogger(InputParser.class);

    private InputParser() {
        throw new IllegalStateException("Utility class cannot be instantiated");
    }

    /**
     * Return a CTestRunnable object.
     *
     * @return a CTestRunnable object.
     */
    public static CTestRunnable getCTestRunner() {
        String project = System.getProperty("project.name");
        if (project == null) {
            throw new NullPointerException("cannot read property project.name");
        }

        return CTestSupported.getCTestRunner(project);
    }

    /**
     * Return the path to the target project root directory.
     *
     * @return a Path object to the root directory of the target project.
     */
    public static Path getTargetProjectRootPath() {
        String projectPath = System.getProperty("project.path");
        if (projectPath == null) {
            throw new NullPointerException("cannot read property project.path");
        }

        return Paths.get(projectPath).toAbsolutePath();
    }

    /**
     * Return additional command line parameters passed to the target project.
     * <p> Example: you can suppress INFO log using `-Dproject.args=-q`.
     * Or, you can pass use.surefire=true to avoid recompiling using
     * `-Dproject.props=use.surefire=true`.
     *
     * @return a Map object containing additional parameters.
     */
    public static Map<String, String> getCMDParamForTargetProject() {
        String args = System.getProperty("project.args");
        String props = System.getProperty("project.props");

        Map<String, String> ctx = new HashMap<>();
        if (args != null) {
            ctx.put("args", args);
            LOGGER.info("Additional arguments passed into target project: {}",
                    args);
        }
        if (props != null) {
            ctx.put("props", props);
            LOGGER.info("Additional properties passed into target project: {}",
                    props);
        }

        return ctx;
    }

    /**
     * Return the json object containing mapping between configuration parameter
     * and associated test methods.
     *
     * @return a json object.
     */
    public static JSONObject getParamTestMappingJSON() {
        String mappingPath = System.getProperty("mapping.path");
        if (mappingPath == null) {
            throw new NullPointerException("cannot read property project.path");
        }

        // reading the param_unset_getter_map.json file
        mappingPath = Paths.get(mappingPath).toAbsolutePath().toString();
        JSONParser parser = new JSONParser();
        JSONObject jsonObj;
        try {
            Reader reader = new FileReader(mappingPath);
            jsonObj = (JSONObject) parser.parse(reader);
            return jsonObj;
        } catch (IOException | ParseException e) {
            e.printStackTrace();
        }

        return new JSONObject();
    }

    /**
     * Return a map containing all modified configurations based on user input.
     *
     * @return a Map object with key is configuration parameter and value is the
     * configuration value.
     */
    public static Map<String, Object> getModifiedConfig() {
        String confPairsStr = System.getProperty("conf.pairs");
        String confFilePathStr = System.getProperty("conf.file");
        if (confPairsStr == null && confFilePathStr == null) {
            throw new NullPointerException("cannot read property conf.pairs or"
                    + " conf.file, you need to specify one of them");
        } else if (confFilePathStr != null) {
            return getConfigFromFile(confFilePathStr);
        } else {
            return getConfigFromCommandLine(confPairsStr);
        }
    }

    private static Map<String, Object> getConfigFromFile(
            final String confFilePathStr) {
        Yaml yaml = new Yaml();

        try (InputStream input = new FileInputStream(confFilePathStr)) {
            return yaml.load(input);
        } catch (IOException ex) {
            ex.printStackTrace();
        }

        return new HashMap<>();
    }

    private static Map<String, Object> getConfigFromCommandLine(
            final String confPairsStr) {
        Map<String, Object> modifiedConfig = new HashMap<>();

        for (String param : confPairsStr.split(",")) {
            String[] paramPair = param.split("=");
            modifiedConfig.put(paramPair[0], paramPair[1]);
        }

        return modifiedConfig;
    }

    /**
     * Return a set of all tests that will be tested based on user input.
     *
     * @return a Set object containing all tests to be tested.
     */
    public static Set<String> getToBeTestedTest() {
        String testMethodsStr = System.getProperty("test.methods");
        String testFileStr = System.getProperty("test.file");
        if (testMethodsStr == null && testFileStr == null) {
            throw new NullPointerException("cannot read property test.methods"
                    + " or test.file, you need to specify one of them");
        } else if (testFileStr != null) {
            return getTestFromFile(testFileStr);
        } else {
            return getTestFromCommandLine(testMethodsStr);
        }
    }

    private static Set<String> getTestFromFile(final String testFileStr) {
        Set<String> tests = new HashSet<>();

        try {
            List<String> lines = Files.readAllLines(Paths.get(testFileStr));
            for (String line : lines) {
                tests.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return tests;
    }

    private static Set<String> getTestFromCommandLine(
            final String testMethodsStr) {
        Set<String> tests = new HashSet<>();
        tests.addAll(Arrays.asList(testMethodsStr.split(",")));
        return tests;
    }
}
