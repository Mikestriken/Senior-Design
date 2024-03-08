#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

repairScripts.sh

installAndRepairVEnv.sh

installAndRepairAPTInstalls.sh

installAndRepairServices.sh