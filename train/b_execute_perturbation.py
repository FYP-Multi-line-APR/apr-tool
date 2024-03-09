#!/usr/bin/python
import sys, os, time, subprocess,fnmatch, shutil, csv,re, datetime, json, re
from itertools import permutations
import copy
from utils import replaceLine
from collect_context import get_function_content_with_prediction_token_without_comments
from collect_context import get_full_file_context_with_prediction_token_without_comments
from collect_context import collect_context, get_context_with_prediction_token_without_comments
from get_function_names_in_java_file import extract_class_name_for_file, extract_method_signatures_for_file
from get_function_names_in_java_file import classname_field, method_signatures_field

# bugIds = ['Cli-1']
# checkoutProjectTo = 'Perturbation-Cli-1'
# projectDir = "/Cli-1"

# bugIds = ['Csv-1']
# checkoutProjectTo = 'Perturbation-Csv-1'
# projectDir = "/Csv-1"

bugIds = []
checkoutProjectTo = 'Perturbation-'
projectDir = "/"

trainDataJsonFilepath = "/PerturbedJsons/train-data.json"
trainDataTxtFilePath = "./PerturbedSamples/PerturbedJsons/train-data.txt"
trainDataTwoMultiLinesJsonFilepath = "/PerturbedJsons/train-data-two-multi-lines.json"
codeFilesInfoFilePath = "/PerturbedJsons/code-files-info.json"

outputData = []
outputDataTwoMultiLines = []

codeFileInfoDict = {}

id = 0
def getNextTrainDataId():
    # read file and get
    global id 
    id += 1
    return id

def getListOfDictsForContexts(contextList):
    output = []
    for context in contextList:
        output.append({
            "txt": context
        })
    return output 

def generateDataDict(id, startBugLine, endBugLine, bug, fix, fixes, err, ctxs, filepathFromCheckoutDir, action):
    data = {
        "id": id, 
        "filepath": filepathFromCheckoutDir,
        "start-bug-line": startBugLine,
        "end-bug-line": endBugLine,
        "bug": bug,
        "fix": fix,
        "fixes": fixes,
        "err": err,
        "ctxs": ctxs,
        "action": action
    }
    return data

def start(bugId,repodir,rootdir):
    projectPath=repodir+'/'+bugId
    traveProject(bugId, projectPath,repodir)

def traveProject(bugId,projectPath,repodir):
    # print(projectPath)
    listdirs = os.listdir(projectPath)
    for f in listdirs:
        pattern = '*.java'
        p = os.path.join(projectPath, f)
        if os.path.isfile(p):
            if fnmatch.fnmatch(f, pattern) and ('Test' not in p and 'test' not in p) :
                filePathFromCheckout = p.split(checkoutProjectTo, 1)[1]
                with open(p,'r') as perturbFile:
                    lines = perturbFile.readlines()
                    if len(lines)>0:
                        for k in range(0,len(lines)):
                            # constructTrainSample(bugId, lines[k], p, repodir, True, rootdir, filePathFromCheckout)
                            construct_large_train_sample(bugId, lines[k], p, repodir, True, rootdir, filePathFromCheckout)
        else:
            traveProject(bugId,p,repodir)

    with open(repodir+trainDataJsonFilepath, 'w') as trainDataJsonFile:
        json.dump(outputData, trainDataJsonFile, indent=2)
    
    with open(repodir+codeFilesInfoFilePath, 'w') as codeFilesInfoFile: 
        json.dump(codeFileInfoDict, codeFilesInfoFile, indent=2)

    # generateTwoMultiLineBugs()
    # with open(repodir+trainDataTwoMultiLinesJsonFilepath, 'w') as trainDataJsonFile:
    #     json.dump(outputDataTwoMultiLines, trainDataJsonFile, indent=2)
   
def generateTwoMultiLineBugs():
    lengthTwoPermutations = permutations(outputData, 2)
    lengthTwoPermutationList = list(lengthTwoPermutations)

    skip_rate = max(int(len(outputData)/5), 1)
    i = 0
    for i in range(0, len(lengthTwoPermutationList), skip_rate):
        lengthTwoPermutation = lengthTwoPermutationList[i]

        bug1 = lengthTwoPermutation[0]
        bug2 = lengthTwoPermutation[1]
        newBug = copy.deepcopy(bug1)

        if bug2["bug-line"] == bug1["bug-line"]:
            continue

        if bug2["ctx-lines"][0][0] < newBug["bug-line"] < bug2["ctx-lines"][0][1]:
            continue
        else:
            bug2ContextWithFix = generateContextWithPatch(bug2)
            newBug["ctxs"].append({
                "txt": bug2ContextWithFix
            })
            newBug["ctx-lines"].append(bug2["ctx-lines"][0])
            outputDataTwoMultiLines.append(newBug)

        i += 1

def generateContextWithPatch(bugInfoInJson):
    # print("======generateContextWithPatch====")
    # print(bugInfoInJson)
    fix = bugInfoInJson["fix"]
    contexts = bugInfoInJson["ctxs"]

    context = contexts[0]
    contextText = context["txt"]

    bug_start = contextText.find('<BUG>')
    bug_end = contextText.find('</BUG>') + len('</BUG>')

    fixed_text = contextText[:bug_start] + fix + contextText[bug_end:]
    fixed_text = fixed_text.replace('<BUG>', '').replace('</BUG>', '')
    return fixed_text

def generateBuggyLineContext(line, lineIdx, buggyLineNos, corruptCode):
    buggyLineNo1 = buggyLineNos[0]
    buggyLineNo2 = buggyLineNos[1]
    buggyLineNo3 = buggyLineNos[2]
    buggyLineNo4 = buggyLineNos[3]
    buggyLineNo5 = buggyLineNos[4]
    if lineIdx == int(buggyLineNo1)-1:
        line ='<BUG> '+corruptCode + ' </BUG> '
    elif buggyLineNo2.isdigit() and lineIdx == int(buggyLineNo2)-1:
        line =''
    elif buggyLineNo3.isdigit() and lineIdx == int(buggyLineNo3)-1:
        line =''
    elif buggyLineNo4.isdigit() and lineIdx == int(buggyLineNo4)-1:
        line =''
    elif buggyLineNo5.isdigit() and lineIdx == int(buggyLineNo5)-1:
        line =''
    return line

def processContextLines(contextLines):
    result = []
    for line in contextLines:
        line = line.strip()
        if line and not line.startswith("//") and not line.startswith("/*") and line != "":
            line = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"', '""', line)
            result.append(line)
    return result

def findBugLineRange(bugLineNos):
    startLineNo = int(bugLineNos[0])
    endLineNo = int(bugLineNos[0])
    for bugLineNo in bugLineNos:
        if bugLineNo.isdigit():
            bugLineNoVal = int(bugLineNo)
            if endLineNo < bugLineNoVal:
                endLineNo = bugLineNoVal
    return startLineNo, endLineNo

def contextContainsStrings(context):
    if "\"" in context:
        return True
    return False

def getMethodNamesOfFile(filepath):
    pass

def construct_large_train_sample(bugId,line,targetfile,repodir,diagnosticFlag,rootdir, filepathFromCheckoutDir):
    codeFilePath = targetfile.replace("Perturbation-","")
    sample=''
    cxt=''
    filename = targetfile.split('/')[-1]
    originFile = targetfile.replace("Perturbation-","")

    if not '^' in line:
        return
    infos = line.split('^')
    if len(infos) < 11:
        return
    if len(infos) > 11:
        return
    curruptCode =  infos[1]

    lineNo1 =  infos[2] 
    lineNo2 =  infos[3] 
    lineNo3 =  infos[4] 
    lineNo4 =  infos[5]
    lineNo5 =  infos[6]

    groundTruth = infos[9]
    groundTruth = groundTruth.replace('  ',' ').replace('\r','').replace('\n','')
    action = infos[0] 

    if '\"' in groundTruth or '\"' in lineNo1 or '\"' in lineNo2 or '\"' in lineNo3 or '\"' in lineNo4 or '\"' in lineNo5:
        return

    curruptCode = curruptCode.replace(' (','(').replace(' )',')')
    curruptCode = curruptCode.replace('(  )','()')
    curruptCode = curruptCode.replace(' .','.')
    
    groundTruth = groundTruth.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
    curruptCode = curruptCode.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')

    buggyLineNos = [lineNo1, lineNo2, lineNo3, lineNo4, lineNo5]

    startBugLineNo, endBugLineNo = findBugLineRange(buggyLineNos)
    originalFile = targetfile.replace("Perturbation-", "")

    all_file_cxts = get_full_file_context_with_prediction_token_without_comments(originalFile, startBugLineNo, endBugLineNo)

    id = getNextTrainDataId()
    
    bugLine = int(lineNo1)
    bug = curruptCode
    fix = groundTruth
    fixes = []
    err = ''
    
    ctxs = getListOfDictsForContexts(all_file_cxts)
    data = generateDataDict(id, startBugLineNo, endBugLineNo, bug, fix, fixes, err, ctxs, filepathFromCheckoutDir, action)
    outputData.append(data)
    addJavaFileInfoToGlobalDict(codeFilePath, filepathFromCheckoutDir)
    append_to_file(trainDataTxtFilePath, str(data) + "\n")


def constructTrainSample(bugId,line,targetfile,repodir,diagnosticFlag,rootdir, filepathFromCheckoutDir):
    codeFilePath = targetfile.replace("Perturbation-","")
    project = bugId.split('-')[0]

    sample=''
    cxt=''
    filename = targetfile.split('/')[-1]
    originFile = targetfile.replace("Perturbation-","")

    if not '^' in line:
        return
    infos = line.split('^')
    if len(infos) < 11:
        return
    if len(infos) > 11:
        return
    curruptCode =  infos[1]

    lineNo1 =  infos[2] 
    lineNo2 =  infos[3] 
    lineNo3 =  infos[4] 
    lineNo4 =  infos[5]
    lineNo5 =  infos[6]
    cxtStart = infos[7]
    cxtEnd = infos[8]
    groundTruth = infos[9]
    metaInfo = infos[10]
    groundTruth = groundTruth.replace('  ',' ').replace('\r','').replace('\n','')
    action = infos[0] 

    if '\"' in groundTruth or '\"' in lineNo1 or '\"' in lineNo2 or '\"' in lineNo3 or '\"' in lineNo4 or '\"' in lineNo5:
        return

    try:
        string_int = int(lineNo1)
    except ValueError:
        return
    

    curruptCode = curruptCode.replace(' (','(').replace(' )',')')
    curruptCode = curruptCode.replace('(  )','()')
    curruptCode = curruptCode.replace(' .','.')
    
    # get diagnostic by execution
#     diagnosticMsg = diagnostic(bugId,line,targetfile,repodir,action,diagnosticFlag,rootdir)
    diagnosticMsg = ' '
    #get context info
    # print("===context lines===")
    # contextDict = {}
    
    # startContextLineNo = int(cxtStart)-2-contextWidth
    # endContextLineNo = int(cxtEnd)+contextWidth

    buggyLineNos = [lineNo1, lineNo2, lineNo3, lineNo4, lineNo5]

    # cxtLines = []
    # if cxtStart not in '' and cxtEnd not in '':
    #     with open(originFile,'r') as perturbFile:
    #         lines = perturbFile.readlines()
    #         for i in range(0,len(lines)):
    #             if i > startContextLineNo and i < endContextLineNo:
    #                 l = lines[i]
    #                 l = l.strip()
    #                 #remove comments
    #                 if  l.startswith('/') or l.startswith('*'):
    #                     l = ' '
    #                 l = l.replace('  ','').replace('\r','').replace('\n','')
    #                 l = generateBuggyLineContext(l, i, buggyLineNos, curruptCode)
    #                 if '\"' in l:
    #                     return False
    #                 cxt+=l+' '
    #                 cxtLines.append(l)

    # # print(cxtLines)
    # processedCtxLines = processContextLines(cxtLines)
    # cxt = " ".join(processedCtxLines)

    startBugLineNo, endBugLineNo = findBugLineRange(buggyLineNos)
    originalFile = targetfile.replace("Perturbation-", "")

    # cxt = get_function_content_with_prediction_token_without_comments(originalFile, startBugLineNo, endBugLineNo)
    # cxt = collect_context(originalFile, startBugLineNo, endBugLineNo, curruptCode)
    cxt = get_context_with_prediction_token_without_comments(originalFile, startBugLineNo, endBugLineNo)
    # all_file_cxts = get_full_file_context_with_prediction_token_without_comments(originalFile, startBugLineNo, endBugLineNo)
    if contextContainsStrings(cxt):
        return False

    os.system("mv "+repodir+"/"+filename +"  "+originFile)
    sample+='[BUG] [BUGGY] ' + curruptCode + diagnosticMsg+ ' [CONTEXT] ' + cxt +' '+'  '
    sample = sample.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
    groundTruth = groundTruth.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
    curruptCode = curruptCode.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')

    id = getNextTrainDataId()
    # # print("lineNo: ", lineNo1)
    bugLine = int(lineNo1)
    bug = curruptCode
    fix = groundTruth
    fixes = []
    err = ''
    # ctxBugLines = [(startContextLineNo, endContextLineNo)]
    
    ctxs = getListOfDictsForContexts([cxt])
    data = generateDataDict(id, startBugLineNo, endBugLineNo, bug, fix, fixes, err, ctxs, filepathFromCheckoutDir, action)
    print(f"data: {data}")
    outputData.append(data)
    addJavaFileInfoToGlobalDict(codeFilePath, filepathFromCheckoutDir)
    append_to_file(trainDataTxtFilePath, str(data) + "\n")

def addJavaFileInfoToGlobalDict(codeFilePath, filepathFromCheckoutDir):
    global codeFileInfoDict
    if codeFileInfoDict.get(codeFilePath) is None: 
        className = extract_class_name_for_file(codeFilePath)
        methodSignatures = extract_method_signatures_for_file(codeFilePath)
        infoDict = generateJavaFileInfoDict(className, methodSignatures)
        codeFileInfoDict[filepathFromCheckoutDir] = infoDict

def generateJavaFileInfoDict(className, methodSignatures): 
    return {
        classname_field: className,
        method_signatures_field: methodSignatures
    }

def append_to_file(file_path, content):
    try:
        file_exists = os.path.exists(file_path)
        if not file_exists:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(content))
            # print(f"File created at {file_path}")
        else:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(str(content))
            # print(f"Content appended to {file_path}")
    except Exception as e:
        print(f"Error: {e}")

def diagnostic(bugId,line,targetfile,repodir,action,executeFlag,rootdir):
    project = bugId.split('-')[0]
    line=line.replace('\r',' ').replace('\n',' ')
    filename = targetfile.split('/')[-1]
    originFile = targetfile.replace("Perturbation-","")
    # print("*****originFile originFile**** :"+originFile)
    # print("*****diagnostics**** :")


    #copy the origin file outside the project
    os.system("cp "+originFile+"  "+repodir)
    # initial perturb string
    perturbStr=''
    
    # print("target line:"+line)
    infos = line.split('^')
    curruptCode =  infos[1]  
    lineNo1 =  infos[2] 
    lineNo2 =  infos[3] 
    lineNo3 =  infos[4] 
    lineNo4 =  infos[5]
    lineNo5 =  infos[6]

    # print('**************Currupt Code*************'+curruptCode)
    
    
    if "Transplant" in action or "Replace" in action or "Move" in action or  "Insert" in action:
        # read and perturb code 
        with open(originFile,'r') as perturbFile:
            lines = perturbFile.readlines()
            for i in range(0,len(lines)):
                if i+1< int(lineNo1) or i+1> int(lineNo1)+4:
                    perturbStr+=lines[i]
                elif i+1==int(lineNo1):
                    perturbStr+=curruptCode+"\n"
                elif i+1==int(lineNo1)+1: 
                    if lineNo2=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+2:
                    if lineNo3=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+3:  
                    if lineNo4=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+4:
                    if lineNo5=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
    #REMOVE actions
    elif "P14_" in action or 'P15_' in action or 'P16_' in action:
        with open(originFile,'r') as perturbFile:
            lines = perturbFile.readlines()
            for i in range(0,len(lines)):
                if i+1< int(lineNo1) or i+1> int(lineNo1)+4:
                    perturbStr+=lines[i]
                elif i+1==int(lineNo1):
                    perturbStr+= curruptCode
                elif i+1==int(lineNo1)+1: 
                    if lineNo2=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+2:
                    if lineNo3=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+3:  
                    if lineNo4=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"
                elif i+1==int(lineNo1)+4:
                    if lineNo5=='':
                        perturbStr+=lines[i]
                    else:
                        perturbStr+=" \n"


  
    # write back the perturb code to class file
    with open(originFile,'w') as perturbFileWrite:
        perturbFileWrite.write(perturbStr)

    if executeFlag:
        execute_result = executePerturbation(bugId,repodir,originFile,action,line,rootdir)
    else:
        execute_result=''
    
    return execute_result


def executePerturbation(bugId,repodir,originFile,action,line,rootdir):
    bugId = bugId.replace('Perturbation-','')
    compile_error_flag = True

    program_path=repodir+'/'+bugId
    # print('****************'+program_path+'******************')
    #get compile result
    cmd = "cd " + program_path + ";"
    cmd += "timeout 90 defects4j compile"
    exectresult='[TIMEOUT]'
    symbolVaraible=''
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # print(result)
    # Running ant (compile.tests)
    if 'Running ant (compile)' in str(result):
        result = str(result).split("Running ant (compile)")[1]
        # print('===result==='+str(result))

        result=result.split('\n')
        for i in range(0,len(result)):
            if 'error: ' in result[i]:
                firstError=result[i].split('error: ')[1]
                exectresult=firstError.split('[javac]')[0]
                if '\\' in exectresult:
                    exectresult=exectresult.split('\\')[0]
                # print('===FirstError==='+firstError)
                # 'cannot  find  symbol      
                if 'symbol' in firstError and 'cannot' in firstError and 'find' in firstError:       
                    if '[javac]' in firstError:
                        lines = firstError.split('[javac]')
                        for l in lines:
                            if 'symbol:'in l and 'variable' in l:
                                symbolVaraible=l.split('variable')[1]
                                if '\\' in symbolVaraible:
                                    symbolVaraible=symbolVaraible.split('\\')[0]
                                break



                exectresult='[CE] '+exectresult+symbolVaraible
                break
            elif 'OK' in result[i]:
                exectresult='[FE]'
                compile_error_flag=False



    if not compile_error_flag:
        #get test result
        cmd = "cd " + program_path + ";"
        cmd += "timeout 180 defects4j test"
        result=''
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # print(result)
        if 'Failing tests: 0' in str(result):
            exectresult='[NO-ERROR]'
        elif 'Failing tests' in str(result):
            result=str(result).split('Failing tests:')[1]
            result=str(result).split('-')
            for i in range(1,len(result)):
                failingtest = result[i]
                if '::' not in failingtest and i+1<len(result):
                    failingtest = result[i+1]
                if '\\' in failingtest:
                    failingtest = failingtest.split('\\')[0]
                failingtest=failingtest.strip()

                if '::' in failingtest:
                    failingTestMethod=failingtest.split('::')[1]
                    faildiag = getFailingTestDiagnostic(failingtest,program_path)
                    exectresult = '[FE] ' + faildiag +' '+failingTestMethod
                else:
                    exectresult = '[FE] '
                break



    os.chdir(rootdir)

    with open(repodir+'/diagnostic.csv','a')  as csvfile:
        filewriter = csv.writer(csvfile, delimiter='\t',  escapechar=' ', 
                                quoting=csv.QUOTE_NONE)               
        filewriter.writerow([exectresult,line])

    return exectresult



def getFailingTestDiagnostic(failingtest,program_path):
    testclass = failingtest.split("::")[0]

    cmd = "cd " + program_path + ";"
    cmd += "timeout 120 defects4j monitor.test -t "+failingtest
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if 'failed!' in str(result) :
        result = str(result).split('failed!')[1]
        if testclass in str(result):
            result = str(result).split(testclass)[1]
            if '):' in str(result):
                result = str(result).split('):')[1]
                if '\\' in str(result):
                    result = str(result).split('\\')[0]
    else:
        result =''
    
    return str(result)




def getFailingTestSourceCode(failingtest,program_path):
    code=''
    if os.path.exists((program_path+'/tests')):
        program_path = program_path+'/tests/'
    elif os.path.exists(program_path+'/test'):
        program_path = program_path+'/test/'
    elif os.path.exists(program_path+'/src/test/java'):
        program_path = program_path+'/src/test/java/'
    elif os.path.exists(program_path+'/src/test'):
        program_path = program_path+'/src/test/'
    elif os.path.exists(program_path+'/gson/src/test/java'):
        program_path = program_path+'/gson/src/test/java/'

    testclass = failingtest.split("::")[0]
    testmethod = failingtest.split("::")[1]
    testclass=testclass.replace('.','/')
    testclass = testclass+'.java'

    fullpath = program_path+testclass

    if os.path.exists(fullpath):    
        startflag=False
        code =''
        with open(fullpath,'r') as codefile:
            lines=codefile.readlines()
            for l in lines:
                if 'public' in l  and 'void' in l and testmethod in l:
                    startflag=True
                if 'public' in l and 'void' in l and testmethod not in l:
                    startflag=False
                if startflag:
                    if 'assert' in l:
                        l = l.strip()
                        if l not in code:
                            code=l
    return code

if __name__ == '__main__':
    # bugIds = ['Lang-65','Chart-26','Math-106','Mockito-38','Time-26','Closure-134','Cli-1','Collections-25','Codec-1','Compress-1','Csv-1','Gson-1','JacksonCore-1','JacksonDatabind-1','JacksonXml-1','Jsoup-1','JxPath-1'] 
    bug_name = sys.argv[1]

    trainDataJsonFilepath = f"/PerturbedJsons/train-data-{bug_name}.json"
    trainDataTxtFilePath = f"./PerturbedSamples/PerturbedJsons/train-data-{bug_name}.txt"
    codeFilesInfoFilePath = f"/PerturbedJsons/code-files-info-{bug_name}.json"

    bugIds = [bug_name]
    checkoutProjectTo = 'Perturbation-' + bug_name
    projectDir = "/" + bug_name

    rootdir= './'
    repodir = rootdir+'PerturbedSamples'
    
    for bugId in bugIds:
        project=bugId.split('-')[0]
        bugNo = bugId.split('-')[1]

        bugId = bugId.replace(project, "Perturbation-"+project)
        start(bugId,repodir,rootdir)