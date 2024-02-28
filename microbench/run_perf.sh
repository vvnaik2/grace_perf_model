#!/bin/bash

# Directory to save perf results
output_dir="perf_results"

# Create the output directory
mkdir -p "$output_dir"

# Loop through all files in the "bins" folder
for file in ./bins/*; do
    if [ -f "$file" ]; then
        # Run perf stat and save results in a file in the output directory
        result_file="$output_dir/$(basename "$file").perf"
        echo "Running perf stat for $file..."
        perf stat -o "$result_file" -e instructions:u,cycles:u -r 100 "$file"
    fi
done

# Grep for instructions:u and cycles:u in all perf result files
grep -e "instructions:u" -e "cycles:u" "$output_dir"/* > "filtered_perf_results.txt"

echo "Results saved in filtered_perf_results.txt"

# Remove the output directory
rm -r "$output_dir