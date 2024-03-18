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

echo "Removing old compiled directory..."
if ! sudo rm -rf "$user_compiled_dir" ; then
    echo -e "\nError: Could not remove $user_compiled_dir"
    exit 1
fi

if ! sudo rm -rf "$root_compiled_dir" ; then
    echo -e "\nError: Could not remove $user_compiled_dir"
    exit 1
fi
echo "Successfully removed old compiled directory."

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

# Check if any user .service files exist
no_user_services=false
no_root_services=false


echo "Checking for user service files to compile..."

if [ "$(find "$user_dir" -maxdepth 1 -type f -name '*.service' | wc -l)" -eq 0 ]; then
    echo "No user '.service' files found in $user_dir"
    echo "Setting no_user_services flag..."
    no_user_services=true
fi

echo "Checking for root service files to compile..."

if [ "$(find "$root_dir" -maxdepth 1 -type f -name '*.service' | wc -l)" -eq 0 ]; then
    echo "No root '.service' files found in $root_dir"
    echo "Setting no_root_services flag..."
    no_root_services=true
fi

# Iterate through each user .service file and compile it
if [ "$no_user_services" = false ]; then
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
fi

# Iterate through each root .service file and compile it
if [ "$no_root_services" = false ]; then
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
fi

echo -e "done.\n"

# Arrays to store file names, this is used to call systemctl commands later with the file names as arguments
user_services=()
user_services+=("$user_compiled_dir"/*) # add the names of all the files in $user_compiled_dir/ to the user_services array

root_services=()
root_services+=("$root_compiled_dir"/*) # add the names of all the files in $root_compiled_dir/ to the user_services array

# * Check if the destination directories exist and create them if they don't
if [ ! -d "$user_destination_dir" ]; then
    echo "Creating user destination directory: $user_destination_dir"
    sudo mkdir -p "$user_destination_dir" || { echo "Error: Failed to create user destination directory."; exit 1; }
fi

if [ ! -d "$user_destination_dir/default.target.wants" ]; then
    echo "Creating user default.target.wants directory: $user_destination_dir"
    sudo mkdir -p "$user_destination_dir/default.target.wants" || { echo "Error: Failed to create user destination directory."; exit 1; }
    sudo chown $(whoami):$(whoami) "$user_destination_dir/default.target.wants"
fi

if [ "$(stat -c "%U" "$user_destination_dir/default.target.wants")" != "$(whoami)" ]; then
    sudo chown $(whoami):$(whoami) "$user_destination_dir/default.target.wants"
    echo "Ownership of $user_destination_dir/default.target.wants changed to $(whoami)."
else
    echo "Ownership of $user_destination_dir/default.target.wants is already $(whoami)."
fi

if [ ! -d "$root_destination_dir" ]; then
    echo "Creating root destination directory: $root_destination_dir"
    sudo mkdir -p "$root_destination_dir" || { echo "Error: Failed to create root destination directory."; exit 1; }
fi

# * Copy all the service files
# Loop through each file in the user_compiled_dir
echo -e "\nCopying User Services..."
if [ "$no_user_services" = false ]; then
    for file in "$user_compiled_dir"/*; do
        # Get the filename without the path
        filename=$(basename "$file")
        
        # Check if the file exists in the user_destination_dir
        if [ -e "$user_destination_dir/$filename" ]; then
            # If the file exists, compare contents
            if sudo cmp -s "$file" "$user_destination_dir/$filename"; then
                echo "File $filename have the same content. No action needed."
            else
                # If the contents are different, replace the file
                sudo cp "$file" "$user_destination_dir/$filename"
                echo "File $filename have different content. Replaced."
            fi
        else
            # If the file does not exist in the user_destination_dir, copy it over
            sudo cp "$file" "$user_destination_dir/$filename"
            echo "Copied $filename to destination."
        fi
    done
fi

# Loop through each file in the root_compiled_dir
echo -e "\nCopying Root Services..."
if [ "$no_root_services" = false ]; then
    for file in "$root_compiled_dir"/*; do
        # Get the filename without the path
        filename=$(basename "$file")
        
        # Check if the file exists in the root_destination_dir
        if [ -e "$root_destination_dir/$filename" ]; then
            # If the file exists, compare contents
            if sudo cmp -s "$file" "$root_destination_dir/$filename"; then
                echo "File $filename have the same content. No action needed."
            else
                # If the contents are different, replace the file
                sudo cp "$file" "$root_destination_dir/$filename"
                echo "File $filename have different content. Replaced."
            fi
        else
            # If the file does not exist in the root_destination_dir, copy it over
            sudo cp "$file" "$root_destination_dir/$filename"
            echo "Copied $filename to destination."
        fi
    done
fi

echo "Service files coppied!"

# * Enable the service files
# Reloading systemctl so that copied files are visible to it
echo -e "\nreloading the systemctl daemon..."
if ! sudo systemctl daemon-reload; then
    echo "Error: reloading root systemctl."
    exit 1
fi

if ! systemctl --user daemon-reload; then
    echo "Error: reloading user systemctl."
    exit 1
fi
echo "done!"

# Enable the user services
echo -e "\nEnabling User Services..."
if [ "$no_user_services" = false ]; then
    for service_file in "${user_services[@]}"; do
        if ! systemctl --user enable "$(basename "$service_file" .service)"; then
            echo "Error: Enabling $(basename "$service_file" .service) service failed."
            exit 1
        fi
    done
fi
echo "done!"

# Enable the root services
echo -e "\nEnabling Root Services..."
if [ "$no_root_services" = false ]; then
    for service_file in "${root_services[@]}"; do
        if ! sudo systemctl enable "$(basename "$service_file" .service)"; then
            echo "Error: Enabling $(basename "$service_file" .service) service failed."
            exit 1
        fi
    done
fi
echo -e "done!\n"

# * Optionally start the services as well
valid=false
# Ask the user if they want to start the services
read -p "Would you like to start these services now [y/n]? " choice
case "$choice" in 
y|Y ) 
    # Start the services here
    echo -e "\nStarting services..."
    valid=true
    ;;
n|N ) 
    echo "Exiting without starting services."
    exit 0
    ;;
* ) 
    # Invalid input, do nothing
    ;;
esac

while [ "$valid" = false ]
do
    read -p "" choice
    case "$choice" in 
    y|Y ) 
        # Start the services here
        echo -e "\nStarting services..."
        valid=true
        ;;
    n|N ) 
        echo "Exiting without starting services."
        exit 0
        ;;
    * ) 
        # Invalid input, do nothing
        ;;
    esac
done

# Start the user services
echo -e "\nStarting User Services..."
if [ "$no_user_services" = false ]; then
    for service_file in "${user_services[@]}"; do
        if ! systemctl --user start "$(basename "$service_file" .service)"; then
            echo "Error: Enabling $(basename "$service_file" .service) service failed."
            exit 1
        fi
    done
fi
echo "done!"

# Start the root services
echo -e "\nStarting Root Services..."
if [ "$no_root_services" = false ]; then
    for service_file in "${root_services[@]}"; do
        if ! sudo systemctl start "$(basename "$service_file" .service)"; then
            echo "Error: Enabling $(basename "$service_file" .service) service failed."
            exit 1
        fi
    done
fi
echo "done!"