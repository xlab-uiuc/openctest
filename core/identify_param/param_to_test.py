import re
import json
import os
import sys


pattern = r'\[CTEST\] #### (.*?) ####'
file_pattern = r'PASS (\S+)'
test_pattern = r'✓ (.*?) \(\d+ ms\)'
directory_path = sys.argv[1]


def flatten_dict(d, parent_key=''):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def process_file(file, param_to_tests):
    file_name = ""
   
    with open(directory_path + file, 'r') as file:
        for line in file:
            match = re.search(pattern, line.strip())
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                flattened_data = flatten_dict(data)


            file_match = re.search(file_pattern, line.strip())
            if file_match:
                file_name = file_match.group(1)


            test_cases = re.findall(test_pattern, line.strip())
            if test_cases:
                for case in test_cases:
                    test_case_full_name = f"{file_name}: {case}"
                    for param in flattened_data.keys():
                        if param not in param_to_tests:
                            param_to_tests[param] = []
                        param_to_tests[param].append(test_case_full_name)


files_in_directory = os.listdir(directory_path)
files = [file for file in files_in_directory if os.path.isfile(os.path.join(directory_path, file))]


param_to_tests = {}


for file in files:
    process_file(file, param_to_tests)


with open('param_to_test_cases_mapping.json', 'w+') as file:
    file.write(json.dumps(param_to_tests, indent=4))
    print("Successfully generated parameter to test cases mapping - param_to_test_cases_mapping.json")