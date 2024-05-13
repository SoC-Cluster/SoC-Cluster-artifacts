import os
import re
from statistics import mean

from utils import get_videos


def parse_nvidia_dmon_power(file):
    """read and get avg power from "nvidia-smi dmon" command log"""
    with open(file) as f:
        lines = f.readlines()
    p = []
    for line in lines:
        if "#" in line:
            continue
        items = line.split()
        if len(items) != 10:
            continue
        p.append(float(items[1]))
    return mean(p)


def parse_throughput(folder, type, streams_num):
    """
    type: online or offline

    First, we need to identify streams_num:
        - for offline transcoding, streams_num is always 1 (passed through parameter);

    All tests are performed repeatedly N times (testing_times = N = 10).
    So, we need to calculate average fps for each test, and get the average fps.

    Last, cause the power consumption has been averaged, we directly use {power} / {avgfps} to get power consumption of each frame.
    """
    folder = os.path.join(folder, type)

    for file in os.listdir(folder):
        if file.endswith(".log"):
            finish_times = []
            video_name = file.split(".")[0]

            with open(os.path.join(folder, file), "r") as f:
                lines = f.readlines()

            # extract idle/work power
            idle_power = float(lines[1].split()[-1])
            work_power = float(lines[3].split()[-1])

            # extract all finish times from ffmpeg log
            for line in lines:
                if "rtime" in line:
                    m = re.match(".+ rtime=([0-9]+\.[0-9]+)s", line)
                    finish_times.append(float(m.group(1)))

            # testing may be performed multiple itmes, we process each test here
            throughputs = []  # used to saved averaged throughput for each testing
            testing_times = len(finish_times) / streams_num
            for i in range(int(testing_times)):
                finish_time_this = finish_times[i]
                total_frames = int(video_name.split("_")[-1]) * 5
                throughput = total_frames / finish_time_this
                throughputs.append(throughput)

            # calculate average throughput and power consumption
            th = mean(throughputs)
            po = (work_power - idle_power) / th

            print(
                f"{folder}/{video_name}, average_throughput={th}, idle={idle_power}, work={work_power}, power={po}"
            )


def parse_power_eff(folder):
    stream_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20]
    for s in stream_num:
        print(f"============== stream number: {s} ======")
        for v in get_videos():
            if "hall" not in v and "pre" not in v:
                continue
            idle = f"{s}_{v}_idle.log"
            work = f"{s}_{v}.log"
            idle_power = parse_nvidia_dmon_power(os.path.join(folder, idle))
            work_power = parse_nvidia_dmon_power(os.path.join(folder, work))
            power_diff = work_power - idle_power
            print(
                f"{v}, stream_num={s}, idle={idle_power}, work={work_power}, total_power_diff={power_diff}, power_per_frame={power_diff / s}"
            )


if __name__ == "__main__":
    parse_throughput("gpulogs", "offline", 1)
    parse_power_eff("gpu-power-eff-logs")
