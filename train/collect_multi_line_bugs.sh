#!/bin/bash
# python3 collect_multi_line_bugs.py \
#     multi-line-set-3 \
#     100 \
#     ./PerturbedSamples/PerturbedJsons/set9-context-5-predict-token-for-fine-tune-finmath/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set10-context-5-prediction-token-for-time4j/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set11-context-5-predict-token-for-html/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set12-context-5-predict-token-for-maven-doxia/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set14-context-5-for-wro4j/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set15-context-5-for-guava/train-data-without-comments-multiple-contexts.json \
#     ./PerturbedSamples/PerturbedJsons/set16-context-5-for-supercsv/train-data-without-comments-multiple-contexts.json 

python3 collect_multi_line_bugs.py \
    multi-line-set-3 \
    10000 \
    ./PerturbedSamples/PerturbedJsons/set9-context-5-predict-token-for-fine-tune-finmath/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set10-context-5-prediction-token-for-time4j/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set11-context-5-predict-token-for-html/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set12-context-5-predict-token-for-maven-doxia/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set14-context-5-for-wro4j/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set15-context-5-for-guava/train-data-without-comments-multiple-contexts.json \
    ./PerturbedSamples/PerturbedJsons/set16-context-5-for-supercsv/train-data-without-comments-multiple-contexts.json 


