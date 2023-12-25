import os
import json
from utils import copyContents, findFilesInDirWithExt, replaceLine

projectSrcDir = './PerturbedSamples/Csv-1/'
projectCompileDir = "./PerturbedSamples/perform-compilation"
intermediateTrainDataDir = "./PerturbedSamples/PerturbedJsons"
jsonExt = "json"

def handleBugContentElement(bugContentElement):
    fromCheckoutProjectBugFilePath = bugContentElement["filepath"]
    bugFilePath = projectCompileDir + fromCheckoutProjectBugFilePath
    replaceLine(bugFilePath, bugContentElement["bug-line"], bugContentElement["bug"])



if __name__ == "__main__":
    copyContents(projectSrcDir, projectCompileDir)
    intermediateTrainDataJsonFiles = findFilesInDirWithExt(intermediateTrainDataDir, jsonExt)
    print(os.getcwd())
    for intermediateTrainDataJsonFilePath in intermediateTrainDataJsonFiles: 
        print(intermediateTrainDataJsonFilePath)
        try:
            with open(intermediateTrainDataJsonFilePath, "r") as intermediateTrainDataJsonFile:
                fileContent = json.load(intermediateTrainDataJsonFile)
        except FileNotFoundError:
            print(f"Error: File not found - {intermediateTrainDataJsonFilePath}")
        
        for bugContentElement in fileContent:
            handleBugContentElement(bugContentElement)
            # compile directory
            # execute tests and get results
            # remove applied changes
            copyContents(projectSrcDir, projectCompileDir)
            # update bugContent with error diagnostic messages
            
        
