#!/bin/

##############################################################################
#                                Run Flask Webserver
# This script manually runs the flask_webserver python script found in the
# /ControlCode/flask_webserver/ directory.
# 
# The purpose of this script is mainly to serve as a utility to reduce the
# length of the command line argument necissary to start the python script.
# 
# The user can specifiy additional command line arguments to be directly
# passed to the python script being ran.
# EG: appending the --no-camera command line argument to this script,
# will disable all the code for the flask webserver associated with the camera.
#
# Created by Michael Marais, Spring 2024
##############################################################################

# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# Change the current directory to ControlCode
cd ".."

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

# Execute the flask webserver
if [ "$windows" == true ]; then
    ../venv/Scripts/python.exe -m flask_webserver.flask_webserver $@
else
    sudo ../venv/bin/python -m flask_webserver.flask_webserver $@
fi