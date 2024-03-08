#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# List of modules to install
packages=("pyserial" "RPi.GPIO" "picamera" "Flask" "greenlet" "paho-mqtt")
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