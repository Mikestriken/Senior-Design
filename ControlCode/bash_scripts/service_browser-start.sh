#!/bin/bash

echo "Sleeping..."

# Pause for 60 seconds
sleep 30
echo "30 sec"
sleep 30

echo "Awake"

# Load the browser
systemctl --user start sd_browser