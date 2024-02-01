import sys
from datasets import Dataset, DatasetDict, concatenate_datasets
from utils import get_json_data
from datasets import load_dataset

dataset_names = [
    "chathuranga-jayanath/context-5-predict-token-for-fine-tune-without-comments-from-times4j", 
    "chathuranga-jayanath/context-5-predict-token-for-fine-tune-without-comments-from-finmath"
]

portion = 0.5

loaded_datasets = []

train_text = "train"
test_text = "test"
validation_text = "validation"

def load_datasets():
    global dataset_names, load_datasets
    load_datasets = []
    for dataset_name in dataset_names:
        dataset = load_dataset(dataset_name)
        loaded_datasets.append(dataset)

def generate_new_train_dataset():
    result = []
    for dataset in loaded_datasets:
        result.append(dataset[train_text])
    return concatenate_datasets(result)

def generate_new_test_dataset():
    result = []
    for dataset in loaded_datasets:
        result.append(dataset[test_text])
    return concatenate_datasets(result)

def generate_new_validation_dataset():
    result = []
    for dataset in loaded_datasets:
        result.append(dataset[validation_text])
    return concatenate_datasets(result)


if __name__ == "__main__":
    load_datasets()
    dataset_name = "context-5-for-finetune-finmath-times4j"
    
    new_train_dataset = generate_new_train_dataset()
    new_validation_dataset = generate_new_validation_dataset()
    new_test_dataset = generate_new_test_dataset()

    new_dataset_dict = DatasetDict({
        'train': new_train_dataset,
        'validation': new_validation_dataset,
        'test': new_test_dataset,
    })
    new_dataset_dict.push_to_hub(f"chathuranga-jayanath/{dataset_name}")
    print("finish concatenating publish")
