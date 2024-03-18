#!/bin/bash

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