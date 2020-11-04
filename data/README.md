


# Ctest Dataset

**historical_issues**:  All 64 real-world configuration-induced failure issues we reproduced and the corresponding ctests that detect the root-cause configuration changes of these issues.

- `64issues.tsv`: tsv file with each row recording the project name,  the issue ID, the corresponding ctest that detected the root cause misconfiguration,  the issue link, and the issue title.

**docker_config_file_eval**:  All evaluated configuration files extracted from Docker Hub images. The detected misconfigured configuration parameters, and the corresponding ctests that detect the misconfigured parameters.

- `docker_misconfig.tsv`: tsv file with each row recording the project name, a detected misconfigured parameter, the corresponding configuration file, error type, and a ctest that detected the misconfiguration. 
- `{project}/DockerHubID.Image.*`: Configuration files extracted from Docker images.

**injected_misconfig_eval**:  All the injected configuration errors, and the corresponding ctests that detect each injected errors.

- `injected_misconfig.tsv`: tsv file with each row recording the project name, parameter name, and injected erroneous value. 
- `failed_ctest_{project}.tsv`:  tsv file with each row recording the parameter, a ctest that failed on the injected invalid value, and the injected invalid value.

**test_rewrite**:  All the rewritten ctests in the form of code patches.

- `test_rewrite.tsv`: tsv file with each row recording the project name, parameter, and a test rewrote.
- `*.patch`: rewritten ctests in the form of patches.
