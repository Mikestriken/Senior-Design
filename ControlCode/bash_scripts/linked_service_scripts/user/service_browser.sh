#!/bin/bash

##############################################################################
#                        Climate Service Script
# This script is timed to start after the firefox browser has been preloaded.
# 
# This script will start a separate instance of firefox running in kiosk mode
# with the URL set to the webserver running locally.
#
# Created by Michael Marais, Spring 2024
##############################################################################

echo "Sleeping..."

# Pause for 40 seconds total
sleep 20

# Log half-way point
echo "20 sec"

sleep 20


# Load the kiosk page
echo "Loading kiosk..."
firefox --new-window --kiosk "localhost:80"