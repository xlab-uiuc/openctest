import re
import subprocess
import os
import glob
import json
import sys


def flatten_json(y):
   out = {}


   def flatten(x, name=''):
       if isinstance(x, dict):
           for a in x:
               flatten(x[a], name + a + '.')
       elif isinstance(x, list): 
           i = 0
           for a in x:
               flatten(a, name + str(i) + '.')
               i += 1
       else:
           out[name.rstrip('.')] = x


   flatten(y)
   return out


def extract_test_names(file_path):
   try:
       with open(file_path, 'r') as file:
           content = file.read()
   except FileNotFoundError:
       return []


   pattern = re.compile(r"test\(['\"](.*?)['\"],|it\(['\"](.*?)['\"],")
   test_names = []


   for match in pattern.finditer(content):
       test_names.append(match.group(1) or match.group(2))


   return test_names


def run_test_case(file_path, test_name):
   file_name = os.path.basename(file_path)
   sanitized_test_name = test_name.replace(' ', '_').replace("'", "").replace('"', '')
   log_file_path = os.path.join('logs', f"{file_name}-{sanitized_test_name}.log")


   command = ["npx", "jest", file_path, "-t", test_name]
   with open(log_file_path, 'w') as log_file:
       subprocess.run(command, stdout=log_file, text=True)


def process_directory(directory_path):
   os.makedirs('logs', exist_ok=True)


   spec_files = glob.glob(os.path.join(directory_path, '**/*.test.ts'), recursive=True)
   spec_files.extend(glob.glob(os.path.join(directory_path, '**/*.spec.ts'), recursive=True))


   for file_path in spec_files:
       test_names = extract_test_names(file_path)
       for name in test_names:
           run_test_case(file_path, name)


def extract_data_and_map_params(log_directory):
   param_to_test_cases = {}
   log_files = os.listdir(log_directory)


   for log_file in log_files:
       parts = log_file.split('-')
       test_file_name = parts[0]
       test_case_name = '-'.join(parts[1:]).rsplit('.log', 1)[0].replace(' ', '_')
       test_case_identifier = f"{test_file_name}: {test_case_name}"


       with open(os.path.join(log_directory, log_file), 'r') as file:
           content = file.read()


       json_pattern = re.compile(r"\[CTEST\]\[GET-PARAM\] #### (.*?) ####", re.DOTALL)
       json_match = json_pattern.search(content)
       if json_match:
           json_data_str = json_match.group(1)
           try:
               json_data = json.loads(json_data_str)
               flattened_data = flatten_json(json_data)
               for param in flattened_data:
                   if param not in param_to_test_cases:
                       param_to_test_cases[param] = []
                   param_to_test_cases[param].append(test_case_identifier)
           except json.JSONDecodeError:
               pass  # Handle error or log as needed


   return param_to_test_cases


def write_to_file(filename, data):
   with open(filename, 'w') as file:
       json.dump(data, file, indent=2)


if len(sys.argv) != 3:
   print("Usage: gen_param_to_case.py <directory_path> <log_directory>")
   sys.exit(1)


directory_path = sys.argv[1]
log_directory = sys.argv[2]


process_directory(directory_path)
param_to_test_cases = extract_data_and_map_params(log_directory)


output_file_path = 'flattened_params_to_tests.json'
write_to_file(output_file_path, param_to_test_cases)
print(f"Mapping of flattened parameters to test cases written to {output_file_path}")