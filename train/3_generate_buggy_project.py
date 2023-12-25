import json
from utils import copyContents, findFilesInDirWithExt, replaceLine

projectSrcDir = './PerturbedSamples/Cli-1/'
projectCompileDir = "./PerturbedSamples/PerturbedJsons/perform-compilation"
intermediateTrainDataDir = "./PerturbedSamples/PerturbedJsons"
jsonExt = "json"

def handleBugContentElement(bugContentElement):
    fromCheckoutProjectBugFilePath = bugContentElement["filepath"]
    bugFilePath = projectCompileDir + fromCheckoutProjectBugFilePath
    replaceLine(bugFilePath, bugContentElement["bug-line"], bugContentElement["bug"])



if __name__ == "__main__":
    copyContents(projectSrcDir, projectCompileDir)
    intermediateTrainDataJsonFiles = findFilesInDirWithExt(intermediateTrainDataDir, jsonExt)
    for intermediateTrainDataJsonFilePath in intermediateTrainDataJsonFiles: 
        with open(intermediateTrainDataJsonFilePath, "r") as intermediateTrainDataJsonFile:
            fileContent = json.load(intermediateTrainDataJsonFilePath)
        for bugContentElement in fileContent:
            handleBugContentElement(bugContentElement)
            # compile directory
            # execute tests and get results
            # remove applied changes
            copyContents(projectSrcDir, projectCompileDir)
            # update bugContent with error diagnostic messages
            
        
