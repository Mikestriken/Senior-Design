#!/bin/bash

##############################################################################
#                        Wall Power Service Script
# This script will be ran by the sd_wallpower.service.
# 
# This script runs the wall_power_main python script found in the
# /ControlCode/operations/ directory.
#
# Created by Michael Marais, Spring 2024
##############################################################################

# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# Change the directory to ControlCode
cd "../../../"

# Execute the flask webserver
../venv/bin/python -m operations.wall_power_main