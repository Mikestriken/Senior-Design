#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# * Check current OS
windows=false
OS=$(uname)
# Check if the output of uname is not "Linux"
if [ "$OS" != "Linux" ]; then
    # If it's not Linux, set windows=true
    windows=true
else
    # Otherwise, set windows=false or leave it unset (your choice)
    windows=false
fi

# * Run all the installation scripts

./repairScripts.sh

./installAndRepairAPTInstalls.sh

./installAndRepairVEnv.sh

if [ windows != true ]; then # Only install services on linux environment

    ./installAndRepairServices.sh

fi