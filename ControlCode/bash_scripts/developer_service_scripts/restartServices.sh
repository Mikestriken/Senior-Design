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

# Compiled Source Directories
user_compiled_dir="$user_dir/compiled"
root_compiled_dir="$root_dir/compiled"

# Destination directories
user_destination_dir="$HOME/.config/systemd/user/"
root_destination_dir="/etc/systemd/system/"

# Service file compilation variable values
gitRepoDir="$(readlink -f "$script_dir/..")"

# * Create the "compiled" subdirectory if they it don't exist
if [ ! -d "$user_compiled_dir" ]; then
    echo -e "Error: $user_compiled_dir does not exist!\nMaybe run install/install.sh first?"
    exit 1
fi

if [ ! -d "$root_compiled_dir" ]; then
    echo -e "Error: $root_compiled_dir does not exist!\nMaybe run install/install.sh first?"
    exit 1
fi

# Arrays to store file names
user_services=()
user_services+=("$user_compiled_dir"/*) # add the names of all the files in $user_dir/ to the user_services array

root_services=()
root_services+=("$root_compiled_dir"/*) # add the names of all the files in $root_dir/ to the user_services array

# * Restart the services
# Restart the user services
echo -e "\nRestarting User Services..."
for service_file in "${user_services[@]}"; do
    if ! systemctl --user restart "$(basename "$service_file" .service)"; then
        echo "Error: Restarting $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo "done!"

# Restart the root services
echo -e "\nRestarting Root Services..."
for service_file in "${root_services[@]}"; do
    if ! sudo systemctl restart "$(basename "$service_file" .service)"; then
        echo "Error: Restarting $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo -e "done!\n"