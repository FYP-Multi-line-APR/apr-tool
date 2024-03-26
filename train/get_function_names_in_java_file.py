import re
import json
import sys 

classname_field = "classname"
method_signatures_field = "methodSignatures"

def extract_class_name_for_file(filepath):
    class_name = None
    with open(filepath, 'r') as f:
        java_code = f.read()
        class_name = extract_class_name(java_code)
    return class_name

def extract_method_signatures_for_file(filepath):
    method_signatures = None 
    with open(filepath, 'r') as f:
        java_code = f.read()
        method_signatures = extract_method_signatures(java_code)
    return method_signatures

def extract_method_signatures(java_code):
    # Define the regex pattern to match Java method declarations
    method_pattern = re.compile(r'(?:(?:public|private|protected|static|final|\s)+)?\s*([\w<>]+)\s+(\w+)\s*\(([^)]*)\)\s*{')

    # Find all matches in the Java code
    method_matches = method_pattern.findall(java_code)

    # Extract method signatures from matches
    method_signatures = [{'return_type': match[0], 'method_name': match[1], 'parameters': match[2]} for match in method_matches]

    return method_signatures

def extract_class_name(java_code):
    # Define the regex pattern to match the class name
    class_name_pattern = re.compile(r'\bclass\s+(\w+)\s*{')

    # Find the class name match in the Java code
    class_name_match = class_name_pattern.search(java_code)

    # Extract the class name
    class_name = class_name_match.group(1) if class_name_match else None

    return class_name

def extract_constructor_details(java_code,class_name):
    if class_name:
        # Define the regex pattern to match Java constructor declarations using the class name
        # constructor_pattern = re.compile(fr'{class_name}\s*\(([^)]*)\)\s*{')
        constructor_pattern = re.compile(fr'{class_name}\s*\(([^)]*)\)')

        # Find all matches in the Java code
        constructor_matches = constructor_pattern.findall(java_code)

        # Extract constructor details from matches
        constructor_details = [{'constructor_name': class_name, 'parameters': match} for match in constructor_matches]

        return constructor_details
    else:
        return []

def extract_class_attributes(java_code):
    # Define the regex pattern to match Java class attributes
    attribute_pattern = re.compile(r'(?:(?:public|private|protected|\s)+)?\s*([\w<>]+)\s+(\w+)\s*;')

    # Find all matches in the Java code
    attribute_matches = attribute_pattern.findall(java_code)

    # Extract attribute details from matches
    attribute_details = [{'type': match[0], 'name': match[1]} for match in attribute_matches]

    return attribute_details

def extract_variable_details(java_code):
    # Define the regex pattern to match Java variable declarations within methods
    variable_pattern = re.compile(r'\b([\w<>]+)\s+(\w+)\s*;')

    # Find all matches in the Java code
    variable_matches = variable_pattern.findall(java_code)

    # Extract variable details from matches
    variable_details = [{'type': match[0], 'name': match[1]} for match in variable_matches]

    return variable_details

def extract_attributes_in_method(java_code,line):
    lines = java_code.splitlines()[:line+1]
    lines = lines[::-1]

    selected_area = []
    for line in lines:
        method = extract_method_signatures(line)
        if(method):
            print("method:",method)
            break
        selected_area.append(line)

        # attributes =  extract_class_attributes(line)
        attributes = extract_variable_details(line)
        if(attributes):
            print("attributes:",attributes[0])
            break
    

    # print("selected area:",selected_area)

if __name__ == "__main__":
    file_path = "./PerturbedSamples/Csv-4/Calculator.java"
    with open(file_path, 'r') as f:
        java_code = f.read()

    # Extract method signatures and constructor details from the Java code
    class_name = extract_class_name(java_code)
    method_signatures = extract_method_signatures(java_code)
    constructor_details = extract_constructor_details(java_code,class_name)
    # Extract class attributes from the Java code
    # class_attributes = extract_class_attributes(java_code)
    extract_attributes_in_method(java_code, 15)


    # Prepare data for JSON
    data = {
        'class_name': class_name,
        'method_signatures': method_signatures,
        'constructor_details': constructor_details,
        # 'class_attributes': class_attributes
    }

    # Save data to JSON file
    with open('java_details.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

    print("Data saved to java_details.json.")