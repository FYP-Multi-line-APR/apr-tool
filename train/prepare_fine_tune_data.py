import sys, os, json
from utils import get_files_inside_dir, make_dir, get_list_of_dirs_in, get_json_data, write_json
from utils import get_unique_item_list, replace_placeholder
from utils import prediction_token

train_data = "train-data"
fine_tune_train_data = "fine-tune-train-data"

code_files_info_json_filepath = "/code-files-info.json"

json_ext = ".json"

bug_token = "[BUG]"
context_token = "[CONTEXT]"
method_token = "[METHOD]"

filepath_field = "filepath"
method_signatures_field = "methodSignatures"
main_method_field = "main"
method_name_field = "method_name"

prompt_version = 0

available_prompt_descriptions = [
    "[BUG]... [CONTEXT]... ",
    "[BUG]... [CONTEXT]... [METHODS]...",
    "[BUG]...<extra_id_0>... [CONTEXT]..."
]

code_files_info_data = {}

def get_method_names_str(filepath):
    code_file_info = code_files_info_data[filepath]
    method_signatures = code_file_info[method_signatures_field]
    method_names = [signature[method_name_field] for signature in method_signatures if signature[method_name_field] != main_method_field]
    unique_method_names = get_unique_item_list(method_names)
    return ' '.join(unique_method_names)

def get_format_text(bug, context_text, filepath):
    global prompt_version
    if prompt_version == 0:
        return f"{bug_token} {bug} {context_token} {context_text}"
    if prompt_version == 1:
        method_names_str = get_method_names_str(filepath)
        return f"{bug_token} {bug} {context_token} {context_text} {method_token} {method_names_str}"
    if prompt_version == 2:
        context_with_bug = replace_placeholder(context_text, prediction_token, bug)
        return f"{bug_token} {context_text} {context_token} {context_with_bug}"

def handle_bug_file(bug_file_path, result_file_path):
    bug_contents = get_json_data(bug_file_path)
    result = []
    for bug_content in bug_contents: 
        filepath = bug_content[filepath_field]
        bug = bug_content["bug"]
        context_text = bug_content["ctxs"][0]["txt"]
        format_text = get_format_text(bug, context_text, filepath)
        bug_content["ctxs"][0]["txt"] = format_text
        result.append(bug_content)
    write_json(result_file_path, result)

def view_available_prompts(): 
    for i in range(len(available_prompt_descriptions)):
        print(f"{i+1}. {available_prompt_descriptions[i]}")

def add_prompt_version_to_result_filename(filename, prompt_version):
    parts = filename.split('.')
    return parts[0] + f"-prompt-{prompt_version}" + '.' + parts[1]

if __name__ == "__main__":
    bug_file_path = sys.argv[1]
    prompt_version = int(sys.argv[2]) - 1
    # bug_file_path = "PerturbedSamples/PerturbedJsons/set12-context-5-predict-token-for-maven-doxia/train-data.json"

    root_dir_path = bug_file_path.rsplit('/', 1)[0]

    project = None 
    bug_file = None 

    # view_available_prompts()
    # prompt_version =  int(input("Enter prompt version: ")) - 1

    try: 
        project = sys.argv[2]
        bug_file = sys.argv[3]
        code_files_info_data = get_json_data(root_dir_path + code_files_info_json_filepath)
    except:
        pass
    
    result_file_path = bug_file_path.replace(train_data, fine_tune_train_data)

    result_file_path = bug_file_path.replace(train_data, fine_tune_train_data)
    result_file_path = add_prompt_version_to_result_filename(result_file_path, prompt_version+1)
    handle_bug_file(bug_file_path, result_file_path)
