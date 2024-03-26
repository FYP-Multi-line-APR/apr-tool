import re 
import os
import shutil
import json

prediction_token = "<extra_id_0>"
bug_token = "[BUG]"
context_token = "[CONTEXT]"

id_field = "id"
filepath_field = "filepath"
bug_field = "bug"
fix_field = "fix"
ctx_field = "ctxs"
txt_field = "txt"
start_bug_line_field = "start-bug-line"
end_bug_line_field = "end-bug-line"

run_keyword = "Run"
failure_keyword = "Failure"
error_keyword = "Error"
skipped_keyword = "Skipped"

def print_dict(data):
    print(json.dumps(data, indent=2))

def get_unique_item_list(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result

def copyContents(source_directory, destination_directory):
    try:
        if os.path.exists(destination_directory):
            shutil.rmtree(destination_directory)
        # Copy the entire directory and its contents to the destination
        shutil.copytree(source_directory, destination_directory, dirs_exist_ok=True)
        print(f"Code copied successfully from '{source_directory}' to '{destination_directory}'.")
    except shutil.Error as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def replace_prediction_token(input_str, replacement):
    return input_str.replace(prediction_token, replacement)

def replace_placeholder(input_str, placeholder, replacement):
    return input_str.replace(placeholder, replacement)

def replaceLine(file_path, line_number, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    if 1 <= line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print(f"Line {line_number} in {file_path} replaced successfully.")
    else:
        print(f"Error: Line number {line_number} is out of bounds.")

def getTestFailureCount(mavenTestResult):
    pattern = r'Tests run: (\d+), Failures: (\d+)'
    match = re.search(pattern, mavenTestResult)
    if match:
        testRunCount = match.group(1)
        testFailCount = match.group(2)
    else:
        print("Given Result doesn't contain test failure count")
        testFailCount = -1 
    return testFailCount

def findFilesInDirWithExt(dirPath, ext):
    # Ensure the directory path is valid
    if not os.path.exists(dirPath) or not os.path.isdir(dirPath):
        raise ValueError(f"The directory '{dirPath}' does not exist or is not a valid directory.")

    # Get a list of all files in the directory
    allFiles = os.listdir(dirPath)

    # Filter files based on the extension
    filteredFiles = [file for file in allFiles if file.endswith(f".{ext}")]

    # Create full file paths
    filePaths = [os.path.join(dirPath, file) for file in filteredFiles]
    return filePaths

def write_json(file_path, json_data):
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)

def write_lines_to_file(file_path, lines):
    print(f"writing files to: {file_path}")
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def write_to_file(file_path, text_to_write):
    try:
        with open(file_path, 'w') as file:
            file.write(text_to_write)
        print(f"Successfully wrote to {file_path}")
    except IOError as e:
        print(f"Error: {e}")

def append_to_file(file_path, text_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write(text_to_append + '\n')
        print(f"Appended '{text_to_append}' to {file_path}")
    except IOError as e:
        print(f"Error: {e}")

def get_json_data(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def file_path_exists(file_path):
    return os.path.exists(file_path)

def get_list_of_dirs_in(current_dir):
    directories = [dir_path for dir_path in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, dir_path))]
    return directories

def get_files_inside_dir(dir_path):
    return os.listdir(dir_path)

def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        print(f"already exist. dir: {dir_path}")

def read_file_lines(file_path):
    lines = []
    with open(file_path, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def get_mvn_repo_final_test_result(mvn_test_output):
    final_result = {
        run_keyword: 0,
        failure_keyword: 0,
        error_keyword: 0,
        skipped_keyword: 0
    }
    for line in mvn_test_output.split("\n"):
        matched_line = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)", line)
        if matched_line:
            tests_run = int(matched_line.group(1))
            failures = int(matched_line.group(2))
            errors = int(matched_line.group(3))
            skipped = int(matched_line.group(4))

            final_result[run_keyword] += tests_run
            final_result[failure_keyword] += failures
            final_result[error_keyword] += errors
            final_result[skipped_keyword] += skipped
    return final_result

if __name__ == "__main__":
    # filepathFromCheckoutDir = "/src/main/java/org/apache/maven/plugin/compiler/CompilerMojo.java"
    # bugLineNo = 36
    # bug = "int operand2 = 5;"
    # dirPath = "./PerturbedSamples/perform-compilation/"
    # pathFromCheckoutDir = "Calculator.java"
    # replaceLine(dirPath+pathFromCheckoutDir, bugLineNo, bug)

    directoryPath = "./PerturbedSamples"
    fileExtension = "json"
    result = findFilesInDirWithExt(directoryPath, fileExtension)
    print(result)

