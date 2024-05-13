import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import List

import numpy as np
from parse_nvidia_gpu_output import parse_power_eff, parse_throughput
from utils import get_bitrate, get_video_stats, get_videos

GPU_INDEX = os.getenv("GPU_INDEX", 0)
print("Use gpu index", GPU_INDEX)
nvidia_smi_cmd = f"nvidia-smi --id={GPU_INDEX} --format=csv,noheader --query-gpu=power.draw,utilization.memory,utilization.gpu"
pool = ThreadPoolExecutor(max_workers=3)
finish_tr = False
offline_cq = 16
normal_logs = "normal_logs"
offline_output = "gpu_output_offline"
online_output = "gpu_output_online"
power_eff_logs = "gpu_power_eff_logs"


def log_power(powers: List):
    i = 0
    st = time.time()
    while not finish_tr:
        p = subprocess.check_output(nvidia_smi_cmd, shell=True)
        powers.append(p)
        time.sleep(0.1)
        i += 1
    print(
        f"Terminate power log thread after logging {i} times, total time: {time.time() - st} ms"
    )


# ref:
#   nvenc visually loseless https://superuser.com/a/1236387
#   https://obsproject.com/forum/threads/influence-of-settings-for-nvenc-lossless-recording.147457/ (16 is visually loseless)
@lru_cache(maxsize=None)
def offline_tr(input):
    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -i /videos/{input} -c:v h264_nvenc -cq {offline_cq} -preset p5 -tune hq -y /videos/{offline_output}/{input}"
    )
    print(f"Offline command: {tr_cmd}")
    return tr_cmd


# online transcoding commands with generated files
@lru_cache(maxsize=None)
def online_tr(input):
    bitrate = get_bitrate("ffprobe", f"videos/{input}")
    resolution, framerate = get_video_stats("ffprobe", f"videos/{input}")
    if framerate > 30:
        target_bitrate = 3 * resolution
    else:
        target_bitrate = 2 * resolution
    target_bitrate = bitrate / 2 if target_bitrate > bitrate / 2 else target_bitrate

    if (resolution / 1000) > 4000:
        preset = "p1"  # fastest (lowest quality)
    elif (resolution / 1000) > 1000:
        preset = "p2"  # faster (lower quality)
    else:
        preset = "p3"  # fast (low quality)

    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -i /videos/{input} -c:v h264_nvenc -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
        + f"-preset {preset} -tune ull -y /videos/{online_output}/{input}"
    )
    print(f"Online command: {tr_cmd}")
    return tr_cmd


def run_tr(input, offline, show_cmd=False):
    if show_cmd:
        if offline:
            print(offline_tr(input))
        else:
            print(online_tr(input))
        return
    # idle mode power
    idle_metrics = []
    for _ in range(50):
        p = subprocess.check_output(nvidia_smi_cmd, shell=True)
        idle_metrics.append(p)
        time.sleep(0.2)

    # work mode power
    work_metrics = []
    work_logs = []
    global finish_tr  # used as an indicator to terminate power log thread
    finish_tr = False
    if offline:
        pool.submit(log_power, work_metrics)
        # run 10 times to eliminate power error
        for _ in range(10):
            work = subprocess.check_output(
                f"{offline_tr(input)}",
                shell=True,
                stderr=subprocess.STDOUT,
            )
            work_logs.append(work)
        finish_tr = True
    else:
        pool.submit(log_power, work_metrics)
        # only need to get transcoding outputs
        work = subprocess.check_output(
            f"{online_tr(input)}",
            shell=True,
            stderr=subprocess.STDOUT,
        )
        work_logs.append(work)
        finish_tr = True

    if offline:
        log_path = f"{normal_logs}/offline/"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log = os.path.join(log_path, f"{input}.log")
        with open(log, "w") as f:
            # metrics = ["3.11 W", "4.22 W", ...] in bytes
            # first decode and convert power to float
            idle_powers = [float(p.decode("utf-8").split()[0]) for p in idle_metrics]
            avg_idle_power = np.mean(idle_powers)
            idle_powers = [str(p) for p in idle_powers]
            f.write(" ".join(idle_powers) + "\n")
            f.write(f"idle avg power: {avg_idle_power}\n")

            work_powers = [float(p.decode("utf-8").split()[0]) for p in work_metrics]
            avg_work_power = np.mean(work_powers)
            work_powers = [str(p) for p in work_powers]
            f.write(" ".join(work_powers) + "\n")
            f.write(f"work avg power: {avg_work_power}\n")

            idle_metrics = [m.decode("utf-8") for m in idle_metrics]
            work_metrics = [m.decode("utf-8") for m in work_metrics]
            print(f"getting {len(work_metrics)} work powers")
            f.write("\n" + "Idle metrics" + "\n")
            f.writelines(idle_metrics)
            f.write("\n" + "Work metrics" + "\n")
            f.writelines(work_metrics)

            for work in work_logs:
                f.write(work.decode("utf-8") + "\n")


# infinite online transcoding
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
        preset = "p1"  # fastest (lowest quality)
    elif (resolution / 1000) > 1000:
        preset = "p2"  # faster (lower quality)
    else:
        preset = "p3"  # fast (low quality)

    tr_cmd = (
        "docker exec -i ffmpeg_exp "
        + f"ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_{input} -c:v h264_nvenc -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
        + f"-preset {preset} -tune ull -f null -"
    )

    # print(f"Online command: {tr_cmd}")
    return tr_cmd


def log_power_dmon(output):
    cmd = f"nvidia-smi dmon --id {GPU_INDEX} -d 1 -f {output}"
    p = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p


def restart_docker():
    subprocess.check_output("docker restart ffmpeg_exp", shell=True)


def test_power_eff_with_stream_num(input, num_streams):
    idlep = log_power_dmon(f"{power_eff_logs}/{num_streams}_{input}_idle.log")
    time.sleep(30)
    idlep.terminate()

    threads = []
    pp = log_power_dmon(f"{power_eff_logs}/{num_streams}_{input}.log")
    for _ in range(num_streams):
        p = subprocess.Popen(
            online_tr_infinite(input).split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        threads.append(p)
    # testing online streams for 60 seconds
    time.sleep(60)
    pp.terminate()
    restart_docker()


def concat_videos_100_times(input):
    concat_cmd = f"docker exec -i ffmpeg_exp ffmpeg -stream_loop 100 -i /videos/{input} -c:v copy -y /videos/inf_{input}"
    subprocess.check_output(concat_cmd, shell=True)
    print(f"Generating infinite video file videos/inf_{input}")


def test_gpu_power_eff():
    if not os.path.exists(power_eff_logs):
        os.makedirs(power_eff_logs)
    streams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20]
    for s in streams:
        for v in get_videos():
            if "hall" not in v and "pre" not in v:
                continue
            print(f"Current video: {v}, stream_num: {s}")
            test_power_eff_with_stream_num(input=v, num_streams=s)
            print(f"Finish testing {v} with {s} streams")
            time.sleep(90)  # interval between videos: 90 seconds


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # get online transcoding command
        if sys.argv[1] == "cmd":
            for v in get_videos():
                run_tr(v, offline=False, show_cmd=True)
            sys.exit("finish printing gpu cmd")

        # concat videos 100 times
        if sys.argv[1] == "concat":
            for v in get_videos():
                concat_videos_100_times(v)
            sys.exit("finish repeating and concating videos")

        # online transcoding power efficiency
        elif sys.argv[1] == "power-eff":
            test_gpu_power_eff()
            parse_power_eff(power_eff_logs)
            sys.exit("finish power efficiency experiments")

        # testing offline transcoding
        elif sys.argv[1] == "offline":
            path = f"videos/{offline_output}/"
            if not os.path.exists(path):
                os.makedirs(path)

            for v in get_videos():
                run_tr(v, offline=True)
                time.sleep(120)

            parse_throughput(normal_logs, "offline", 1)
            sys.exit("finish offline transcoding")

        # only used for generating online transcoding videos
        elif sys.argv[1] == "online":
            path = f"videos/{online_output}/"
            if not os.path.exists(path):
                os.makedirs(path)

            for v in get_videos():
                run_tr(v, offline=False)
            sys.exit("finish online transcoding")
