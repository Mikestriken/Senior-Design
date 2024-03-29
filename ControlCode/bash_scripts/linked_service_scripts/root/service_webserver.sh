#!/bin/bash

# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# Change the directory to ControlCode
cd "../../../"

# Execute the flask webserver
../venv/bin/python -m flask_webserver.flask_webserver --no-camera