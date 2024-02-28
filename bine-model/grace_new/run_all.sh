#!/bin/bash

# Define the directory containing the NPB_SER files
BINS_DIR="../../microbench/bins/"
CPU_TYPE="Grace_Pipelined"

# Iterate over files in the NPB_SER directory
for file in $BINS_DIR/*
do
    if [ -f "$file" ]; then
        filename=$(basename -- "$file")
            echo $file
            # Extract the file name without the path and extension
            filename=$(basename -- "$file")
            filename_ext="${filename%.*}"
            new_filename="${CPU_TYPE}_${filename_ext}_${filename##*.}"

            #echo "File name $new_filename"

            # Build and execute the gem5 command
            build/ARM/gem5.opt -d "gem5_grace_pipeline/$new_filename" ./configs/example/se.py --cpu-type=$CPU_TYPE --caches -n=1 --mem_latency=20ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz --cmd="$file"

            echo "Executed gem5 for $new_filename"
        # fi
    fi
done
