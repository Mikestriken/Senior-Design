#!/bin/bash
##############################################################################
#                                 Install
# This script runs all the install scripts in order:
# 1. repairScripts.sh
# 2. installAndRepairAPTInstalls.sh
# 3. installAndRepairVEnv.sh
# 4. installAndRepairServices.sh
#
# Created by Michael Marais, Spring 2024
##############################################################################

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
    echo "Non linux OS detected, windows flag set to $windows"
else
    # Otherwise, set windows=false or leave it unset (your choice)
    windows=false
    echo "Linux OS Detected, windows flag unset to $windows"
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

if [ "$windows" != true ]; then # Only install services on linux environment

    if ! ./installAndRepairServices.sh; then
        echo -e "Error: $(basename ./installAndRepairServices.sh) failed!"
        exit 1
    fi

fi