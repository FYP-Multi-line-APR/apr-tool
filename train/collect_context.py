import os, re 

context_jar_path = "./../utils/context.jar "
prediction_token = "<extra_id_0>"
bug_token = "[BUG]"
context_token = "[CONTEXT]"
context_width = 10

def divide_front_line_range_into_parts(lower_bound, upper_bound, width):
    parts = []
    end = upper_bound
    while end > lower_bound:
        start = max(end - width + 1, lower_bound)
        parts.append((start, end))
        end -= width
    parts.reverse() 
    return parts

def divide_back_line_range_into_parts(lower_bound, upper_bound, width):
    parts = []
    start = lower_bound
    while start < upper_bound:
        end = min(start + width - 1, upper_bound)
        parts.append((start, end))
        start += width
    return parts

def extract_lines(lines, line_ranges):
    extracted_lists = []
    for start, end in line_ranges:
        extracted_lists.append(lines[start-1:end])  # Adjust indices to 0-based indexing
    return extracted_lists

def filter_full_file_context(file_lines):
    global context_width
    file_start = 1
    file_end = len(file_lines) - 1
    predicting_line_index = -1 
    for i in range(len(file_lines)):
        line = file_lines[i]
        if prediction_token in line:
            predicting_line_index = i 
            break 
    estimate_start = predicting_line_index - context_width
    estimate_end = predicting_line_index + context_width
    start_index = max(0, estimate_start) 
    end_index = min(len(file_lines) - 1, estimate_end)

    # from 0 to start index divide into 2xcontext width 
    front_line_ranges = divide_front_line_range_into_parts(file_start, start_index - 1, context_width * 2)
    back_line_ranges = divide_back_line_range_into_parts(end_index, file_end, context_width * 2)
    # from end index to file end divide into 2xcontext width 
    extracted_front_lines_set = extract_lines(file_lines, front_line_ranges)
    extracted_back_lines_set = extract_lines(file_lines, back_line_ranges)
    buggy_lines_set = [file_lines[start_index:end_index + 1]]
    return extracted_front_lines_set + buggy_lines_set + extracted_back_lines_set

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
    return result

def get_function_line_range(bug_file_path, bug_line):
    results = os.popen("java -jar "+context_jar_path +bug_file_path +" test-"+str(bug_line)).read()
    stratline_no = extract_startline_no(results)
    endline_no = extract_endline_no(results)
    return stratline_no, endline_no 

def get_function_content_with_prediction_token(file_path, stratline_no, endline_no, start_bug_line, end_bug_line):
    print(f"start_bug_line:{start_bug_line}, end_bug_line:{end_bug_line}")
    extracted_lines = []
    buggy_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        stratline_no = max(1, min(stratline_no, len(all_lines)))
        endline_no = max(1, min(endline_no, len(all_lines)))
        for i in range(stratline_no - 1, endline_no):
            if i == (start_bug_line - 1):
                extracted_lines.append(prediction_token)
                buggy_lines.append(all_lines[i])
            elif i < start_bug_line:
                extracted_lines.append(all_lines[i])
            elif start_bug_line - 1 < i and i < end_bug_line:
                buggy_lines.append(all_lines[i])
                continue
            else:
                extracted_lines.append(all_lines[i])
    return extracted_lines, buggy_lines

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

def get_file_lines_with_prediction_token(file_path, start_bug_line, end_bug_line):
    file_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        for i in range(0, len(all_lines)):
            if i == (start_bug_line - 1):
                file_lines.append(prediction_token)
            elif i < start_bug_line:
                all_lines[i] = all_lines[i].replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
                file_lines.append(all_lines[i])
            elif start_bug_line - 1 < i and i < end_bug_line:
                continue
            else:
                all_lines[i] = all_lines[i].replace('\t',' ').replace('\n',' ').replace('\r',' ').replace('  ',' ')
                file_lines.append(all_lines[i])
    return file_lines

def filter_context(func_lines):
    global context_width
    predicting_line_index = -1 
    for i in range(len(func_lines)):
        line = func_lines[i]
        if prediction_token in line:
            predicting_line_index = i 
            break 
    estimate_start = predicting_line_index - 1 - context_width
    estimate_end = predicting_line_index + 1 + context_width
    start_index = max(0, estimate_start) 
    end_index = min(len(func_lines) - 1, estimate_end)
    return func_lines[start_index:end_index + 1]

def get_context_with_prediction_token_without_comments(file_path, start_bug_line, end_bug_line):
    file_lines = get_file_lines_with_prediction_token(file_path, start_bug_line, end_bug_line)
    file_lines_without_comment = remove_comment_lines(file_lines)
    filtered_content = filter_context(file_lines_without_comment)
    return get_content_lines_as_string(filtered_content)

def get_full_file_context_with_prediction_token_without_comments(file_path, start_bug_line, end_bug_line):
    file_lines = get_file_lines_with_prediction_token(file_path, start_bug_line, end_bug_line)
    file_lines_without_comment = remove_comment_lines(file_lines)
    filtered_content = filter_full_file_context(file_lines_without_comment)
    return [get_content_lines_as_string(each_element) for each_element in filtered_content]
    # split_list = [get_content_lines_as_string(file_lines_without_comment[i:i+context_width]) for i in range(0, len(file_lines_without_comment), context_width)]
    # return split_list

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

def collect_buggy_lines(func_lines, func_start, func_end, bug_start, bug_end):
    result = []
    for i in range(len(func_lines)):
        line = func_lines[i]
        curr_line = func_start + i 
        if bug_start <= curr_line and curr_line <= bug_end:
            result.append(line)
    return process_lines(result)

def collect_context(file_path, start_bug_line, end_bug_line, corrupt_code):
    func_start, func_end = get_function_line_range(file_path, start_bug_line)
    # func_lines = get_function_content(file_path, func_start, func_end)
    func_lines, buggy_lines = get_function_content_with_prediction_token(file_path, func_start, func_end, start_bug_line, end_bug_line)
    # func_lines = add_bug_token_for_func(func_lines, func_start, start_bug_line, end_bug_line)
    func_lines = remove_comment_lines(func_lines)
    # print(f"buggy_lines:{buggy_lines}")
    buggy_lines_str = process_lines(buggy_lines)
    # limit context 
    truncated_lines = func_lines
    truncated_lines_str = process_lines(truncated_lines)
    return  f"{bug_token} {corrupt_code} {context_token} {truncated_lines_str}"

def process_lines(lines):
    result = []
    for line in lines:
        processed_line = process_line(line)
        if processed_line != '':
            result.append(processed_line)
    # print(f"process lines : {result}")
    return ' '.join(result)

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
    print(context)
