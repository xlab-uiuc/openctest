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


def process_file(file, result_mapping, all_params_set, all_test_cases_list):
    test_cases_list = []
    config_list = [] # for all test cases 
    file_name = ""
   
    with open(directory_path + file, 'r') as file:
        for line in file:
            match = re.search(pattern, line.strip())
            if match:
                json_str = match.group(1)
                data = json.loads(json_str)
                config_list.append(data)
                flattened_data = flatten_dict(data)
                all_params_set.update(flattened_data.keys())


            file_match = re.search(file_pattern, line.strip())
            if file_match:
                file_name = file_match.group(1)


            test_cases = re.findall(test_pattern, line.strip())
            if test_cases:
                for case in test_cases:
                    test_cases_list.append(case)
                    all_test_cases_list.append(f"{file_name}: {case}")


    values_list = []
    for case in test_cases_list:
        mapping = {}
        mapping[case] = config_list
        values_list.append(mapping)


    test_mapping = {}
    test_mapping[file_name] = values_list
    result_mapping.append(test_mapping)


files_in_directory = os.listdir(directory_path)
files = [file for file in files_in_directory if os.path.isfile(os.path.join(directory_path, file))]


result_mapping = []
all_params_set = set()
all_test_cases_list = []


for file in files:
    process_file(file, result_mapping, all_params_set, all_test_cases_list)


with open('result_mapping.json', 'w+') as file:
    file.write(json.dumps(result_mapping, indent=4))
    print("Successfully generated mappings - result_mapping.json")


with open('all_params.txt', 'w+') as file:
    for param in sorted(all_params_set):
        file.write(param + '\n')
    print("Successfully generated all parameters in nested format - all_params.txt")


with open('all_test_cases.txt', 'w+') as file:
    for test_case in all_test_cases_list:
        file.write(test_case + '\n')
    print("Successfully generated all test cases - all_test_cases.txt")