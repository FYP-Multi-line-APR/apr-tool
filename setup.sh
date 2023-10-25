#!/bin/bash

# move to apr-tool directory 
cd content/apr-tool

# Clone the Defects4J repository
git clone https://github.com/rjust/defects4j.git

# Update the package list
sudo apt-get update

# Install cpanminus
sudo apt-get install -y cpanminus

# Install dependencies
cpanm --installdeps .

# Change directory to the Defects4J repository
cd content/defects4j

# installing defects4j
!./init.sh

# change directory to the root
cd content/apr-tool


# setting up path variables
python setting_up_path_variables.py