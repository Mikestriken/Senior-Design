#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# * Define variables that will be used
# Source directories
user_dir="../ControlCode/service_files/user"
root_dir="../ControlCode/service_files/root"

# Compiled Source Directories
user_compiled_dir="$user_dir/compiled"
root_compiled_dir="$root_dir/compiled"

# Destination directory
user_destination_dir="$HOME/.config/systemd/user/"
root_destination_dir="/etc/systemd/system/"

# Service file compilation variable values
gitRepoDir="$(readlink -f "$script_dir/..")"

# Arrays to store file names
user_services=()
user_services+=("$user_dir"/*) # add the names of all the files in $user_dir/ to the user_services array

root_services=()
root_services+=("$root_dir"/*) # add the names of all the files in $root_dir/ to the user_services array


# * Create the "compiled" subdirectory if they it don't exist
if [ ! -d "$user_compiled_dir" ]; then
    echo "Creating user destination directory: $user_compiled_dir"
    sudo mkdir -p "$user_compiled_dir" || { echo "Error: Failed to create user destination directory."; exit 1; }
fi

if [ ! -d "$root_compiled_dir" ]; then
    echo "Creating user destination directory: $root_compiled_dir"
    sudo mkdir -p "$root_compiled_dir" || { echo "Error: Failed to create user destination directory."; exit 1; }
fi

# * Attempt to gain ownership of the compiled
if ! sudo chown $(whoami):$(whoami) "$user_compiled_dir"; then
    echo -e "\nError: Could not compile $file to $user_compiled_dir"
    exit 1
fi

if ! sudo chown $(whoami):$(whoami) "$root_compiled_dir"; then
    echo -e "\nError: Could not compile $file to $root_compiled_dir"
    exit 1
fi

echo "Compiling .service files..."

# Iterate through each user .service file and compile it
for file in $user_dir/*.service; do
    echo -n "compiling $(basename "$file")..............."
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Replace variables with their values and save the output to a new file in the "compiled" subdirectory
        if ! sudo sed "s@\$gitRepoDir@$gitRepoDir@g" "$file" > "$user_compiled_dir/$(basename "$file")"; then
            echo -e "\nError: Could not compile $file to $user_compiled_dir"
            exit 1
        fi
    else
        echo -e "\nError: Could not compile $file to $user_compiled_dir"
        exit 1
    fi
    echo "ok"
done

# Iterate through each root .service file and compile it
for file in $root_dir/*.service; do
    echo -n "compiling $(basename "$file")..............."
    # Check if the file is a regular file
    if [ -f "$file" ]; then
        # Replace variables with their values and save the output to a new file in the "compiled" subdirectory
        if ! sudo sed "s@\$gitRepoDir@$gitRepoDir@g" "$file" > "$root_compiled_dir/$(basename "$file")"; then
            echo -e "\nError: Could not compile $file to $root_compiled_dir"
            exit 1
        fi
    else
        echo -e "\nError: Could not compile $file to $root_compiled_dir"
        exit 1
    fi
    echo "ok"
done

echo -e "done.\n"
