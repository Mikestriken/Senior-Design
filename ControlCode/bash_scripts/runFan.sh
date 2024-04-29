#!/bin/bash

##############################################################################
#                             Run Fan Control Code
# This script manually runs the fan_operation python script found in the
# /ControlCode/operations/ directory.
# 
# The purpose of this script is mainly to serve as a utility to reduce the
# length of the command line argument necissary to start the python script.
# 
# The user can specifiy additional command line arguments to be directly
# passed to the python script being ran.
# EG: appending the --no-camera command line argument for the runFlask script,
# will disable all the code for the flask webserver associated with the camera.
#
# Created by Michael Marais, Spring 2024
##############################################################################

# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# Change directory to ControlCode
cd "../"

# Execute the flask webserver
sudo ../venv/bin/python -m operations.fan_operation $@