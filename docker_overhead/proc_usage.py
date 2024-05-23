import sys

import numpy as np


def proc_single_usage(filename):
    with open(filename) as f:
        lines = f.readlines()
    gpu_usages, cpu_usages, mem_usages = [], [], []
    for l in lines:
        if l.startswith("GPU: "):
            gpu_usages.append(float(l.split()[-1]))
        elif l.startswith("CPU: "):
            cpu_usages.append(float(l.split()[-1]))
        elif l.startswith("Mem"):
            items = l.split()
            mem_usage = float(items[2]) / float(items[1])
            mem_usages.append(mem_usage * 100)
    # print(f"avg CPU: {np.mean(cpu_usages):.3f}, max CPU: {np.max(cpu_usages):.3f}, p90 CPU: {np.percentile(cpu_usages, 90):.3f}")
    # print(f"avg GPU: {np.mean(gpu_usages):.3f}, max GPU: {np.max(gpu_usages):.3f}, p90 GPU: {np.percentile(gpu_usages, 90):.3f}")
    # print(f"avg Mem: {np.mean(mem_usages):.3f}, max Mem: {np.max(mem_usages):.3f}, p90 Mem: {np.percentile(mem_usages, 90):.3f}")
    print(f"{np.mean(cpu_usages):.3f}")
    print(f"{np.mean(gpu_usages):.3f}")
    print(f"{np.mean(mem_usages):.3f}")


if __name__ == '__main__':
    for file in sys.argv[1:]:
        print(f".... processing {file} ....")
        proc_single_usage(file)