#!/bin/bash

# Define the directory
dir="frontier_state"

# Check if the directory exists
if [ -d "$dir" ]; then
    # Remove all files in the directory
    rm -r "$dir"/*

    echo "All files in the $dir directory have been removed."
else
    echo "The $dir directory does not exist."
fi