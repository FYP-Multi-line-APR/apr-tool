#!/usr/bin/python
import sys, os, subprocess,fnmatch, shutil, csv, re, datetime


if __name__ == '__main__':
    project=sys.argv[1]
    bug=sys.argv[2]
    checkout=sys.argv[3]
    checkout.replace(' ','')
    if checkout in 'init':
        checkout=True
    else:
        checkout=False
        
    CURRENT_PATH = "/content/apr-tool"
    
    #checkout the project
    if checkout:
        if os.path.exists(CURRENT_PATH + "/projects/"+project+bug):
            os.system("rm -rf "+ CURRENT_PATH +"/projects/"+project+bug)
        checkout_project="defects4j checkout -p " + project +" -v "+ bug+"b  -w" +CURRENT_PATH +"/projects/"+project+bug
        os.system(checkout_project)

    print("=====================checkout completed========================")
    
    
    #get project information
    project_info="defects4j info -p "+ project +" -b " +bug
    infos = os.popen(project_info).read()
    infos=str(infos)
    tests = infos.split("List of modified sources:")[0]
    tests = tests.split("Root cause in triggering tests:")[1]
    sources = infos.split("List of modified sources:")[1]

    print("=====================Project information collected========================")
    
    #infomation of failing tests
    fail_tests = ""
    tests=tests.split(" - ")
    for t in tests:
        if "::" in t:
            t = t.split("::")[0]
            t = t.replace("\n","").replace("\r","")
            if t not in fail_tests:
                fail_tests+=t+"#*:" 
    fail_tests = fail_tests[:len(fail_tests)-1]
    print("fail_tests:"+fail_tests)

    print("=====================Information of failed test collected========================")
    
    source_files = ""
    sources=sources.split(" - ")
    for s in sources:
        s =s.split("--")[0]
        s = s.replace("\n","").replace("\r","")
        if s not in source_files:
            source_files+=s+":" 
    source_files = source_files[:len(source_files)-1]
    print("source_files:"+source_files)

    print("=====================Source files are founded========================")
    
    #copy run.sh to the target project
    if "Closure" in project:
        os.system(f"cp {CURRENT_PATH}/run_gzoltar_fl_Closure-after.sh {CURRENT_PATH}/projects/"+project+bug)
        os.system(f'mv  {CURRENT_PATH}/projects/'+project+bug+'/run_gzoltar_fl_Closure-after.sh  ./projects/'+project+bug+'/run_gzoltar_fl.sh')
    else:
        os.system(f"cp {CURRENT_PATH}/run_gzoltar_fl.sh {CURRENT_PATH}/projects/"+project+bug)
  

   
    #compile target project
    os.chdir(f"{CURRENT_PATH}/projects/"+project+bug)
    os.system("defects4j compile")
    print("=====================Target project compiled========================")
    
    currentpath=os.path.dirname(os.path.realpath(__file__))
    print("currentpath:"+currentpath)
    #create build folder
    if "Cli" in project or 'Math' in project or 'Compress' in project or 'Gson' in project or 'Csv' in project  or 'JacksonCore' in project  or 'JacksonDatabind' in project or 'Jsoup' in project:
        if os.path.exists("./target"):
            print("target exists")
            os.system("mkdir build")
            os.system("mkdir build-tests")
            os.system("cp -rf ./target/classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build-tests/")
    if "Codec" in project : 
        if os.path.exists("./target"):
            os.system("mkdir build")
            os.system("mkdir build-tests")
            os.system("cp -rf ./target/classes/*" + "  ./build/")
            os.system("cp -rf ./target/tests/*" + "  ./build/")
            os.system("cp -rf ./target/tests/*" + "  ./build-tests/")
                                                                  
        
    if 'Time' in project:
        if os.path.exists("./target"):
            os.system("mkdir build")
            os.system("mkdir build-tests")
            os.system("cp -rf ./target/classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build-tests/")
        elif os.path.exists("./build"):
            os.system("mkdir build-tests")
            os.system("cp -rf ./build/classes/*" + "  ./build/")
            if os.path.exists("./build/tests"):
                os.system("cp -rf ./build/tests/*" + "  ./build/")
                os.system("cp -rf ./build/tests/*" + "  ./build-tests/")

    if "Closure" in project:
        if os.path.exists("./build/classes"):
            os.system("mkdir build-tests")
            os.system("cp -rf ./build/classes/*" + "  ./build/")
            os.system("cp -rf ./build/test/*" + "  ./build/")
            os.system("cp -rf ./build/test/*" + "  ./build-tests/")
#             os.system("cp -rf ./build/lib/*" + "  ./lib/")
#             os.system("cp -rf ./lib/classes/*" + "  ./lib/")
    
    if "Lang" in project:
        if os.path.exists("./target") and os.path.exists("./target/tests"):
            os.system("mkdir build")
            os.system("mkdir build-tests")
            os.system("cp -rf ./target/classes/*" + "  ./build/")
            os.system("cp -rf ./target/tests/*" + "  ./build/")
            os.system("cp -rf ./target/tests/*" + "  ./build-tests/")
        elif os.path.exists("./target") and os.path.exists("./target/test-classes"):
            os.system("mkdir build")
            os.system("mkdir build-tests")
            os.system("cp -rf ./target/classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build/")
            os.system("cp -rf ./target/test-classes/*" + "  ./build-tests/")

    print("=====================Project Builed========================")        
    
    #execute the Gzoltar FL
    print("final execution completed")

        # get list of the files in the current directory
    print("current path:"+currentpath)
    files = os.listdir(currentpath)
    print("CP\WD",os.getcwd())

    command = ["chmod", "+x", f"{CURRENT_PATH}/run_gzoltar_fl.sh"]
    # Use subprocess.run() to execute the command
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("=====================Subprocess Executed========================") 
  
    fl_result = os.popen(f"{CURRENT_PATH}/projects/{project}{bug}/run_gzoltar_fl.sh --instrumentation online --failtests "+fail_tests+" --sourcefiles "+source_files).read()       
    print("result :",fl_result)
    print("=====================FL Results collected========================") 
    
    with open("./FL_execution.txt","w") as fl_file:
        fl_file.write(f"{CURRENT_PATH}/run_gzoltar_fl.sh --instrumentation online --failtests "+fail_tests+" --sourcefiles "+source_files)
        print("=====================Execution process completed========================") 
   
    with open("./FL_result.txt","w") as fl_result_file:
        fl_result_file.write(fl_result)

    print("=====================Results are write and save========================") 
        
    
    
