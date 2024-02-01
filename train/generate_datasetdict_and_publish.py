import random
import sys
from datasets import Dataset, DatasetDict
from utils import get_json_data

seed_value = 42 
random.seed(seed_value)

dataset_names = [
    "context-5-predict-token-for-fine-tune-without-comments-from-maven-doxia",
    "context-5-predict-token-for-fine-tune-without-comments-from-finmath",
    "context-5-predict-token-for-fine-tune-without-comments-from-times4j"
]

def create_dataset_dict(data_array, consider_portion, validation_split=0.1, test_split=0.1):
    random.shuffle(data_array)
    # len_considered = int(len(data_array) * consider_portion)
    # data_array = data_array[:len_considered]
    total_samples = len(data_array)
    validation_samples = int(validation_split * total_samples)
    test_samples = int(test_split * total_samples)

    train_data = data_array[:-validation_samples - test_samples]
    validation_data = data_array[-validation_samples - test_samples:-test_samples]
    test_data = data_array[-test_samples:]

    train_ids = [item['id'] for item in train_data]
    train_filepaths = [item['filepath'] for item in train_data]
    train_start_bug_lines = [item['start-bug-line'] for item in train_data]
    train_end_bug_lines = [item['end-bug-line'] for item in train_data]
    train_bugs = [item['bug'] for item in train_data]
    train_fixes = [item['fix'] for item in train_data]
    train_ctxs = [item['ctxs'][0]['txt'] for item in train_data]

    validation_ids = [item['id'] for item in validation_data]
    validation_filepaths = [item['filepath'] for item in validation_data]
    validation_start_bug_lines = [item['start-bug-line'] for item in validation_data]
    validation_end_bug_lines = [item['end-bug-line'] for item in validation_data]
    validation_bugs = [item['bug'] for item in validation_data]
    validation_fixes = [item['fix'] for item in validation_data]
    validation_ctxs = [item['ctxs'][0]['txt'] for item in validation_data]

    test_ids = [item['id'] for item in test_data]
    test_filepaths = [item['filepath'] for item in test_data]
    test_start_bug_lines = [item['start-bug-line'] for item in test_data]
    test_end_bug_lines = [item['end-bug-line'] for item in test_data]
    test_bugs = [item['bug'] for item in test_data]
    test_fixes = [item['fix'] for item in test_data]
    test_ctxs = [item['ctxs'][0]['txt'] for item in test_data]

    train_dict = {
        'id': train_ids,
        'filepath': train_filepaths,
        'start_bug_line': train_start_bug_lines,
        'end_bug_line': train_end_bug_lines,
        'bug': train_bugs,
        'fix': train_fixes,
        'ctx': train_ctxs,
    }

    validation_dict = {
        'id': validation_ids,
        'filepath': validation_filepaths,
        'start_bug_line': validation_start_bug_lines,
        'end_bug_line': validation_end_bug_lines,
        'bug': validation_bugs,
        'fix': validation_fixes,
        'ctx': validation_ctxs,
    }

    test_dict = {
        'id': test_ids,
        'filepath': test_filepaths,
        'start_bug_line': test_start_bug_lines,
        'end_bug_line': test_end_bug_lines,
        'bug': test_bugs,
        'fix': test_fixes,
        'ctx': test_ctxs,
    }

    train_dataset = Dataset.from_dict(train_dict)
    validation_dataset = Dataset.from_dict(validation_dict)
    test_dataset = Dataset.from_dict(test_dict)

    dataset_dict = DatasetDict({
        'train': train_dataset,
        'validation': validation_dataset,
        'test': test_dataset,
    })

    return dataset_dict

def display_available_dataset_names():
    print("Available dataset names")
    for i in range(len(dataset_names)):
        print(f"{i+1}. {dataset_names[i]}")

def get_combined_loaded_data(data_file_paths, consider_portion):
    result = []
    for data_file_path in data_file_paths:
        loaded_data = get_json_data(data_file_path)
        len_considered = int(len(loaded_data) * consider_portion)
        portioned_data = loaded_data[:len_considered]
        result.extend(portioned_data)
    return result

if __name__ == "__main__":
    publish_dataset_name = sys.argv[1]
    consider_portion = float(sys.argv[2])
    prompt_version = int(sys.argv[3])
    data_file_paths = sys.argv[4:]
    loaded_data = get_combined_loaded_data(data_file_paths, consider_portion)
    result_dataset = create_dataset_dict(loaded_data, consider_portion)
    published_name = f"chathuranga-jayanath/{publish_dataset_name}-portion-{consider_portion}-prompt-{prompt_version}"
    result_dataset.push_to_hub(published_name)
    print(f"Published dataset to: {published_name}")

# if __name__ == "__main__":
#     data_file_path = sys.argv[1]
#     consider_portion = float(sys.argv[2])
#     prompt_version = int(sys.argv[3])
#     display_available_dataset_names()
#     dataset_name_idx = int(input("Select datasetname: ")) - 1
#     dataset_name = dataset_names[dataset_name_idx]
#     print(dataset_name)
#     loaded_data = get_json_data(data_file_path)
#     result_dataset = create_dataset_dict(loaded_data, consider_portion)
#     result_dataset.push_to_hub(f"chathuranga-jayanath/{dataset_name}-portion-{consider_portion}-prompt-{prompt_version}")
#     print(result_dataset)

