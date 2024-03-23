repo_name="$1"
temp_dir_name="$2"

cloned_repo_dir_path="cloned-repos/${repo_name}"
perturbed_repo_dir_path="perturbed_repos/${repo_name}"
before_perturb_dir_path="PerturbedSamples/${temp_dir_name}"
after_perturb_dir_path="PerturbedSamples/Perturbation-${temp_dir_name}"
result_dir_name="PerturbedSamples/all-file-input-${repo_name}"

generated_file_1_path="PerturbedSamples/PerturbedJsons/code-files-info-${temp_dir_name}.json"
generated_file_2_path="PerturbedSamples/PerturbedJsons/train-data-${temp_dir_name}.json"
generated_file_3_path="PerturbedSamples/PerturbedJsons/train-data-${temp_dir_name}.txt"

final_result_file_1_path="$result_dir_name/code-files-info.json"
final_result_file_2_path="$result_dir_name/train-data.json"
final_result_file_3_path="$result_dir_name/train-data.txt"

mkdir "$before_perturb_dir_path"
mkdir "$after_perturb_dir_path"

cp -r ./$cloned_repo_dir_path/* $before_perturb_dir_path

# python3 "1_perturb_projects.py" "$temp_dir_name"

cp -r ./$perturbed_repo_dir_path/* $after_perturb_dir_path

python3 "b_execute_perturbation.py" "$temp_dir_name"

mkdir "$result_dir_name"
mkdir "$perturbed_repo_dir_path"

mv "$after_perturb_dir_path/*" "$perturbed_repo_dir_path"

mv "$generated_file_1_path" "$final_result_file_1_path"
mv "$generated_file_2_path" "$final_result_file_2_path"
mv "$generated_file_3_path" "$final_result_file_3_path"
