import sys
from typing import List


def write_to_file(array, filename):
    file = open(filename, mode="w")
    for num in array:
        file.write(str(num) + "\n")
    file.close()


def del_none_type(s: List[str]):
    while True:
        if "" in s:
            s.remove("")
        else:
            break


def get_resnet_throughput(data_file: str) -> float:
    with open(data_file) as f:
        lines = f.readlines()
    for line in lines:
        split_line = line.split(" ")
        del_none_type(split_line)
        if len(split_line) == 7 and split_line[0] == "count=50":
            return 1000000 / float(split_line[-2].split("=")[-1])
    return 0


def resnet_result(path_to_bb: str):
    resnet_gpu_throughputs = []
    resnet_socs = [1, 5, 10, 20, 30]
    resnet_bss = [1, 2, 4, 8, 16, 24]
    for resnet_soc in resnet_socs:
        tmp_gpu_throughput = 0
        for i in range(101, 101 + resnet_soc):
            tmp_gpu_throughput = tmp_gpu_throughput + get_resnet_throughput(
                path_to_bb
                + "/result/"
                + str(i)
                + "/workload_result/resnet_gpu_soc"
                + str(resnet_soc)
                + "_bs1.txt"
            )
        resnet_gpu_throughputs.append(tmp_gpu_throughput)
    for resnet_bs in resnet_bss:
        tmp_gpu_throughput = 0
        for i in range(101, 161):
            tmp_gpu_throughput = tmp_gpu_throughput + resnet_bs * get_resnet_throughput(
                path_to_bb
                + "/result/"
                + str(i)
                + "/workload_result/resnet_gpu_soc60_bs"
                + str(resnet_bs)
                + ".txt"
            )
        resnet_gpu_throughputs.append(tmp_gpu_throughput)
    print(resnet_gpu_throughputs)


def get_yolo_throughput(data_file: str) -> float:
    with open(data_file) as f:
        lines = f.readlines()
        target_lines = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39]
        total_throughput = 0
        for target_line in target_lines:
            total_throughput = total_throughput + 1000 / float(
                lines[target_line].split(" ")[-2]
            )
        return total_throughput / 10


def yolo_result(path_to_bb: str):
    yolo_gpu_throughputs = []
    yolo_socs = [1, 2, 3, 4, 5, 10, 15, 20, 30, 40, 50, 60]
    for yolo_soc in yolo_socs:
        tmp_gpu_throughput = 0
        for i in range(101, 101 + yolo_soc):
            tmp_gpu_throughput = tmp_gpu_throughput + get_yolo_throughput(
                path_to_bb
                + "/result/"
                + str(i)
                + "/workload_result/yolo_gpu_soc"
                + str(yolo_soc)
                + "_bs1.txt"
            )
        yolo_gpu_throughputs.append(tmp_gpu_throughput)
    print(yolo_gpu_throughputs)


if __name__ == "__main__":
    resnet_result(sys.argv[1])
    yolo_result(sys.argv[1])
