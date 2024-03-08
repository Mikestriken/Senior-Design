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

if ! ./repairScripts.sh; then
    echo -e "Error: $(basename ./repairScripts.sh) failed!"
    exit 1
fi

if ! ./installAndRepairAPTInstalls.sh; then
    echo -e "Error: $(basename ./installAndRepairAPTInstalls.sh) failed!"
    exit 1
fi

if ! ./installAndRepairVEnv.sh; then
    echo -e "Error: $(basename ./installAndRepairVEnv.sh) failed!"
    exit 1
fi

if [ windows != true ]; then # Only install services on linux environment

    if ! ./installAndRepairServices.sh; then
        echo -e "Error: $(basename ./installAndRepairServices.sh) failed!"
        exit 1
    fi

fi