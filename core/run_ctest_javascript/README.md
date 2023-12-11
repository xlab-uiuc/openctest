# Running CTest


```
    python3 ctest_runner_json_override.py <file_name> <destination_directory> <jest_test_case_path> <jest_test_case_name>
```


```
    <file_name>: The name of the file to be moved and renamed. This is the source file that the script will operate on.


    <destination_directory>: The directory where the file will be moved to. If this directory does not exist, the script will create it.


    <jest_test_case_path>: The path to the Jest test case file. This is used to specify which Jest test case to run.


    <jest_test_case_name>: The specific name of the Jest test case to be executed. This allows the script to run a particular test case within a larger test suite.
```