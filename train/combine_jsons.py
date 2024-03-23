import sys
from utils import get_json_data, write_json

def combine_json_lists(file_paths, output_path):
    result = []
    for file_path in file_paths:
        data = get_json_data(file_path)
        result = result + data 
    print(output_path)
    write_json(output_path, result)

# Example usage
if __name__ == "__main__":
    output_path = sys.argv[1]
    file_paths = sys.argv[2:]
    combine_json_lists(file_paths, output_path)
