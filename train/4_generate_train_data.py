import os
import json

writeFilePath = './train-data/'
perturbedJsonsDirPah = "./PerturbedSamples/PerturbedJsons/"
jsonExt = ".json"

all_files = os.listdir(perturbedJsonsDirPah) 
json_files = [file for file in all_files if file.endswith(jsonExt)]

for json_file in json_files:
    file_path = os.path.join(perturbedJsonsDirPah, json_file)
    filename = file_path.split('/')[-1]
    outputData = []
    with open(file_path, 'r') as file:
        print(f"file_path: {file_path}")
        json_data = json.load(file)
        if (len(json_data) == 0):
            print("empty file")
        else:
            for jsonDataElement in json_data:
                outputData.append({
                    "id": jsonDataElement["id"],
                    "bug": jsonDataElement["bug"],
                    "fix": jsonDataElement["fix"],
                    "fixes": jsonDataElement["fixes"],
                    "err": jsonDataElement["err"],
                    "ctxs": jsonDataElement["ctxs"]
                })

    with open(writeFilePath+filename, 'w') as outputFile:
        json.dump(outputData, outputFile, indent=2)




