import subprocess
import sys

CURRENT_PATH = "test-project"
LOG_FILE = "build_errors.log"


def maven_get_compilation_errors(test_project_path):
    maven_command = "mvn clean package"

    try:
        # Run the Maven command and capture the stdout and stderr
        result = subprocess.run(
            maven_command, 
            shell=True, 
            cwd=test_project_path,
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
        )

        if result.returncode == 0:
            print("Maven build successful.")
        else:
            print("Maven build failed with the following error details:")
            # Print the stderr (error details) captured during the build
            print(result.stderr)

            # Write the compilation errors to the log file
            with open(LOG_FILE, "w") as log_file:
                log_file.write(result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error: Maven build failed with return code {e.returncode}")
        print(e.stderr)



if __name__ == '__main__':
    # project="1"
    # bug="2"

    # test_project_path = f"{CURRENT_PATH}/{project}/{bug}"
    test_project_path = f"{CURRENT_PATH}"
    maven_get_compilation_errors(test_project_path)

    



    
    