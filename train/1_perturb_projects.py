#!/usr/bin/python
import sys, os, time, subprocess,fnmatch, shutil, csv,re, datetime
import shutil

def perturb(bugId,repodir,rootdir):
    projectPath=repodir+'/'+bugId
    traveProject(projectPath)
    

def deleteAllExceptGiven(directory, directory_to_keep):
    # Get a list of all directories in the parent directory
    all_directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    # Iterate through all directories and delete those not equal to the directory_to_keep
    for to_delete in all_directories:
        if to_delete != directory_to_keep:
            try:
                print(os.path.join(directory, to_delete))
                # Use shutil.rmtree for recursive deletion (including subdirectories and files)
                shutil.rmtree(os.path.join(directory, to_delete))
                print(f'Successfully deleted: {to_delete}')
            except FileNotFoundError:
                print(f'Folder not found: {to_delete}')
            except OSError as e:
                print(f'Error deleting folder {to_delete}: {e}')


def traveProject(projectPath):
    listdirs = os.listdir(projectPath)
    for f in listdirs:
        if  'test' not in projectPath and 'Test' not in projectPath:
            pattern = '*.java'
            p = os.path.join(projectPath, f)
            if os.path.isfile(p):
                if 'test' not in p and fnmatch.fnmatch(f, pattern): 
                    print(p)
                    #call spoon based Java pertubation programs.
                    callstr = 'timeout 600 java -jar ./perturbation_model/target/perturbation-0.0.1-SNAPSHOT-jar-with-dependencies.jar '
                    callstr+=p+' SelfAPR '
                    os.system(callstr)
                    print(p)

            else:
                traveProject(p)



if __name__ == '__main__':
   
    # bugIds = ['Lang-65','Chart-26','Math-106','Mockito-38','Time-26','Closure-134','Cli-1','Collections-25','Codec-1','Compress-1','Csv-1','Gson-1','JacksonCore-1','JacksonDatabind-1','JacksonXml-1','Jsoup-1','JxPath-1']
    # bugIds = ['Cli-1']
    bugId = 'Csv-1'
    rootdir= './'
    repodir = rootdir+'PerturbedSamples'
    perturbJASONs = repodir+'/PerturbedJsons'
    
    
    if not os.path.exists(repodir):
        exit(0)
    
    deleteAllExceptGiven(repodir,bugId)
    if not os.path.exists(perturbJASONs):
        os.mkdir(perturbJASONs)
    # for bugId in bugIds:
    perturb(bugId,repodir,rootdir)