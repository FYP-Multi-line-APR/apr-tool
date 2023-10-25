#!/bin/bash

# move to apr-tool directory 

echo "=====================================Packages installation======================================"
# Update the package list
sudo apt-get update

echo "=====================================Cpan installation======================================"
# Install cpanminus
sudo apt-get install -y cpanminus

# Install dependencies
cpanm --installdeps .

echo "=====================================DBI installation======================================"
# install cpan modules
cpan install DBI -y

sudo apt-get update
sudo apt-get install subversion -y

echo "svn version: $(svn --version)"

echo "=====================================JAVA installation======================================"
# install java 
sudo apt-get update -y
sudo apt-get install openjdk-8-jdk -y

# Configure Java 1.8 as the default
sudo update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java


# defects4j installation
echo "=====================================Defects4J installation======================================"
cd /content/apr-tool

echo "Current path: $(pwd)"

# Clone the Defects4J repository
git clone https://github.com/rjust/defects4j.git

# Change directory to the Defects4J repository
cd /content/apr-tool/defects4j
echo "Current path: $(pwd)"


# installing defects4j
./init.sh

# change directory to the root
cd /content/apr-tool
echo "Current path: $(pwd)"

# setting up path variables
python setting_up_path_variables.py



