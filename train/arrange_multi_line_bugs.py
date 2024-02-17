import os 
import sys
import copy 
from utils import get_json_data, write_json
from utils import id_field, filepath_field, fix_field, ctx_field

max_multi_line_bugs_per_file = 5

def arranged_multi_line_data(collected_data):
    result = []
    processed_files = set()
    curr_file_name = None 
    curr_file_bugs = 0
    for bug in collected_data:
        curr_file_name = bug[filepath_field]
        if curr_file_name not in processed_files:
            curr_file_bugs = 1
            contexts = bug[ctx_field]
            crop_context_len = min(len(contexts), max_multi_line_bugs_per_file)
            for cur_context_len in range(2, crop_context_len):
                new_bug = copy.copy(bug)
                # new_bug[ctx_field] = contexts[:curr_file_bugs + 1]
                new_bug[ctx_field] = contexts[:cur_context_len]
                result.append(new_bug)
            processed_files.add(curr_file_name)
        elif curr_file_bugs < max_multi_line_bugs_per_file:
            new_bug = copy.copy(bug)
            curr_file_bugs += 1
            contexts = bug[ctx_field]
            crop_context_len = min(len(contexts), max_multi_line_bugs_per_file)
            for cur_context_len in range(2, crop_context_len):
                new_bug = copy.copy(bug)
                # new_bug[ctx_field] = contexts[:curr_file_bugs + 1]
                new_bug[ctx_field] = contexts[:cur_context_len]
                result.append(new_bug)
        else:
            curr_file_bugs = 0
    return result

if __name__=="__main__":
    # collected_multi_line_train_data_path = "./PerturbedSamples/PerturbedJsons/multi-line-set-1/collected-multi-line-train-data.json"
    collected_multi_line_train_data_path = sys.argv[1]
    result_dir_path = '/'.join(collected_multi_line_train_data_path.split('/')[:-1])
    arranged_train_data_path = result_dir_path + "/arranged-multi-line-train-data.json"
    collected_multi_line_data = get_json_data(collected_multi_line_train_data_path)
    arranged_data = arranged_multi_line_data(collected_multi_line_data)
    write_json(arranged_train_data_path, arranged_data)