# Gem5 Perf Models with Microbenchmark

This repository containing modified versions of the gem5 simulator integrated with Bine-Brake, Darch, and Microbenchmark. This repository is set up to provide an easy way for you to build and run gem5 with these modifications. Below are the steps to get started:

## Getting Started

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/hegdeprajwal/perf-model.git
```

### 2. Clone the Repository
This repository includes submodules (gem5 from Bine Brank, gem5 from Darch and Microbenchmark), which need to be initialized and updated. Navigate to the repository root directory and run:
```bash
cd perf-model
git submodule update --init --recursive
```

### 3. Build Microbenchmark
Navigate to the microbenchmark directory:
```bash
cd microbench
```
To build Microbenchmark for the ARM architecture (make sure you are running this on ARM Machine), run the following command:
```bash
make ARM
```

### 4. Gather Binaries and run perf command
To collect the necessary binaries and modify to include .Y(n1 number of iterations) and .Z(n2 number of iterations) form of the benchmark, execute:
```bash
source gather_bin.sh
```
**Note:**
It is crucial to execute the build and run processes for two executables—one with the .Y variant (N1: lower loop count) and the other with the .Z variant (N2: higher loop count). This approach is employed to gather statistics specifically focused on the inside loop portion. The difference of N2 stats from N1 allows us to isolate and extract the statistics pertaining only to the code section inside the loop.

Run the perf command and collect stats for all the executables:
```bash
source run_perf.sh
```
### 5. Build gem5
Move to the gem5 directory:
```bash
cd ..
cd bine or darch model/grace_new
```
Build gem5 for the ARM architecture using SCons. You can specify the number of processor cores to use by replacing <nproc> with the desired number:
#### For Bine model
```bash
scons build/ARM/gem5.opt -j `nproc`
```
#### For Darch model
```bash
scons build/ALL_CHI/gem5.opt -j `nproc` --default=ALL PROTOCOL=CHI
```


### 6. Run gem5 simulation
#### For Bine model
Modify the bins `BINS_DIR` and `CPU_TYPE` if needed in `run_all.sh` script.
```bash
source run_all.sh
```
#### For Darch model
Modify the `_base_dir` in microbench\__init__.py to point to global `microbench/` directory that contains `bins` repo directory as
```bash
gem5/build/ALL_MESI_Three_Level/gem5.opt run_grace_all.py `cpu-type`
```
### 7. Gather all the stats
Gather all the stats and execute the following command to print the stats space separated which can be easily copied to excel or csv format
```bash
  python3 post_process.py `gsrc` `g_out` `p_src` `cpu`
```
- `gsrc` : Path to the gem5 stats folder
- `g_out` : Intermediate grep output from gem5 stats
- `p_src` : Path to the grep result of perf stats (run_perf in microbench creates grep result directly)
- `cpu` : CPU type to filter Default : GraceCPU

## Additional Information
- For more information on gem5 and its usage, please refer to the official gem5 documentation.
- For specific details about the Bine Brank and Darch modifications, please refer to their respective documentation or the associated repositories.

Sit back and enjoy your coffee! Happy Simulations!!