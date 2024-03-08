#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# * Define variables that will be used
# Source directories
user_dir="../../service_files/user"
root_dir="../../service_files/root"

# Destination directories
user_destination_dir="$HOME/.config/systemd/user/"
root_destination_dir="/etc/systemd/system/"

# Arrays to store file names
user_services=()
user_services+=("$user_dir"/*) # add the names of all the files in $user_dir/ to the user_services array

root_services=()
root_services+=("$root_dir"/*) # add the names of all the files in $root_dir/ to the user_services array

# * Enable the services
# Enable the user services
echo -e "\nEnabling User Services..."
for service_file in "${user_services[@]}"; do
    if ! systemctl --user enable "$(basename "$service_file" .service)"; then
        echo "Error: Enabling $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo "done!"

# Enable the root services
echo -e "\nEnabling Root Services..."
for service_file in "${root_services[@]}"; do
    if ! sudo systemctl enable "$(basename "$service_file" .service)"; then
        echo "Error: Enabling $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo -e "done!\n"