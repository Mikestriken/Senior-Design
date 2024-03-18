#!/bin/bash

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

# List of packages to install
packages=("mosquitto" "mosquitto-clients")
winPackages=("mosquitto")

# Loop through the list of packages
if [ "$windows" == true ]; then
    # Loop through the list of packages
    for pkg in "${winPackages[@]}"; do
        # Check if the package is already installed
        if winget list | grep -i -q "$pkg"; then
            echo -e "\n$pkg is already installed\n"
        else
            # Attempt to install the package
            winget install -e $pkg
            
            # Check the exit code of the installation
            if [ $? -eq 0 ]; then
                echo -e "\nSuccessfully installed $pkg\n"
            else
                echo -e "\nFailed to install $pkg\n"
                exit 1
            fi
        fi
    done
else
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
fi

echo "All packages installed sucessfully!"