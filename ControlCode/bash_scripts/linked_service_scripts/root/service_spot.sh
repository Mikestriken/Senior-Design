#!/bin/bash

##############################################################################
#                        Spoot Service Script
# This script will be ran by the sd_spot.service.
# 
# This script runs the spot_interaction python script found in the
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

# Execute the operation
../venv/bin/python -B -m operations.spot_interaction