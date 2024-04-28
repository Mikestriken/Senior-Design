#!/bin/bash

##############################################################################
#                        Flask Webserver Service Script
# This script will be ran by the sd_webserver.service.
# 
# This script runs the flask_webserver python script found in the
# /ControlCode/flask_webserver/ directory.
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
../venv/bin/python -m flask_webserver.flask_webserver