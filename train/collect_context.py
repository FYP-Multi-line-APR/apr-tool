import os, re 

context_jar_path = "./../utils/context.jar "
prediction_token = "<extra_id_0>"
bug_token = "[BUGGY]"
context_token = "[CONTEXT]"

def extract_startline_no(text):
    match = re.search(r'startline:(\d+)', text)
    if match:
        return int(match.group(1))
    else:
        return None

def extract_endline_no(text):
    match = re.search(r'endline:(\d+)', text)
    if match:
        return int(match.group(1))
    else:
        return None

def extract_for_fine_tune(text):
    match = re.search(r'\[CLASS\].*?(?=\bstartline:)', text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None

def execute_find_context(file_path, bug_line_no):
    result = os.popen("java -jar "+context_jar_path +file_path +" test-"+str(bug_line_no)).read()
    # print(f"execute_find_context:{result}")
    return result

def get_function_line_range(bug_file_path, bug_line):
    results = os.popen("java -jar "+context_jar_path +bug_file_path +" test-"+str(bug_line)).read()
    stratline_no = extract_startline_no(results)
    endline_no = extract_endline_no(results)
    return stratline_no, endline_no 

def get_function_content_with_prediction_token(file_path, stratline_no, endline_no, start_bug_line, end_bug_line):
    print(f"start_bug_line:{start_bug_line}, end_bug_line:{end_bug_line}")
    extracted_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        stratline_no = max(1, min(stratline_no, len(all_lines)))
        endline_no = max(1, min(endline_no, len(all_lines)))
        for i in range(stratline_no - 1, endline_no):
            
            if i == (start_bug_line - 1):
                
                extracted_lines.append(prediction_token)
            elif i < start_bug_line:
                extracted_lines.append(all_lines[i])
            elif start_bug_line - 1 < i and i < end_bug_line:
                continue
            else:
                extracted_lines.append(all_lines[i])
    return extracted_lines

def get_function_content(file_path, stratline_no, endline_no):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            all_lines = file.readlines()
            stratline_no = max(1, min(stratline_no, len(all_lines)))
            endline_no = max(1, min(endline_no, len(all_lines)))
            extracted_lines = all_lines[stratline_no - 1:endline_no]
            return extracted_lines
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_function_content_without_comments(file_path, stratline_no, endline_no):
    content_with_comments = get_function_content(file_path, stratline_no, endline_no)
    content_without_comments = remove_comment_lines(content_with_comments)
    return get_content_lines_as_string(content_without_comments)

def remove_comment_lines(content_lines):
    content_without_comments = []
    for line in content_lines:
        processed_line = process_line(line) 
        if processed_line != "":
            content_without_comments.append(processed_line)
        # else:
        #     print(f"comment line: {line}")
    return content_without_comments

def get_content_lines_as_string(content_lines):
    return ' '.join(content_lines)

def get_function_content_with_prediction_token_without_comments(file_path, start_bug_line, end_bug_line):
    print(f"filepath:{file_path}")
    context_result = execute_find_context(file_path, start_bug_line)
    startline_no = extract_startline_no(context_result)
    endline_no = extract_endline_no(context_result)
    function_content_lines = get_function_content_with_prediction_token(file_path, startline_no, endline_no, start_bug_line, end_bug_line)
    print(f"function_content_lines: {function_content_lines}")
    content_without_comments = remove_comment_lines(function_content_lines)
    return get_content_lines_as_string(content_without_comments)

def add_bug_token_for_func(lines, func_start, bug_start, bug_end):
    result = []
    for i in range(len(lines)):
        line = lines[i]
        curr_line = func_start + i
        if bug_start <= curr_line and curr_line <= bug_end:
            result.append(f"{bug_token} {line}")
        else:
            result.append(line)        
    return result

def collect_context(file_path, start_bug_line, end_bug_line):
    func_start, func_end = get_function_line_range(file_path, start_bug_line)
    
    func_lines = get_function_content(file_path, func_start, func_end)
    func_lines = add_bug_token_for_func(func_lines, func_start, start_bug_line, end_bug_line)
    func_lines = remove_comment_lines(func_lines)
    context_info = get_content_lines_as_string(func_lines)
    
    class_info = execute_find_context(file_path, start_bug_line)
    class_info = extract_for_fine_tune(class_info)
    return  f"{context_token} {context_info} {class_info}"

def process_lines(lines):
    result = []
    for line in lines:
        if process_line(line) != '':
            result.append(line)
    return result

def process_line(line):
    line = line.strip()
    line = line.replace('\n', '')
    line = re.sub(r'\s+', ' ', line)
    if line.startswith('//') or line.startswith('/*') or line.startswith('*') or line.startswith('*/'):
        return ''
    return line 

if __name__ == "__main__":
    bug_file_path = "./../train/PerturbedSamples/Csv-1/src/main/java/org/apache/maven/doxia/DefaultConverter.java"
    bug_line = 188

    context = collect_context(bug_file_path, 188, 189)
    # result = execute_find_context(bug_file_path, bug_line)
    # finetune_result = extract_for_fine_tune(result)
    print(context)
    