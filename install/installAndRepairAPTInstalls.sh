#!/bin/bash

# List of packages to install
packages=("mosquitto" "mosquitto-clients")

# Loop through the list of packages
for pkg in "${packages[@]}"; do
    # Check if the package is already installed
    if dpkg -l | grep -q "^ii  $pkg"; then
        echo -e "\n$pkg is already installed\n"
    else
        # Attempt to install the package
        sudo apt install -y $pkg
        
        # Check the exit code of the installation
        if [ $? -eq 0 ]; then
            echo -e "\nSuccessfully installed $pkg\n"
        else
            echo -e "\nFailed to install $pkg\n"
            exit 1
        fi
    fi
done

echo "All packages installed sucessfully!"