#!/bin/bash

# * CD to the script file location
# Get the directory where the script is located
script_dir=$(dirname "$(readlink -f "$0")")

# Change the current directory to the script's directory
cd "$script_dir"

# Directory to search
SEARCH_DIR="../"

echo -e "Searching for .sh files in $(readlink -f "$SEARCH_DIR")\n"

find "$SEARCH_DIR" -type f -name "*.sh" | while read -r file; do
    echo -n -e "Checking $(basename "$file")..............."
    if [ "$(stat -c %a "$file")" != "700" ]; then
        # If not, set permissions to 700
        if ! chmod 700 "$file"; then
        echo "Error: Couldn't enable rwx permissions on $file!"
        exit 1
    fi
        echo -e "Set to 700\n"
    else
        echo -e "ok"
    fi
done
