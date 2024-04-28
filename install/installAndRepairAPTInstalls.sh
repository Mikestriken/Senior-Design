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
packages=("mosquitto" "mosquitto-clients" "libcamera-dev")
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
    # Prompt user to press any key
    echo "After installation is complete, make sure to run the mosquitto client in the background for MQTT and Flask Server Functionality."
    echo "A good place to look is 'C:\Program Files\mosquitto', run mosquitto.exe when you find it."
    echo "Press any key to continue..."

    # Disable terminal input buffering and echo
    stty raw -echo

    # Read a single character
    keypress=''
    while [ "x$keypress" = "x" ]; do
        read -n 1 keypress
    done

    # Enable terminal input buffering and echo
    stty -raw echo
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
    # Prompt user to press any key
    echo "Make sure to run the mosquitto client status and ensure it's running in the background for MQTT and Flask Server Functionality"
    echo "Run 'sudo systemctl status mosquitto' to check its status, 'sudo systemctl enable mosquitto' to enable it and 'sudo systemctl start mosquitto' to start it..."
    echo "Press any key to continue..."

    # Disable terminal input buffering and echo
    stty raw -echo

    # Read a single character
    keypress=''
    while [ "x$keypress" = "x" ]; do
        read -n 1 keypress
    done

    # Enable terminal input buffering and echo
    stty -raw echo
fi

echo "All packages installed sucessfully!"