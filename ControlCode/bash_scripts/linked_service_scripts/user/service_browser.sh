#!/bin/bash

echo "Sleeping..."

# Pause for 40 seconds total
sleep 20

# Log half-way point
echo "20 sec"

sleep 20


# Load the kiosk page
echo "Loading kiosk..."
firefox --new-window --kiosk "localhost:80"