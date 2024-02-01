#!/bin/bash
# python3 generate_datasetdict_and_publish.py \
#     context-5-from-finmath-time4j-html-mavendoxia \
#     0.4 \
#     1 \
#     PerturbedSamples/PerturbedJsons/set9-context-5-predict-token-for-fine-tune-finmath/fine-tune-train-data-without-comments-prompt-1.json \
#     PerturbedSamples/PerturbedJsons/set10-context-5-prediction-token-for-time4j/fine-tune-train-data-without-comments-prompt-1.json \
#     PerturbedSamples/PerturbedJsons/set11-context-5-predict-token-for-html/fine-tune-train-data-without-comments-prompt-1.json \
#     PerturbedSamples/PerturbedJsons/set12-context-5-predict-token-for-fine-tune-maven-doxia/fine-tune-train-data-without-comments-prompt-1.json \

python3 generate_datasetdict_and_publish.py \
    formatted-selfapr-train-data \
    1 \
    3 \
    PerturbedSamples/PerturbedJsons/set13-from-selfapr/fine-tune-train-data.json

        