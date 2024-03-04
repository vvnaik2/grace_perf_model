#!/bin/bash

# Function to remove substring from filename
remove_substring() {
    local filename="$1"
    local substring="$2"
    
    # Replace substring with an empty string in the filename
    new_filename="${filename//$substring/}"
    
    # Check if the new filename is different from the original filename
    if [[ "$filename" != "$new_filename" ]]; then
        mv "$filename" "$new_filename"
        echo "Renamed $filename to $new_filename"
    fi
}

# Main script starts here
directory="/home/vishaln/research/checkin/grace_perf_model/microbench/bins"  # Specify the directory path
substring="*in" # Specify the substring to remove

# Change directory to the target directory
cd "$directory" || exit

# Loop through each file in the directory
for file in *; do
    # Check if it's a regular file (not a directory)
    if [ -f "$file" ]; then
        remove_substring "$file" "$substring"
    fi
done

echo "All files processed."

