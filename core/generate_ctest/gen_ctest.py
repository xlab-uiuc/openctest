import subprocess
import csv
import json
import os


def read_tsv(file_path):
    params = {}
    with open(file_path) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            param, *values = row
            params[param] = values
    return params


def read_json(file_path):
    with open(file_path) as file:
        return json.load(file)


def run_test_case(param, value, test_cases, report):
    for test_case in test_cases:
        test_file, test_name = test_case.split(": ")
        test_name = test_name.replace('_', ' ')
        test_file_path = f"/home/ikarna2/project/fork/superset/superset-websocket/spec{test_file}"


        # Generate the JSON configuration command
        gen_json_cmd = ["python3", "gen_json.py", param, value, "config.test.override.json"]
        print("Executing command:", ' '.join(gen_json_cmd))
        subprocess.run(gen_json_cmd)
        
        # Run the test case command
        test_cmd = ["python3", "ctest_runner_json_override.py", "config.test.override.json",
            "/home/ikarna2/project/fork/superset/superset-websocket", test_file_path, f'"{test_name}"']
        print("Executing command:", ' '.join(test_cmd))
        result = subprocess.run(test_cmd, capture_output=True, text=True)


        # Process the result
        if result.returncode == 0:
            test_result = 'p'
        else:
            test_result = 'f'
        
        # Assuming the execution time is part of the result output
        execution_time = extract_execution_time(result.stdout)


        report.append([param, test_case, value, test_result, execution_time])




def extract_execution_time(output):
    # Extract execution time from the output
    # Placeholder for actual implementation
    return "time_placeholder"


def write_report(report, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in report:
            writer.writerow(row)


def main():
    tsv_file = 'default_params.tsv'  # Placeholder for TSV file path
    json_file = 'flattened_params_to_tests.json'  # Placeholder for JSON file path
    report_file = 'test_report.csv'


    params = read_tsv(tsv_file)
    test_mapping = read_json(json_file)
    report = []


    for param, values in params.items():
        test_cases = test_mapping.get(param, [])
        for value in values:
            if value != 'SKIP':
                run_test_case(param, value, test_cases, report)


    write_report(report, report_file)


if __name__ == "__main__":
    main()