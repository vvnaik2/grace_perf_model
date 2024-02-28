import subprocess
import argparse
import re

def process_line(line) :
    line_stat = line.split("/")[-2:]
    #Extract cpu, benchmark, iteration
    #Expecting CPU_{Benchmark}_Iter
    parts = line_stat[0].split('_')
    cpu, it = parts[0], parts[-1]
    parts.remove(cpu)
    parts.remove(it)
    benchmark = "_".join(parts)

    pattern = r'.*[.:](\S+)\s+(\d+)'
    matches = re.findall(pattern, line_stat[1])
    event, value = matches[0][0], matches[0][1]
    return (cpu, benchmark, it, event, value)

def process_gem5_file(file_name, cpu_type) :
    """
    Process the file for the stats
    Go through each line and extract the fields
    Get to the following format
    [list of cpu_benchmark dictionary]
    """
    cpu_benchmark = dict()
    with open(file_name, 'r') as file:
        for line in file :
            cpu, benchmark, it, event, value = process_line(line)
            print(cpu, benchmark, it, event, value)
            if cpu == cpu_type :
                key = f"{benchmark}"
                if key not in cpu_benchmark:
                    cpu_benchmark[key] = {"Y":{}, "Z":{}}
                cpu_benchmark[key][it][event] = int(value)

    #Process each of the benchmark and get the difference in
    #simInsts and Cycles count
    for key, values in cpu_benchmark.items():
        for event in values["Y"]:
            if not (event not in values["Z"].keys()
                or event not in values["Y"].keys() ) :
                diff = values["Z"][event] - values["Y"][event]
                cpu_benchmark[key]["final count"] = cpu_benchmark[key].get("final count", {})
                cpu_benchmark[key]["final count"][event] = diff

    return cpu_benchmark

def process_perf_file(file_name):

    benchmark_data=dict()
    with open(file_name, 'r') as file:
        for line in file :
            parts = line.split()
            if len(parts) >= 4:
                filename = parts[0].split("/")[-1]
                value = parts[1]
                event = parts[2]

                benchmark, stat_type = filename.split('.')[0], filename.split('.')[1]

                # Create a sub-dictionary for the benchmark if it doesn't exist
                if benchmark not in benchmark_data:
                    benchmark_data[benchmark] = {}

                # Populate the sub-dictionary with the corresponding "Y" or "Z" stat
                #NOTE: Dividing by 100 since grace gives cumulative result
                #Remove this if we get avg of 100 runs
                if "instructions" in event:
                    benchmark_data[benchmark][stat_type] = {"instructions": int(int(value.replace(',',''))/100)}
                elif "cycles" in event:
                    benchmark_data[benchmark][stat_type]["cycles"] = int(int(value.replace(',',''))/100)

    for key, values in benchmark_data.items():
        if("Y" in values.keys() and "Z" in values.keys()) :
            for event in values["Y"]:
                if not (event not in values["Z"].keys()
                    or event not in values["Y"].keys() ) :
                    diff = values["Z"][event] - values["Y"][event]
                    benchmark_data[key]["final count"] = benchmark_data[key].get("final count", {})
                    benchmark_data[key]["final count"][event] = diff

    return benchmark_data

def run_grep(pattern, dest_folder, output_file_path):
    with open(output_file_path, 'w') as output_file:
        try:
            subprocess.check_call(["grep", "-r", pattern, dest_folder], stdout=output_file)
            print(f"Output saved to {output_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running grep: {e}")

def get_all_stat(perf_res, gem5_result) :
    for key, values in perf_res.items():
    #benchmark, perf_instr, perf_cyc, gem5_instr, gem5_count
        benchmark = key
        perf_instr, perf_cyc = None, None
        gem5_instr, gem5_cyc = None, None
        if "final count" in values.keys() :
            perf_instr = values["final count"]['instructions']
            perf_cyc = values["final count"]['cycles']

        if key in gem5_result.keys():
            if "final count" in gem5_result[key].keys():
                gem5_instr = gem5_result[key]["final count"]['simInsts']
                gem5_cyc   = gem5_result[key]["final count"]['numCycles']

        print(benchmark, perf_instr, perf_cyc, gem5_instr, gem5_cyc)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gsrc", help="Path to the destination folder")
    parser.add_argument("g_out", nargs='?', help="Path to the output grep file", default="grep_result.txt")
    parser.add_argument("p_src", nargs='?', help="Path to the perf grep file", default="filtered_perf_results.txt")
    parser.add_argument("cpu", nargs='?', help="filter cpu type", default="Grace_CPU")

    args = parser.parse_args()

    pattern = "simInsts\|numCycles"
    run_grep(pattern, args.gsrc, args.g_out)

    gem5_result = process_gem5_file(args.g_out, args.cpu)
    perf_res = process_perf_file(args.p_src)
    get_all_stat(perf_res, gem5_result)





