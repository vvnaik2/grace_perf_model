#!/bin/bash

# Source directory where you want to search for matching folders
src_dir="."

# Destination directory for ".ARM" files
dest_dir_bins="bins"

# Check if the destination directory exists; create it if not
mkdir -p "$dest_dir_bins"

# Loop through all directories in the source directory
for dir in "$src_dir"/*/; do
    # Check if the directory contains "bench.ARM"
    if [ -e "$dir/bench.ARM" ]; then
        # Move the ".ARM" file to the "bins" destination
        cp "$dir/bench.ARM" "$dest_dir_bins/$(basename "$dir").Y"
    fi

    # Check if the directory contains "bench_v1.ARM"
    if [ -e "$dir/bench_v1.ARM" ]; then
        # Move the ".ARM" file to the "bins" destination
        cp "$dir/bench_v1.ARM" "$dest_dir_bins/$(basename "$dir").Z"
    fi
done