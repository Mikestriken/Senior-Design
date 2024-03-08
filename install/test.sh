#!/bin/bash

# Define a function called "calculate"
calculate () {
    result=$(( $1 + $2 ))
    echo "The result is: $result"
}

# Call the function "calculate" with two arguments
calculate 5 3
