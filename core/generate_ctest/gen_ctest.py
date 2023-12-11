import json
import sys
import subprocess


def load_params(file_path):
    params = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                params.append((parts[0], parts[1]))  # (parameter, value)
    return params


def load_test_cases(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def run_test_case(param, value, test_case_path, test_case_name):
    try:
        # Constructing the command
        command = ['python3', 'ctest_runner.py', param, value, test_case_path, test_case_name]


        print(command)
        
        # Running the test case
        result = subprocess.run(command, check=True, capture_output=True, text=True)


        print(result.returncode)


        # Here you should parse the result to determine pass/fail and execution time
        # This is dependent on the output format of your testing framework
        test_result = 'p' if result.returncode == 0 else 'f'
        test_time = 'unknown'  # Extract this from the result if possible


        return test_result, test_time
    except subprocess.CalledProcessError as e:
        print(f"Error running the test case: {e}")
        return 'f', 'unknown'


def generate_test_report(params_file, test_cases_file, report_file):
    params = load_params(params_file)
    test_cases = load_test_cases(test_cases_file)


    with open(report_file, 'w') as file:
        file.write("parameter\ttest_case\tvalue\ttest_result\ttestcase_time\n")


        for param, value in params:
            if param in test_cases:
                for test_case in test_cases[param]:
                    test_case_name = test_case.split(': ')[-1]
                    test_case_path = test_case.split(':')[0]


                    test_result, test_time = run_test_case(param, value, test_case_path, test_case_name)
                    file.write(f"{param}\t{test_case_name}\t{value}\t{test_result}\t{test_time}\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: gen_ctest.py <params_file> <test_cases_file> <report_file>")
        sys.exit(1)


    params_file = sys.argv[1]
    test_cases_file = sys.argv[2]
    report_file = sys.argv[3]


    generate_test_report(params_file, test_cases_file, report_file)