import sys , random

from utils import ctx_field
from utils import get_json_data, write_json, make_dir

# file_paths = [
#     # "./PerturbedSamples/PerturbedJsons/set8-context-5-predict-token-for-fine-tune/train-data-multiple-contexts.json",
#     "./PerturbedSamples/PerturbedJsons/set9-context-5-predict-token-for-fine-tune-finmath/train-data-without-comments-multiple-contexts.json",
#     # "./PerturbedSamples/PerturbedJsons/set10-context-5-prediction-token-for-time4j/train-data-without-comments-multiple-contexts.json",
# ]

def shuffle_and_take(data, amount):
    random.shuffle(data)
    result = data[:amount]
    return result

def get_amount_to_take(amount_to_take_input, file_content_length):
    if amount_to_take_input == "all":
        return file_content_length
    return min(int(amount_to_take_input), file_content_length)

def filter_max_context_size(content):
    result = []
    for data_element in content:
        contexts = data_element[ctx_field]
        crop_context_size = max_context_size if len(contexts) > max_context_size else len(contexts)
        data_element[ctx_field] = data_element[ctx_field][:crop_context_size]
        result.append(result)
    return result

mulitple_context_identification = "multiple-contexts"
max_context_size = 2

if __name__ == "__main__":
    result_dir = sys.argv[1]
    amount_to_take_input = sys.argv[2]
    file_paths = sys.argv[3:]
    multi_line_set_dir = f"./PerturbedSamples/PerturbedJsons/{result_dir}/"
    make_dir(multi_line_set_dir)
    result_file_path = multi_line_set_dir + "collected-multiple-context-train-data.json"
    result = []
    for file_path in file_paths:
        if mulitple_context_identification in file_path:
            file_content = get_json_data(file_path)
            amount_to_take = get_amount_to_take(amount_to_take_input, len(file_content))
            shuffled_data = shuffle_and_take(file_content, amount_to_take)
            data_to_write = filter_max_context_size(shuffled_data)
            result.extend(data_to_write)
    write_json(result_file_path, result)