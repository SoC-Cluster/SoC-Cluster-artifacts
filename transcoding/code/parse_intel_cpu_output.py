import os
import re
from statistics import mean

from utils import get_videos


def parse_throughput(folder, type, cpu_num, streams_num):
    """DEPRECATED"""
    print(f"Parsing {folder}/{type} results ... {cpu_num=}, {streams_num=}")
    folder = os.path.join(folder, type)

    for file in os.listdir(folder):
        if file.endswith(f"{cpu_num}.log"):
            finish_times = []
            video_name = file.split(".")[0]

            # extract finish times from ffmpeg log
            with open(os.path.join(folder, file), "r") as f:
                lines = f.readlines()
            for line in lines:
                if "rtime" in line:
                    m = re.match(".+ rtime=([0-9]+\.[0-9]+)s", line)
                    finish_times.append(float(m.group(1)))

            # processing all frames
            total_frames = int(video_name.split("_")[-1]) * streams_num * 5
            total_time = max(finish_times)
            print(
                f"{video_name}, {total_time=}, {total_frames=}, throughput={total_frames / total_time}"
            )


def parse_power(folder, type, cpu_num, streams_num):
    print(f"Parsing {folder}/{type} results ... {cpu_num=}, {streams_num=}")
    print("=============================================")
    folder = os.path.join(folder, type)

    for file in os.listdir(folder):
        if file.endswith(f"{cpu_num}.log"):
            video_name = file.split(".")[0]
            # extract finish times from ffmpeg log
            with open(os.path.join(folder, file), "r") as f:
                lines = f.readlines()
            p = lines[2].split()
            idle_cpu_power, idle_ram_power = float(p[0]), float(p[1])
            p = lines[-2].split()
            work_cpu_power, work_ram_power = float(p[0]), float(p[1])
            for line in lines:
                if "rtime" in line:
                    m = re.match(".+ rtime=([0-9]+\.[0-9]+)s", line)
                    finish_time = float(m.group(1))

            power_diff = (work_cpu_power + work_ram_power) - (
                idle_cpu_power + idle_ram_power
            )
            total_frames = int(video_name.split("_")[-1]) * streams_num * 5
            throughput = total_frames / finish_time
            power = power_diff / throughput
            print(f"{video_name}, {throughput=} (frame/s), {power=} (Joule/frame)")


def parse_turbostat_log(file):
    """turbostat log format:
    PkgWatt	RAMWatt
    171.95	161.63
    172.45	161.23
    168.38	158.91
    xxx     xxx

    return avg_cpu_power, avg_ram_power
    """
    with open(file) as f:
        lines = f.readlines()
    cpu, ram = [], []
    for line in lines[1:]:
        cpu.append(float(line.split()[0]))
        ram.append(float(line.split()[1]))
    return mean(cpu), mean(ram)


def parse_power_eff(power_eff_folder):
    stream_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20]
    for s in stream_num:
        print(f"============== stream number: {s} ======")
        for v in get_videos():
            if not "pre" in v and not "hall" in v:
                continue
            idle_log = os.path.join(power_eff_folder, f"{s}_{v}_idle.log")
            work_log = os.path.join(power_eff_folder, f"{s}_{v}.log")
            cpu_idle, ram_idle = parse_turbostat_log(idle_log)
            cpu_work, ram_work = parse_turbostat_log(work_log)
            idle = cpu_idle + ram_idle
            work = cpu_work + ram_work
            cpu_diff = cpu_work - cpu_idle
            ram_diff = ram_work - ram_idle
            print(
                f"{v}, stream_num={s}, idle={idle}, work={work}, total_power_diff={work-idle}, power_per_frame={(work-idle)/s}"
            )


if __name__ == "__main__":
    """Latency/power exp:
    folder: cpulogs-power
    scenario: offline
    cpu cores: 8
    num_streams: 1
    """
    parse_power("cpulogs", "offline", cpu_num=8, streams_num=1)

    """Power efficiency exp:
            folder: cpu-power-eff-logs
    """
    parse_power_eff("cpu-power-eff-logs")
