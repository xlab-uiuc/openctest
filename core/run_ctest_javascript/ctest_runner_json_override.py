import os
import shutil
import subprocess
import sys


def move_file(file_name, dest_dir):
    new_file_name = "config.test.override.json"
    if not os.path.isfile(file_name):
        print("File does not exist.")
        return
    if not os.path.exists(dest_dir):
        print("Destination directory does not exist, creating it.")
        os.makedirs(dest_dir)
    new_file_path = os.path.join(dest_dir, new_file_name)
    shutil.move(file_name, new_file_path)
    print(f"File {file_name} moved and renamed to {new_file_path}")


def run_jest_test(test_case_path, test_case_name):
    print("Running the npx jest command with the specified test case")
    try:
        result = subprocess.run(['npx', 'jest', test_case_path, '-t', test_case_name], check=True)
        if result.returncode == 0:
            print("CTest PASS")
        else:
            print(f"CTest FAIL: {result.returncode}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"CTest FAIL: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 ctest_runner_json_override.py <file_name> <destination_directory> <jest_test_case_path> <jest_test_case_name>")
        sys.exit(1)


    file_name = sys.argv[1]
    dest_dir = sys.argv[2]
    test_case_path = sys.argv[3]
    test_case_name = sys.argv[4]


    move_file(file_name, dest_dir)
    run_jest_test(test_case_path, test_case_name)