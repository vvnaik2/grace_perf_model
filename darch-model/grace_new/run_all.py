
from gem5.utils.multiprocessing import Process

from microbench_experiments import get_benchmarks, run_grace_microbench

if __name__ == "__m5_main__":

    # Note: The code below is set up so that we can run many tests in parallel
    # I will extend this script later to do this. For now, we just run one
    # test. To use other benchmarks, you will need to edit the
    # microbench/workloads.py file

    # Note that the outdir is set to the name here.
    print(get_benchmarks())
    for benchmark in get_benchmarks() :
        p1 = Process(target=run_microbench, args=(benchmark,), name=benchmark)
        p1.start()
        p1.join()