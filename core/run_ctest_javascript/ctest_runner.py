import yaml
import subprocess
import sys
from collections import OrderedDict


# Custom loader with OrderedDict
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
   class OrderedLoader(Loader):
       pass
   def construct_mapping(loader, node):
       loader.flatten_mapping(node)
       return object_pairs_hook(loader.construct_pairs(node))
   OrderedLoader.add_constructor(
       yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
       construct_mapping)
   return yaml.load(stream, OrderedLoader)


# Custom dumper to maintain order
def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
   class OrderedDumper(Dumper):
       pass
   def _dict_representer(dumper, data):
       return dumper.represent_mapping(
           yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
           data.items())
   OrderedDumper.add_representer(OrderedDict, _dict_representer)
   return yaml.dump(data, stream, OrderedDumper, **kwds)


def update_yaml_hierarchy(file_path, hierarchy, value):
   # Load the existing YAML data from file
   with open(file_path, 'r') as file:
       data = ordered_load(file, yaml.SafeLoader)


   # Split the hierarchy input by dots to get the keys
   keys = hierarchy.split('.')


   # Traverse the data based on the hierarchy and set the value
   temp_data = data
   original_value = None
   try:
       for key in keys[:-1]:
           temp_data = temp_data[key]


       original_value = temp_data.get(keys[-1], None)  # Store original value
       temp_data[keys[-1]] = value
   except KeyError:
       return False, original_value  # Key not found in this file


   # Write the modified data back to the file
   with open(file_path, 'w') as file:
       ordered_dump(data, file, Dumper=yaml.SafeDumper, default_flow_style=False)
   return True, original_value  # Update was successful


def revert_yaml_change(file_path, hierarchy, original_value):
   update_yaml_hierarchy(file_path, hierarchy, original_value)


def run_jest_test(test_case_path, test_case_name):
   # print("Running the npx jest command for a specific test case")
   try:
       result = subprocess.run(['npx', 'jest', test_case_path, '-t', test_case_name], check=True)
       # if result.returncode == 0:
           # print("Jest test ran successfully!")
       # else:
           # print(f"Jest test failed with return code: {result.returncode}")
       return result.returncode
   except subprocess.CalledProcessError as e:
       # print(f"Error running the jest test: {e}")
       return 1


if __name__ == "__main__":
   if len(sys.argv) < 5:
       print("Usage: ctest_runner.py <dot-separated hierarchy> <new value> <jest_test_case_path> <jest_test_case_name>")
       sys.exit(1)


   hierarchy = sys.argv[1]
   value = sys.argv[2]
   test_case_path = sys.argv[3]
   test_case_name = sys.argv[4]


   # Try to convert value to int or float if possible
   try:
       value = int(value)
   except ValueError:
       try:
           value = float(value)
       except ValueError:
           pass


   # Paths of YAML files to check
   yaml_file_paths = [
       '/home/ikarna2/project/fork/forem/config/reactions.yml',
       '/home/ikarna2/project/fork/forem/config/locales/en.yml'
   ]


   updated = False
   original_value = None
   updated_file_path = ""
   for yaml_file_path in yaml_file_paths:
       success, original_value = update_yaml_hierarchy(yaml_file_path, hierarchy, value)
       if success:
           # print(f"Updated {hierarchy} in {yaml_file_path}")
           updated_file_path = yaml_file_path
           updated = True
           break


   if not updated:
       # print(f"Parameter {hierarchy} not found in the specified YAML files.")
       sys.exit(1)


   # Run Jest test case
   run_jest_test(test_case_path, test_case_name)


   # Revert changes in YAML file
   if original_value is not None:
       revert_yaml_change(updated_file_path, hierarchy, original_value)
       # print(f"Reverted changes to {hierarchy} in {updated_file_path}")