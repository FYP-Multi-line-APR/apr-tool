import sys 

from utils import get_json_data, write_json
from utils import bug_token, context_token
from utils import bug_field
from generate_single_file_multi_line_bugs import ctx_field, prediction_token, fix_field, txt_field
from generate_single_file_multi_line_bugs import get_fix_added_context


def get_new_context(bug_with_phrase, context):
    return f"{bug_token} {bug_with_phrase} {context_token} {context}"

def get_ctxs_entry(context_text):
    return {
        txt_field: context_text
    }

def handle_file_data(file_data):
    result = []
    for data_item in file_data:
        new_ctxs = []
        all_ctxs = data_item[ctx_field]
        bug_context_text = all_ctxs[0][txt_field]
        fix = data_item[fix_field]
        bug = data_item[bug_field]
        bug_applied_context = get_fix_added_context(bug_context_text, bug)
        new_context_text = get_new_context(bug_context_text, bug_applied_context)
        new_ctxs.append(get_ctxs_entry(new_context_text))
        for i in range(1, len(all_ctxs)):
            curr_context_text = all_ctxs[i][txt_field]
            new_context_text = get_new_context(bug_context_text, curr_context_text)
            new_ctxs.append(get_ctxs_entry(new_context_text))
        data_item[ctx_field] = new_ctxs
        result.append(data_item)
    write_json(result_file_path, result)

result_file_path = "./PerturbedSamples/PerturbedJsons/multi-line-set-4/arranged-multi-line-train-data-format-1.json"
text_result_file_path = "./PerturbedSamples/PerturbedJsons/multi-line-set-4/arranged-multi-line-train-data-format-1.txt"

if __name__ == "__main__":
    file_path = sys.argv[1]
    # file_path = "./PerturbedSamples/PerturbedJsons/multi-line-set-3/arranged-multi-line-train-data.json"
    data = get_json_data(file_path)
    handle_file_data(data)
    # print(data[0])
    print("finishing formatting multi line data")
