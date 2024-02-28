"""
This file is for exposing the binaries in this repo as gem5 workloads.
"""

from gem5.resources.resource import BinaryResource
from gem5.resources.workload import CustomWorkload

from pathlib import Path
import os

#Absolute path to microbench
_base_dir = '../../microbench/'

source_directory = "bins"
benchmarks = {}
for root, dirs, files in os.walk(str(_base_dir)+"/"+source_directory):
    for file in files:
        if file.endswith(".Y"):
            # Create a key for .Y files by removing the extension
            key = file.replace('.', '_')
            # Create the corresponding value by appending ".Y" to the path
            value = os.path.join(source_directory, file)
            benchmarks[key] = value
        elif file.endswith(".Z"):
            # Create a key for .Z files by removing the extension
            key = file.replace('.', '_')
            # Create the corresponding value by appending ".Z" to the path
            value = os.path.join(source_directory, file)
            benchmarks[key] = value

workloads = {}
for benchmark, binary_path in benchmarks.items():
    workload = CustomWorkload(
        function="set_se_binary_workload",
        parameters={
            "binary": BinaryResource(str(_base_dir)+"/"+binary_path),
        },
    )
    workloads[benchmark] = workload