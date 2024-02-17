import copy 
import json 
import sys 
from utils import get_json_data, replace_placeholder, write_json

id_field = "id"
filepath_field = "filepath"
start_bug_line_field = "start-bug-line"
prediction_token = "<extra_id_0>"
fix_field = "fix"
ctx_field = "ctxs"
txt_field = "txt"

json_ext = ".json"

def get_dict_from_bug_id(bug_train_data):
    result = {}
    for content in bug_train_data:
        result[content["id"]] = content 
    return result

def get_dict_of_bug_file_and_ids(bug_train_data):
    result = {}
    for content in bug_train_data:
        if result.get(content[filepath_field]):
            result[content[filepath_field]].append(content[id_field])
        else:
            result[content[filepath_field]] = [content[id_field]]
    return result 

def get_fix_added_context(context, fix):
    global prediction_token
    return replace_placeholder(context, prediction_token, fix)

def get_ctx_dict(ctx_text):
    return { txt_field: ctx_text }

def generate_multi_line_bugs(bug_file_and_ids_dict, bug_train_data_dict):
    result = []
    for bug_file in bug_file_and_ids_dict.keys():
        bug_file_ids = bug_file_and_ids_dict[bug_file]
        lines_considered = set()
        multi_line_bugs = []
        for bug_id in bug_file_ids:
            curr_bug = bug_train_data_dict[bug_id]
            if curr_bug[start_bug_line_field] not in lines_considered:
                lines_considered.add(curr_bug[start_bug_line_field])
                multi_line_bugs.append(curr_bug)
        for i in range(len(multi_line_bugs)):
            new_bug = copy.copy(multi_line_bugs[i])
            for j in range(len(multi_line_bugs)):
                if i!=j:
                    curr_bug_content = multi_line_bugs[j]
                    curr_ctx = curr_bug_content[ctx_field][0][txt_field]
                    curr_fix = curr_bug_content[fix_field]
                    fixed_context = get_fix_added_context(curr_ctx, curr_fix)
                    fixed_context_dict = get_ctx_dict(fixed_context)
                    new_bug[ctx_field].append(fixed_context_dict)
            result.append(new_bug)
    return result

def get_result_file_path(input_file_path):
    file_name = input_file_path.split('.')[0]
    file_name = file_name + "-multiple-contexts"
    return file_name + json_ext

if __name__ == "__main__":
    # curr_train_data_file_path = "./PerturbedSamples/PerturbedJsons/set8-context-5-predict-token-for-fine-tune/train-data.json"
    curr_train_data_file_path = sys.argv[1]
    result_file_path = get_result_file_path(curr_train_data_file_path)
    single_line_bug_train_data = get_json_data(curr_train_data_file_path)

    bug_train_data_dict = get_dict_from_bug_id(single_line_bug_train_data)
    bug_file_and_ids_dict = get_dict_of_bug_file_and_ids(single_line_bug_train_data)

    result = generate_multi_line_bugs(bug_file_and_ids_dict, bug_train_data_dict)
    write_json(result_file_path, result)
    print(f"finish generating {len(result)} multi line bugs")
