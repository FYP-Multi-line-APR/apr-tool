#!/bin/bash

# move to apr-tool directory 
cd apr-tool

# Clone the Defects4J repository
git clone https://github.com/rjust/defects4j.git

# Update the package list
sudo apt-get update

# Install cpanminus
sudo apt-get install -y cpanminus

# Install dependencies
cpanm --installdeps .

# Change directory to the Defects4J repository
cd defects4j

# installing defects4j
!./init.sh

# change directory to the root
cd ..


# setting up path variables
python setting_up_path_variables.py