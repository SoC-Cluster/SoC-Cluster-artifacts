import sys
from typing import List


def del_none_type(s: List[str]):
    while True:
        if "" in s:
            s.remove("")
        else:
            break


def get_mnn_result_num(data_file: str) -> float:
    with open(data_file) as f:
        lines = f.readlines()
    for line in lines:
        split_line = line.split(" ")
        del_none_type(split_line)
        if len(split_line) >= 4 and split_line[-4] == "avg":
            print(split_line[-2])
            return float(split_line[-2])


def mnn_result(path_to_bb: str, file_name: str):
    result_sum = 0
    for i in range(101, 161):
        print(i, ":")
        result_sum = result_sum + get_mnn_result_num(
            path_to_bb + "/result/" + str(i) + "/" + file_name
        )
    result_avg = result_sum / 60
    print(result_avg)


def get_tfl_result_num(data_file: str) -> float:
    avg_result = 0
    with open(data_file) as f:
        lines = f.readlines()
    for line in lines:
        split_line = line.split(" ")
        del_none_type(split_line)
        if len(split_line) == 7:
            avg_result = split_line[-2].split("=")[-1]
    print(avg_result)
    return float(avg_result)


def tfl_result(path_to_bb: str, file_name: str):
    result_sum = 0
    for i in range(101, 161):
        print(i, ":")
        result_sum = result_sum + get_tfl_result_num(
            path_to_bb + "/result/" + str(i) + "/" + file_name
        )
    result_avg = result_sum / 60
    print(result_avg)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "usage: python3 process_soc_result.py tfl/mnn {model}_{device}_{batchsize}.log path_to_bb"
        )
        raise Exception("Should pass energy log file as param")
    else:
        if sys.argv[1] == "mnn":
            mnn_result(sys.argv[3], sys.argv[2])
        elif sys.argv[1] == "tfl":
            tfl_result(sys.argv[3], sys.argv[2])
