import os
import subprocess
import sys
import time
from functools import lru_cache

from parse_intel_cpu_output import parse_power, parse_power_eff
from utils import get_bitrate, get_video_stats, get_videos

normal_logs = "cpulogs"  # online/offline transcoding
power_eff_logs = "cpu-power-eff-logs"
offline_output = "cpu_output_offline"
online_output = "cpu_output_online"


@lru_cache(maxsize=None)
def offline_tr(input, cpuset=None):
    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -benchmark -i /videos/{input} -c:v libx264 -crf 18 -preset veryslow -y /videos/{offline_output}/{input}"
    )
    print(f"Offline command: {tr_cmd}")
    return tr_cmd


@lru_cache(maxsize=None)
def online_tr(input, cpuset=None):
    bitrate = get_bitrate("ffprobe", f"videos/{input}")
    resolution, framerate = get_video_stats("ffprobe", f"videos/{input}")
    if framerate > 30:
        target_bitrate = 3 * resolution
    else:
        target_bitrate = 2 * resolution
    target_bitrate = bitrate / 2 if target_bitrate > bitrate / 2 else target_bitrate

    if (resolution / 1000) > 4000:
        preset = "ultrafast"
    elif (resolution / 1000) > 1000:
        preset = "superfast"
    else:
        preset = "veryfast"

    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -benchmark -i /videos/{input} -c:v libx264 -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
        + f"-preset {preset} -tune zerolatency -y /videos/{online_output}/{input}"
    )
    print(f"Online command: {tr_cmd}")
    return tr_cmd


def run_tr(input, offline, cpuset):
    turbostat_cmd = "turbostat --Summary --quiet --show PkgWatt,RAMWatt"
    # idle mode power
    idle = subprocess.check_output(
        f"{turbostat_cmd} sleep 10s",
        shell=True,
        stderr=subprocess.STDOUT,
    )
    # print(idle.decode("utf-8"))

    # work mode power
    if offline:
        work = subprocess.check_output(
            f"{turbostat_cmd} {offline_tr(input, cpuset)}",
            shell=True,
            stderr=subprocess.STDOUT,
        )
    else:
        work = subprocess.check_output(
            f"{turbostat_cmd} {online_tr(input, cpuset)}",
            shell=True,
            stderr=subprocess.STDOUT,
        )
    if cpuset:
        corenum = int(cpuset.split("-")[1]) - int(cpuset.split("-")[0]) + 1
    else:
        corenum = 80

    if offline:
        log_path = f"{normal_logs}/offline/"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log = os.path.join(log_path, f"{input}-{corenum}.log")
        with open(log, "w") as f:
            f.write(idle.decode("utf-8") + "\n")
            f.write(work.decode("utf-8") + "\n")


@lru_cache(maxsize=None)
def online_tr_infinite(input):
    bitrate = get_bitrate("ffprobe", f"videos/{input}")
    resolution, framerate = get_video_stats("ffprobe", f"videos/{input}")
    if framerate > 30:
        target_bitrate = 3 * resolution
    else:
        target_bitrate = 2 * resolution
    target_bitrate = bitrate / 2 if target_bitrate > bitrate / 2 else target_bitrate

    if (resolution / 1000) > 4000:
        preset = "ultrafast"
    elif (resolution / 1000) > 1000:
        preset = "superfast"
    else:
        preset = "veryfast"

    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -benchmark -re -stream_loop 10 -i /videos/{input} -c:v libx264 -threads 1 "
        + f"-b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
        + f"-preset {preset} -tune zerolatency -f null -"
    )

    return tr_cmd


def log_runtime_power(output):
    cmd = f"turbostat --Summary --quiet --show PkgWatt,RAMWatt --interval 1 --out {output}"
    p = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p


def test_stream_num_power_eff(input, num_streams):
    idlep = log_runtime_power(f"{power_eff_logs}/{num_streams}_{input}_idle.log")
    time.sleep(30)
    idlep.terminate()

    # work mode power
    threads = []
    pp = log_runtime_power(f"{power_eff_logs}/{num_streams}_{input}.log")
    for _ in range(num_streams):
        p = subprocess.Popen(
            online_tr_infinite(input).split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        threads.append(p)
    # wait for all processes to finish
    [p.wait() for p in threads]
    # terminate power log thread
    pp.terminate()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "offline":
            if not os.path.exists(f"videos/{offline_output}/"):
                os.makedirs(f"videos/{offline_output}/")

            cpusets = ["10-17"]
            for cpuset in cpusets:
                print(f"Current cpuset: {cpuset}")
                subprocess.check_output(
                    f"docker update ffmpeg_exp --cpuset-cpus={cpuset}", shell=True
                )
                for v in get_videos():
                    run_tr(v, offline=True, cpuset=cpuset)
                    time.sleep(120)

            # parse output
            parse_power(normal_logs, "offline", cpu_num=8, stream_num=1)

        elif sys.argv[1] == "online":
            if not os.path.exists(f"videos/{online_output}/"):
                os.makedirs(f"videos/{online_output}/")

            # generagte online transcoding outputs
            for v in get_videos():
                run_tr(v, offline=False, cpuset=None)
                time.sleep()

        elif sys.argv[1] == "power-eff":
            if not os.path.exists(power_eff_logs):
                os.makedirs(power_eff_logs)
            streams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20]
            for s in streams:
                for v in get_videos():
                    if "hall" not in v and "pre" not in v:
                        continue
                    print(f"Current video: {v}, stream_num={s}")
                    test_stream_num_power_eff(input=v, num_streams=s)
                    time.sleep(60)

            # parse output
            parse_power_eff(power_eff_logs)
