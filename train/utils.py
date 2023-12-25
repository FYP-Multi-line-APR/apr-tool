import re 
import os
import shutil

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

