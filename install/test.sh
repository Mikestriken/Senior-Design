#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# List of modules to install
packages=("pyserial" "RPi.GPIO" "picamera"  "Flask" "greenlet" "paho-mqtt")
raspberryPackages=("pyserial" "RPi.GPIO" "picamera")

# Specify the directory for the virtual environment
venv_dir="../venv"

# Flag if venv folder detected
venvDetected=false
if [ -d "$venv_dir" ]; then
    venvDetected=true
fi

# * Check for "--windows" command line argument and update packages list to match OS.
echo -e "Updating packages list for specified OS...\n"
windows=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --windows)
            # Set the 'windows' variable to true
            windows=true

            # Loop through each element in 'packages'
            new_packages=()
            for package in "${packages[@]}"; do
                if [[ ! " ${raspberryPackages[@]} " =~ " ${package} " ]]; then
                    new_packages+=("$package")
                else
                    echo "Removed $package from packages"
                fi
            done

            # Update the 'packages' array
            packages=("${new_packages[@]}")

            ;;
        *)
            # Ignore other command line arguments
            ;;
    esac
    # Move to the next argument
    shift
done

echo "Updated 'packages' array: ${packages[@]}"