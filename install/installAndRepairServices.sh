#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# * Define variables that will be used
# Source directories
user_dir="services/user"
root_dir="services/root"

# Destination directory
user_destination_dir="$HOME/.config/systemd/user/"
root_destination_dir="/etc/systemd/system/"

# Arrays to store file names
user_services=()
user_services+=("$user_dir"/*) # add the names of all the files in $user_dir/ to the user_services array

root_services=()
root_services+=("$root_dir"/*) # add the names of all the files in $root_dir/ to the user_services array

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
# Loop through each file in the user_dir
echo -e "\nCopying User Services..."
for file in "$user_dir"/*; do
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

# Loop through each file in the root_dir
echo -e "\nCopying Root Services..."
for file in "$root_dir"/*; do
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
for service_file in "${user_services[@]}"; do
    if ! systemctl --user start "$(basename "$service_file" .service)"; then
        echo "Error: Enabling $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo "done!"

# Start the root services
echo -e "\nStarting Root Services..."
for service_file in "${root_services[@]}"; do
    if ! sudo systemctl start "$(basename "$service_file" .service)"; then
        echo "Error: Enabling $(basename "$service_file" .service) service failed."
        exit 1
    fi
done
echo "done!"