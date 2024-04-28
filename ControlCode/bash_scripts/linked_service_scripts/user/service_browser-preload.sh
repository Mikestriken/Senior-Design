#!/bin/bash

##############################################################################
#                        Browser Preload Service Script
# This script will be ran by the sd_browser-preload.service.
# 
# The main purprose of this script is to fix a bug where loading firefox in
# kiosk mode immediately on startup will cause the kiosk to load in a
# glitchy state (part of it loads, off screen).
# 
# This script starts an instance of firefox, to get the firefox browser
# application loaded and running before trying to open a kiosk view of the
# website.
#
# Created by Michael Marais, Spring 2024
##############################################################################

echo "Sleeping..."

# Pause for 20 seconds
sleep 20

# Load the browser
echo "Awake"
firefox
