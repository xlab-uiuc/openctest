import re
import subprocess
import os
import glob
import json
import sys


global_results = {}
all_test_cases = set()
all_params = set()


def remove_nested_keys(json_data, params):
   if isinstance(json_data, dict):
       for key in list(json_data.keys()):
           direct_key = key in params
           nested_keys = [p for p in params if p.startswith(key + '.')]
          
           if direct_key:
               del json_data[key]
           elif nested_keys:
               adjusted_nested_keys = [p.split('.', 1)[1] for p in nested_keys]
               remove_nested_keys(json_data[key], adjusted_nested_keys)
           else:
               remove_nested_keys(json_data[key], params)
   elif isinstance(json_data, list):
       for item in json_data:
           remove_nested_keys(item, params)


def flatten_json(y):
   out = {}


   def flatten(x, name=''):
       if type(x) is dict:
           for a in x:
               flatten(x[a], name + a + '.')
       elif type(x) is list:
           i = 0
           for a in x:
               flatten(a, name + str(i) + '.')
               i += 1
       else:
           out[name.rstrip('.')] = x


   flatten(y)
   return out


def extract_data(log_directory):
   global global_results, all_test_cases, all_params
   log_files = os.listdir(log_directory)


   for log_file in log_files:
       parts = log_file.split('-')
       test_file_name = parts[0]
       test_case_name = '-'.join(parts[1:]).rsplit('.log', 1)[0].replace(' ', '_')


       all_test_cases.add(f"{test_file_name}: {test_case_name}")


       with open(os.path.join(log_directory, log_file), 'r') as file:
           content = file.read()


       json_pattern = re.compile(r"\[CTEST\]\[GET-PARAM\] #### (.*?) ####", re.DOTALL)
       json_match = json_pattern.search(content)
       json_data = None
       if json_match:
           json_data_str = json_match.group(1)
           try:
               json_data = json.loads(json_data_str)
           except json.JSONDecodeError:
               json_data = None


       if json_data:
           flattened_data = flatten_json(json_data)
           all_params.update(flattened_data.keys())


       if test_file_name not in global_results:
           global_results[test_file_name] = {}
       global_results[test_file_name][test_case_name] = json_data


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


def write_to_file(filename, data):
   with open(filename, 'w') as file:
       json.dump(data, file, indent=2)


if len(sys.argv) != 3:
   print("Usage: script.py <directory_path> <log_directory>")
   sys.exit(1)


directory_path = sys.argv[1]
log_directory = sys.argv[2]


process_directory(directory_path)
extract_data(log_directory)


write_to_file('result_mapping.json', global_results)
print("Results written to result_mapping.json")


write_to_file('all_test_cases.json', list(all_test_cases))
print("Test cases written to all_test_cases.json")


write_to_file('all_params.json', list(all_params))
print("Parameters written to all_params.json")