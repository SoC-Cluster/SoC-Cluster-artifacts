import os
import subprocess
import sys
import time
from functools import lru_cache

from utils import get_bitrate, get_video_stats, get_videos

local_log_folder = "soc-logs"
local_power_log_folder = "soc-power-logs"
device_cpu_log_folder = "/data/local/tmp/videos/cpu_output/logs/"
device_hw_log_folder = "/data/local/tmp/videos/mediacodec_output/logs/"
offline_output = "soc-cpu_output_offline"
online_output = "soc-cpu_output_online"


def pre_delete():
    subprocess.check_output('bb -i exec -c "rm -r /data/local/tmp/videos/"', shell=True)
    subprocess.check_output('bb -i exec -c "rm -r /data/local/tmp/ffmpeg*"', shell=True)


def pre_commands():
    """
    1. Push all videos to /data/local/tmp/videos/
    2. Push FFmpeg release executable to /data/local/tmp/
    3. Add executable permission to /data/local/tmp/ffmpeg
    4. Create output video dir /data/local/tmp/videos/cpu_output/, /data/local/tmp/videos/mediacodec_output/
    """
    subprocess.check_output(
        "bb -i distribute_file -f videos/ -d /data/local/tmp/", shell=True
    )
    subprocess.check_output(
        "bb -i distribute_file -f pre-built/ffmpeg-x264 -d /data/local/tmp/", shell=True
    )
    subprocess.check_output(
        'bb -i exec -c "chmod +x /data/local/tmp/ffmpeg-x264"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "mkdir -p {device_cpu_log_folder}"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "mkdir -p {device_hw_log_folder}"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "mkdir -p /data/local/tmp/videos/{offline_output}"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "mkdir -p /data/local/tmp/videos/{online_output}"', shell=True
    )


def pre_disable_little_cores():
    subprocess.check_output(
        f'bb -i exec -c "echo 0 > /sys/devices/system/cpu/cpu0/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 0 > /sys/devices/system/cpu/cpu1/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 0 > /sys/devices/system/cpu/cpu2/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 0 > /sys/devices/system/cpu/cpu3/online"', shell=True
    )


def after_enable_little_cores():
    subprocess.check_output(
        f'bb -i exec -c "echo 1 > /sys/devices/system/cpu/cpu0/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 1 > /sys/devices/system/cpu/cpu1/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 1 > /sys/devices/system/cpu/cpu2/online"', shell=True
    )
    subprocess.check_output(
        f'bb -i exec -c "echo 1 > /sys/devices/system/cpu/cpu3/online"', shell=True
    )


@lru_cache(maxsize=None)
def offline_tr(ffmpeg, input, codec, times):
    if codec == "h264":
        tr_cmd = (
            f"{ffmpeg} "
            + f" -benchmark -i /data/local/tmp/videos/{input} -c:v libx264 -crf 18 -preset veryslow -y /data/local/tmp/videos/{offline_output}/{input} "
            + f"2>&1 | tee -a {device_cpu_log_folder}/{times}_offline_{codec}_{input}.log"
        )

    # print(f"Offline command: {tr_cmd}")
    return tr_cmd


@lru_cache(maxsize=None)
def online_tr(ffmpeg, input, codec, times):
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

    if codec == "h264":
        tr_cmd = (
            f"{ffmpeg} "
            + f"-benchmark -i /data/local/tmp/videos/{input} -c:v libx264 -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
            + f"-preset {preset} -tune zerolatency -y /data/local/tmp/videos/{online_output}/{input} "
            + f"2>&1 | tee -a {device_cpu_log_folder}/{times}_online_{codec}_{input}.log"
        )

    # print(f"Online command: {tr_cmd}")
    return tr_cmd


def run_tr(ffmpeg, input, codec, offline, times=1, show_cmd=False):
    if offline:
        power_log_name = f"{times}_offline_{codec}_{input}"
        tr_cmd = offline_tr(ffmpeg, input, codec, times)
    else:
        power_log_name = f"{times}_online_{codec}_{input}"
        tr_cmd = online_tr(ffmpeg, input, codec, times)
    if show_cmd:
        print(tr_cmd + "\n")
        return
    # run ffmpeg command 10 times to eliminate power error
    bb_cmd = f'bb -i exec -o {power_log_name} -e -c "'
    for _ in range(10):
        bb_cmd += f"{tr_cmd}; "
    print("\n" + bb_cmd + "\n")
    subprocess.check_output(bb_cmd, shell=True)


def log_arm_power(output):
    cmd = f"bash log_arm_power.sh {output}"
    p = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return p


@lru_cache(maxsize=None)
def online_tr_infinite(ffmpeg, input, codec):
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

    if codec == "libx264":
        tr_cmd = (
            f"{ffmpeg} "
            + f"-benchmark -i /data/local/tmp/videos/inf_{input} -c:v libx264 -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate} "
            + f"-preset {preset} -tune zerolatency -f null -"
        )
    # print(f"Online command: {tr_cmd}")
    return tr_cmd


def test_power_eff(enc, log_folder):
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)
    soc_base = "192.168.1.1"
    for i in range(1, 9):
        ip = soc_base + str(0) + str(i) + ":5555"
        os.system(f"adb connect {ip}")
    for i in range(10, 61):
        ip = soc_base + str(i) + ":5555"
        os.system(f"adb connect {ip}")

    streams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20]
    for s in streams:
        for v in get_videos():
            if "hall" in v or "pre" in v:
                continue
            print(f"Current video: {v}, stream_num: {s}")

            print(f"Logging idle power ...")
            idlep = log_arm_power(f"{log_folder}/{s}_{v}_{enc}_idle.log")
            time.sleep(20)
            idlep.terminate()

            print(f"Logging transcoding power ...")
            # libx264 max supported streams on single SoC: pre=9, hall=3
            # SoC-range = [30-50]
            ffmpeg_cmd = online_tr_infinite("/data/local/tmp/ffmpeg-x264", v, enc)
            threads = []
            for i in range(s):
                soc_ip = soc_base + str(31 + i) + ":5555"
                cmd = f"adb -s {soc_ip} shell {ffmpeg_cmd}"
                print(cmd)
                p = subprocess.Popen(
                    cmd.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                threads.append(p)
            workp = log_arm_power(f"{log_folder}/{s}_{v}_{enc}.log")
            time.sleep(60)
            workp.terminate()
            [p.terminate() for p in threads]
            ffmpeg_log = os.path.join(log_folder, f"ffmpeg_{s}_{v}_{enc}.log")
            with open(ffmpeg_log, "w") as f:
                for p in threads:
                    p.terminate()
                    out, err = p.communicate()
                    f.write(out.decode("utf-8") + "\n")

            print(f"Finish working stage ...")
            time.sleep(60)


if __name__ == "__main__":
    #######################################################
    ####### upload all resources to soc-cluster
    #######################################################
    if len(sys.argv) == 2:
        if sys.argv[1] == "pre":
            pre_commands()
            sys.exit("finish pre process")
        elif sys.argv[1] == "disable":
            pre_disable_little_cores()
            sys.exit("disaling 4 little cores")
        elif sys.argv[1] == "enable":
            after_enable_little_cores()
            sys.exit("re-enabling 4 little cores")
        elif sys.argv[1] == "log":
            if not os.path.exists(local_log_folder):
                os.mkdir(local_log_folder)
            if not os.path.exists(local_power_log_folder):
                os.mkdir(local_power_log_folder)

            subprocess.check_output(
                f"bb -i collect_result -f {device_cpu_log_folder} -d {local_log_folder}",
                shell=True,
            )
            sys.exit("finish pulling logs")

        elif sys.argv[1] == "cmd":
            # extract command on single soc
            ffmpeg = "/data/local/tmp/ffmpeg"
            for video in get_videos():
                run_tr(ffmpeg, video, codec="h264", offline=True, show_cmd=True)
            sys.exit("finish printing commands")

        elif sys.argv[1] == "power-eff":
            test_power_eff("libx264", "power-eff-logs")
            sys.exit("finish testing power efficiency")

        elif sys.argv[1] == "offline":
            #######################################################
            ####### perf using bb
            #######################################################
            ffmpeg = "/data/local/tmp/ffmpeg-x264"
            sleep_sec = 60
            videos = get_videos()
            for times in range(1, 6):
                for video in videos:
                    run_tr(ffmpeg, video, codec="h264", offline=True, times=times)
                    time.sleep(sleep_sec)

            #######################################################
            ####### get back all logs and save to local using bb
            #######################################################
            if not os.path.exists(local_log_folder):
                os.mkdir(local_log_folder)
            if not os.path.exists(local_power_log_folder):
                os.mkdir(local_power_log_folder)

            subprocess.check_output(
                f"bb -i collect_result -f {device_cpu_log_folder} -d {local_log_folder}",
                shell=True,
            )
            sys.exit("finish offline transcoding")

        # save online transcoding outputs and pull to local
        elif sys.argv[1] == "online":
            ffmpeg = "/data/local/tmp/ffmpeg-x264"
            sleep_sec = 10
            videos = get_videos()
            for times in range(1, 6):
                for video in videos:
                    run_tr(ffmpeg, video, codec="h264", offline=False, times=times)
                    time.sleep(sleep_sec)

            subprocess.check_output(
                f"adb -s 192.168.1.101:5555 pull /data/local/tmp/videos/{online_output}/ videos/"
            )
            sys.exit("finish online transcoding")
