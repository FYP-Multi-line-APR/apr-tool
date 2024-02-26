#!/bin/bash
context_size=4

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set8-context-5-for-rhino/train-data-without-comments.json "$context_size" 

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set9-context-5-predict-token-for-fine-tune-finmath/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set10-context-5-prediction-token-for-time4j/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set11-context-5-predict-token-for-html/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set12-context-5-predict-token-for-maven-doxia/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set14-context-5-for-wro4j/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set15-context-5-for-guava/train-data-without-comments.json "$context_size"

python3 generate_single_file_multi_line_bugs.py \
    PerturbedSamples/PerturbedJsons/set16-context-5-for-supercsv/train-data-without-comments.json "$context_size"
