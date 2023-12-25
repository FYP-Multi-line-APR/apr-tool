#!/usr/bin/python
import sys, os, time, subprocess,fnmatch, shutil, csv,re, datetime, json
from itertools import permutations
import copy
from utils import replaceLine

# bugIds = ['Cli-1']
# checkoutProjectTo = 'Perturbation-Cli-1'

bugIds = ['Csv-1']
checkoutProjectTo = 'Perturbation-Csv-1'

os.environ['PATH'] = os.environ['PATH'] + ":/home/chathuranga/Work/defects4j/framework/bin/"

trainDataJsonFilepath = "/PerturbedJsons/train-data.json"
trainDataTwoMultiLinesJsonFilepath = "/PerturbedJsons/train-data-two-multi-lines.json"

outputData = []
outputDataTwoMultiLines = []

projectDir = "/Csv-1"
compilationDir = "/perform-compilation/"

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

def generateDataDict(id, bugLine, bug, fix, fixes, err, ctxBugLines, ctxs, filepathFromCheckoutDir, action):
    data = {
        "id": id, 
        "filepath": filepathFromCheckoutDir,
        "bug-line": bugLine,
        "bug": bug,
        "fix": fix,
        "fixes": fixes,
        "err": err,
        "ctx-lines": ctxBugLines,
        "ctxs": ctxs,
        "action": action
    }
    return data

def start(bugId,repodir,rootdir):
    projectPath=repodir+'/'+bugId
    # move content in src dir to compilation dir
    traveProject(bugId, projectPath,repodir)

def traveProject(bugId,projectPath,repodir):
    print(projectPath)
    listdirs = os.listdir(projectPath)
    for f in listdirs:
        pattern = '*.java'
        p = os.path.join(projectPath, f)
        if os.path.isfile(p):
            # print(p)
            if fnmatch.fnmatch(f, pattern) and ('Test' not in p and 'test' not in p) :
                print("===filepath===")
                print(p)
                filePathFromCheckout = p.split(checkoutProjectTo, 1)[1]
                with open(p,'r') as perturbFile:
                    lines = perturbFile.readlines()
                    if len(lines)>0:
                        for k in range(0,len(lines)):
                            constructTrainSample(bugId, lines[k], p, repodir, True, rootdir, filePathFromCheckout)
                            # break
        else:
            traveProject(bugId,p,repodir)
        # break

    with open(repodir+trainDataJsonFilepath, 'w') as trainDataJsonFile:
        json.dump(outputData, trainDataJsonFile, indent=2)

    # generateTwoMultiLineBugs()
    # with open(repodir+'/train-data-2-lines.json', 'w') as trainDataJsonFile:
    #     json.dump(outputDataTwoMultiLines, trainDataJsonFile, indent=2)
    


    
def generateTwoMultiLineBugs():
    lengthTwoPermutations = permutations(outputData, 2)
    for lengthTwoPermutation in lengthTwoPermutations:
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



def generateContextWithPatch(bugInfoInJson):
    print("======generateContextWithPatch====")
    print(bugInfoInJson)
    fix = bugInfoInJson["fix"]
    contexts = bugInfoInJson["ctxs"]

    context = contexts[0]
    contextText = context["txt"]

    bug_start = contextText.find('<BUG>')
    bug_end = contextText.find('</BUG>') + len('</BUG>')

    fixed_text = contextText[:bug_start] + fix + contextText[bug_end:]
    fixed_text = fixed_text.replace('<BUG>', '').replace('</BUG>', '')
    return fixed_text

def constructTrainSample(bugId,line,targetfile,repodir,diagnosticFlag,rootdir, filepathFromCheckoutDir):
    print(f"targetfile: {targetfile}")
    print(f"repodir: {repodir}")
    project = bugId.split('-')[0]
    print(line)
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
    print("===context lines===")
    # contextDict = {}
    
    startContextLineNo = int(cxtStart)-2 
    endContextLineNo = int(cxtEnd)

    if cxtStart not in '' and cxtEnd not in '':
        with open(originFile,'r') as perturbFile:
            lines = perturbFile.readlines()
            for i in range(0,len(lines)):
                if i > int(cxtStart)-2 and i < int(cxtEnd):

                    l = lines[i]
                    l = l.strip()
                    #remove comments
                    if  l.startswith('/') or l.startswith('*'):
                        l = ' '
                    l = l.replace('  ','').replace('\r','').replace('\n','')
                    if i == int(lineNo1)-1:
                        l='<BUG> '+curruptCode + ' </BUG> '
                    cxt+=l+' '


    os.system("mv "+repodir+"/"+filename +"  "+originFile)
    sample+='[BUG] [BUGGY] ' + curruptCode + diagnosticMsg+ ' [CONTEXT] ' + cxt +' '+'  '
    sample = sample.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
    groundTruth = groundTruth.replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
    
    print("*****sample**** :"+sample)

    id = getNextTrainDataId()
    print("lineNo: ", lineNo1)
    bugLine = int(lineNo1)
    bug = curruptCode
    fix = groundTruth
    fixes = []
    err = ''
    ctxBugLines = [(startContextLineNo, endContextLineNo)]
    
    ctxs = getListOfDictsForContexts([cxt])
    # ctxs = contextDict
    
    
    # replace bugline
    fileToUpdate = repodir + compilationDir + targetfile.split("/")[-1]
    replaceLine(fileToUpdate, bugLine, bug)
    print(f"bugLine: {bugLine}")
    print(f"bug: {bug}")

    # compile and check test fail count 


    data = generateDataDict(id, bugLine, bug, fix, fixes, err, ctxBugLines, ctxs, filepathFromCheckoutDir, action)
    outputData.append(data)

    # with open(repodir+'/train-'+bugId+'.csv','a')  as csvfile:
    #     filewriter = csv.writer(csvfile, delimiter='\t',  escapechar=' ', 
    #                             quoting=csv.QUOTE_NONE)               
    #     filewriter.writerow([groundTruth,sample])




def diagnostic(bugId,line,targetfile,repodir,action,executeFlag,rootdir):
    project = bugId.split('-')[0]
    line=line.replace('\r',' ').replace('\n',' ')
    filename = targetfile.split('/')[-1]
    originFile = targetfile.replace("Perturbation-","")
    print("*****originFile originFile**** :"+originFile)
    print("*****diagnostics**** :")


    #copy the origin file outside the project
    os.system("cp "+originFile+"  "+repodir)
    # initial perturb string
    perturbStr=''
    
    print("target line:"+line)
    infos = line.split('^')
    curruptCode =  infos[1]  
    lineNo1 =  infos[2] 
    lineNo2 =  infos[3] 
    lineNo3 =  infos[4] 
    lineNo4 =  infos[5]
    lineNo5 =  infos[6]

    print('**************Currupt Code*************'+curruptCode)
    
    
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
    print('****************'+program_path+'******************')
    #get compile result
    cmd = "cd " + program_path + ";"
    cmd += "timeout 90 defects4j compile"
    exectresult='[TIMEOUT]'
    symbolVaraible=''
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(result)
    # Running ant (compile.tests)
    if 'Running ant (compile)' in str(result):
        result = str(result).split("Running ant (compile)")[1]
        print('===result==='+str(result))

        result=result.split('\n')
        for i in range(0,len(result)):
            if 'error: ' in result[i]:
                firstError=result[i].split('error: ')[1]
                exectresult=firstError.split('[javac]')[0]
                if '\\' in exectresult:
                    exectresult=exectresult.split('\\')[0]
                print('===FirstError==='+firstError)
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
        print(result)
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
    print('====result===='+str(result))
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

    print(failingtest+'&&&&&&&&failingtest')
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
    rootdir= '/home/chathuranga/Work/perturbation'
    repodir = rootdir+'/PerturbedSamples'
    
    for bugId in bugIds:
        project=bugId.split('-')[0]
        bugNo = bugId.split('-')[1]

        # if os.path.exists(repodir+'/'+bugId):
        #     os.system('rm -rf '+repodir+'/'+bugId)
        # os.system('defects4j checkout -p '+ str(project)+' -v '+str(bugNo)+'f   -w '+repodir+'/'+bugId)

        bugId = bugId.replace(project, "Perturbation-"+project)
        start(bugId,repodir,rootdir)