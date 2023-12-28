import os
import json
from utils import copyContents, findFilesInDirWithExt, replaceLine
import subprocess
import re
from ansi2html import Ansi2HTMLConverter
from bs4 import BeautifulSoup

projectSrcDir = './PerturbedSamples/Csv-1/'
projectCompileDir = "./PerturbedSamples/perform-compilation"
intermediateTrainDataDir = "./PerturbedSamples/PerturbedJsons"
jsonExt = "json"
BASH_COMPLIE_PATH = "./bash/compile.sh"
BASH_TEST_PATH = "./bash/run_test.sh"
NO_OF_TEST_CASES = 3

def handleBugContentElement(bugContentElement):
    fromCheckoutProjectBugFilePath = bugContentElement["filepath"]
    bugFilePath = projectCompileDir + fromCheckoutProjectBugFilePath
    replaceLine(bugFilePath, bugContentElement["bug-line"], bugContentElement["bug"])

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def getHtmlErrors(result):
    converter = Ansi2HTMLConverter(inline=True)
    html_errors = converter.convert(result.stdout)
    return html_errors

def getErrorMsg(error_msg):
    return extractCompilationError(remove_html_tags(getHtmlErrors(error_msg)))
    


# def extract_expected_actual(input_string):
#     pattern = r'Expected: is "(.*?)"\s*but: was "(.*?)"'
#     match = re.search(pattern, input_string)
#     if match:
#         expected = match.group(1)
#         actual = match.group(2)
#         return f'Expected: is "{expected}"\n     but: was "{actual}"'
#     else:
#         return None

def extract_expected_actual(input_string):
    pattern = r'Expected: is "(.*?)"\s*but: was "(.*?)"'
    matches = re.finditer(pattern, input_string, re.DOTALL)
    
    result_list = []
    for i, match in enumerate(matches):
        if i < NO_OF_TEST_CASES:
            expected = match.group(1)
            actual = match.group(2)
            result_list.append(f'Expected: is "{expected}"\n     but: was "{actual}"')
        else:
            break
    
    return "\n".join(result_list)

def getTestFailureError(text):
    text = remove_html_tags(getHtmlErrors(text))
    if "BUILD SUCCESS" in text or "BUILD FAILURE" not in text:
        return None
    
    if "<<< ERROR!" in text:
        text = text.split("<<< ERROR!")[-1].strip()
        text =  text.split("\n")[0].strip()
        
        if text != "":
            
            return text
        return None
    
    if "Failed tests:" not in text:
        return None
    
    text = text.split("Failed tests:")[-1]

    if "Tests run:" not in text:
        return None

    text = text.split("Tests run:")[0].strip()

    text =  extract_expected_actual(text)
    
    return text

def find_pom_path(folder):
    for root, dirs, files in os.walk(folder):
        #print(dirs)
        for file in files:
            # print(file)
            if file.endswith("pom.xml"):
                path_to_pom =  os.path.join(root, file)
                return path_to_pom[:-7]
    return None


def getCompileResult(projectCompileDir):
    # compile directory
    result = subprocess.run(['bash', BASH_COMPLIE_PATH,projectCompileDir], capture_output=True, text=True)
    # print(result.stdout)
    return result

def getTestRunResults(projectCompileDir):
    # execute tests and get results
    result = subprocess.run(['bash', BASH_TEST_PATH,projectCompileDir], capture_output=True, text=True)
    # print(result.stdout)

    return result

def checkForCompilationError(result):
    pattern = r'COMPILATION ERROR'
    match = re.search(pattern, result)
    if match:
        return True
    else:
        return False


def extractCompilationError(result):
    if "Compilation failure" in result:
        result = result.strip()
        result = result.split("Compilation failure")[-1]
        if "->" not in result:
            return None
        
        result = result.split("->")[0]
        result = result.replace("[ERROR] ", "")
        result = result.strip()
        error_msg = ""
        for i in result.split("\n"):
            removed_spaces = i.strip(" ")
            if removed_spaces.startswith("/"):
                if ":" in removed_spaces:
                    removed_spaces = removed_spaces.split(":")[-1]
                    if "]" in removed_spaces:
                        removed_spaces = removed_spaces.split("]")[-1]
                        removed_spaces = removed_spaces.strip()
                    else:
                        removed_spaces = removed_spaces.strip()
                    if removed_spaces != "" and removed_spaces not in error_msg:
                        error_msg += removed_spaces+", "
                
            elif "symbol" in removed_spaces or "reason" in removed_spaces:
                if removed_spaces not in error_msg:
                    error_msg += removed_spaces+", "
        if error_msg == "":
            return None
        
        return error_msg.strip(", ")
    else:
        return None

def remove_newlines(text):
    text=  text.strip()
    text = text.replace("\n", ", ")
    return re.sub(r'\s+', ' ', text)

def overideFileContent(filePath, content):
    with open(filePath, "w") as file:
        file.write(content)



if __name__ == "__main__":
    copyContents(projectSrcDir, projectCompileDir)
    pom_path = find_pom_path(projectCompileDir)
    if not pom_path:
        print("No .pom file found in the specified folder.")
        exit(1)

    
    intermediateTrainDataJsonFiles = findFilesInDirWithExt(intermediateTrainDataDir, jsonExt)
    print(intermediateTrainDataJsonFiles)
    print(os.getcwd())
    

    for intermediateTrainDataJsonFilePath in intermediateTrainDataJsonFiles: 
        print("---------------------------------------------------\n\n\n\n")
        
        try:
            with open(intermediateTrainDataJsonFilePath, "r") as intermediateTrainDataJsonFile:
                fileContent = json.load(intermediateTrainDataJsonFile)
        except FileNotFoundError:
            print(f"Error: File not found - {intermediateTrainDataJsonFilePath}")
        
        train_data = []
        # print(len(fileContent))
        # exit(1)
        for bugContentElement in fileContent:
            handleBugContentElement(bugContentElement)
            print(bugContentElement["bug"])
            print(bugContentElement["fix"])            
            
            # compile directory
            error_msg = ""
            result = getCompileResult(pom_path)

            if checkForCompilationError(result.stdout):
                error_msg = getErrorMsg(result)
                if not error_msg:
                    copyContents(projectSrcDir, projectCompileDir)
                    print("Compilation error but no error message found\n\n\n\n")
                    continue
            else:
                test_result =  getTestRunResults(pom_path)
                error_msg = getTestFailureError(test_result)
                
                if not error_msg:
                    copyContents(projectSrcDir, projectCompileDir)
                    print("No test failure error message found\n\n\n\n")
                    continue

    
            print("Error message: ", error_msg)
            error_msg = remove_newlines(error_msg)
            print("Error message: ", error_msg)
            print("---------------------------------------------------\n\n\n\n")

            bugContentElement["err"] = error_msg
            train_data.append(bugContentElement)

            copyContents(projectSrcDir, projectCompileDir)
        overideFileContent(intermediateTrainDataJsonFilePath, json.dumps(train_data, indent=1))
        
        
            # break


        
