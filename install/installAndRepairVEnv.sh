#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# List of modules to install
# Note: if package is raspberry specific, add it to raspberryPackages... Otherwise, just add it to packages.
packages=("Flask" "flask-socketio" "greenlet" "paho-mqtt")
raspberryPackages=("pyserial" "RPi.GPIO" "rpi-libcamera" "rpi-kms" "picamera2" "opencv-python" )

# Specify the directory for the virtual environment
venv_dir="../venv"

# Flag if venv folder detected
venvDetected=false
if [ -d "$venv_dir" ]; then
    venvDetected=true
fi

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

# * Update packages list based on OS
echo -e "Updating packages list for specified OS...\n"
if [ "$windows" = false ]; then
    # If not on Windows, append raspberryPackages to packages
    packages+=("${raspberryPackages[@]}")
fi

echo -e "\ndone.\n"

# * If venv directory detected, try to access it
venvAccessed=false
if [ "$venvDetected" = true ]; then
    echo -e "Detected venv directory, attempting to access it...\n"

    # Activate the virtual environment
        # Check if 'windows' is set to true
    if [ "$windows" = true ]; then
        if ! source $venv_dir/Scripts/activate; then
            echo -e "Error: Couldn't set source to detected venv!\nAttempting to create a new venv...\n"
            rm -rf $venv_dir
        else
            echo -e "Success! Skipping venv installation...\n"
            venvAccessed=true
        fi
    else
        if ! source $venv_dir/bin/activate; then
            echo -e "Error: Couldn't set source to detected venv!\nAttempting to create a new venv...\n"
            sudo rm -rf $venv_dir
        else
            echo -e "Success! Skipping venv installation...\n"
            venvAccessed=true
        fi
    fi
fi

if [ "$venvAccessed" = false ]; then
    echo -e "Creating venv...\n"

    # Create a Python virtual environment
    if ! python -m venv "$venv_dir"; then
        echo "Error: Couldn't create virtual environment!"
        exit 1
    fi

    echo -e "\ndone.\n"

    echo -e "Activating venv...\n"

    # Activate the virtual environment
    if [ "$windows" = true ]; then
        if ! source $venv_dir/Scripts/activate; then
        echo "Error: Couldn't set source to venv!"
        exit 1
        fi
    else
        if ! source $venv_dir/bin/activate; then
        echo "Error: Couldn't set source to venv!"
        exit 1
        fi
    fi

    echo -e "\ndone.\n"
fi


echo -e "Installing modules...\n"

# Loop through the list of packages
for pkg in "${packages[@]}"; do
    # Check if the package is already installed
    if pip show "$pkg" &> /dev/null; then
        echo -e "\n$pkg is already installed\n"
    else
        # Attempt to install the package
        pip install "$pkg"

        # Check the exit code of the installation
        if [ $? -eq 0 ]; then
            echo -e "\nSuccessfully installed $pkg\n"
        else
            echo -e "\nFailed to install $pkg\n"
            exit 1
        fi
    fi
done

echo "All packages installed successfully!"