# Steps to follow
1. Move inside the `train` directory
2. The move inside the `perturbation_model` directory
3. Then execute `mvn package assembly:single` to build the target
4. Execute following scripts one after another.
    - `1_perturb_projects.py`
    - `2_execute_perturbation.py`
    - `3_generate_buggy_project.py`
    - `4_generate_train_data.py`