#!/bin/bash

# Define the directory where you want to run Maven compilation
project_directory="test-project"

# Define the name of the log file to capture compilation failures
log_file="compilation_failures.log"

# Change to the project directory
cd "$project_directory"

# Run Maven clean and package and redirect the output to a temporary file
mvn clean package > temp_log.txt 2>&1

# Check if the compilation was successful
if [ $? -eq 0 ]; then
  echo "Maven clean package succeeded."
else
  echo "Maven clean package failed. See $log_file for details."
  # Copy the compilation failure details to the log file
  cat temp_log.txt >> "$log_file"
fi

# Clean up the temporary log file
rm temp_log.txt
