#!/bin/bash

# list PIDs that have a custom tag that start with 'service_'
pgrep -d',' -f '^service_'