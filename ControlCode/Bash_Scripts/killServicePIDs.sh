#!/bin/bash

# Search for custom PIDs that start with 'service_'
custom_pids=$(pgrep -d',' -f '^service_')

# Print the custom PIDs
echo "Custom PIDs found: $custom_pids"

# Example: Kill each custom PID
for pid in $(echo "$custom_pids" | tr ',' '\n'); do
    echo "Killing PID $pid"
    sudo kill "$pid"
done
