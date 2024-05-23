import os
import signal
import subprocess
import sys
import time

soc_phy = "192.168.1.180:5555"
soc_vir_host = "192.168.1.180:5555"
soc_vir_soc = "192.168.1.201:5555"
os.system(f"adb connect {soc_phy}")
os.system(f"adb connect {soc_vir_host}")
os.system(f"adb connect {soc_vir_soc}")


cpu_commands = {
    "resnet50_fp32": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet50.tflite --num_threads=4 --input_layer=input --input_layer_shape=1,224,224,3 --num_runs=500",
    "resnet152_fp32": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet152.tflite --num_threads=4 --input_layer=input --input_layer_shape=1,224,224,3 --num_runs=500",
    "yolov5x_fp32": "cd /data/local/tmp/ && LD_LIBRARY_PATH=/data/local/tmp/ ./benchmark.out /data/local/tmp/MNN_Models 100 0 0 4",
    "bert_fp32": "cd /data/local/tmp/ && ./benchmark_model --graph=bert.tflite --num_threads=4 --num_runs=500",
}

gpu_commands = {
    "resnet50_fp32": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet50.tflite --input_layer=input --input_layer_shape=1,224,224,3 --use_gpu=true --num_runs=500",
    "resnet152_fp32": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet152.tflite --input_layer=input --input_layer_shape=1,224,224,3 --use_gpu=true --num_runs=500",
    "yolov5x_fp32": "cd /data/local/tmp/ && LD_LIBRARY_PATH=/data/local/tmp/ ./benchmark.out /data/local/tmp/MNN_Models 100 0 7 4",
}

dsp_commands = {
    "resnet50_i8": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet50-quant.tflite --num_threads=4 --input_layer=input --input_layer_shape=1,224,224,3 --use_hexagon=true --hexagon_profiling=true --num_runs=1000",
    "resnet152_i8": "cd /data/local/tmp/ && ./benchmark_model --graph=resnet152-quant.tflite --num_threads=4 --input_layer=input --input_layer_shape=1,224,224,3 --use_hexagon=true --hexagon_profiling=true --num_runs=500 ",
}

def push_all_files():
    socs = [soc_phy, soc_vir_soc, soc_vir_host]
    for soc in socs:
        os.system(f"adb connect {soc}")
        os.system(f"adb -s {soc} push get_cpu_usage /data/local/tmp/")
        os.system(f"adb -s {soc} shell chmod +x /data/local/tmp/get_cpu_usage")

        for f in os.listdir("dl/binary/"):
            os.system(f"adb -s {soc} push {os.path.join('dl/binary/', f)} /data/local/tmp/")

        os.system(f"adb -s {soc} shell chmod +x /data/local/tmp/benchmark_model")
        os.system(f"adb -s {soc} shell chmod +x /data/local/tmp/benchmark.out")
        
        for f in os.listdir("dl/models/"):
            os.system(f"adb -s {soc} push {os.path.join('dl/models/', f)} /data/local/tmp/")

        os.system(f"adb -s {soc} shell mkdir -p /data/local/tmp/MNN_Models")
        os.system(f"adb -s {soc} shell mv /data/local/tmp/yolov5x.mnn /data/local/tmp/MNN_Models/")


def get_src_monitor_commands(soc: str, hw: str, model: str):
    return f"adb -s {soc} shell '/data/local/tmp/get_cpu_usage > /data/local/tmp/{hw}_{model}.usage'"

def get_pull_monitor_log_command(soc: str, hw: str, model: str):
    return f"adb -s {soc} pull /data/local/tmp/{hw}_{model}.usage ."

def get_exec_commands(soc: str, hw: str, model: str):
    """
    hw: [cpu, gpu, dps]
    model: [resnet50_fp32, resnet152_fp32, yolov5x_fp32, bert_fp32, resnet50_i8, resnet152_i8]
    """
    if hw == "cpu":
        command_dict = cpu_commands
    elif hw == "gpu":
        command_dict = gpu_commands
    elif hw == "dsp":
        command_dict = dsp_commands

    cmd = f"adb -s {soc} shell '{command_dict[model]}' 2>&1 > {hw}_{model}.latency"

    return cmd


def run_single_command(exec_cmd: str, monitor_cmd: str, pull_log_cmd: str):
    # start the infinite monitor cmd
    print(f"executing: {monitor_cmd}")
    monitor_process = subprocess.Popen(monitor_cmd, shell=True)

    # start the execution cmd
    print(f"executing: {exec_cmd}")
    exec_process = subprocess.Popen(exec_cmd, shell=True)
    exec_process.wait()

    # after the execution cmd finished, terminate the monitor cmd
    monitor_process.send_signal(signal.SIGTERM)
    monitor_process.wait()

    # pull the log file
    pull_process = subprocess.Popen(pull_log_cmd, shell=True)
    pull_process.wait()

    time.sleep(20)


def run_all_phy():
    hw = "cpu"
    models = ["resnet50_fp32", "resnet152_fp32", "bert_fp32", "yolov5x_fp32"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_phy, hw, model)
        exec_cmd = get_exec_commands(soc_phy, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    hw = "gpu"
    models = ["resnet50_fp32", "resnet152_fp32", "yolov5x_fp32"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_phy, hw, model)
        exec_cmd = get_exec_commands(soc_phy, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    hw = "dsp"
    models = ["resnet50_i8", "resnet152_i8"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_phy, hw, model)
        exec_cmd = get_exec_commands(soc_phy, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    if os.path.exists("phy"):
        os.rmdir("phy")
    os.mkdir("phy")
    for f in os.listdir("."):
        if f.endswith(".usage") or f.endswith(".latency"):
            os.rename(f, os.path.join("phy", f))


def run_all_vir():
    hw = "cpu"
    models = ["resnet50_fp32", "resnet152_fp32", "bert_fp32", "yolov5x_fp32"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_vir_host, hw, model)
        exec_cmd = get_exec_commands(soc_vir_soc, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    hw = "gpu"
    models = ["resnet50_fp32", "resnet152_fp32", "yolov5x_fp32"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_vir_host, hw, model)
        exec_cmd = get_exec_commands(soc_vir_soc, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    hw = "dsp"
    models = ["resnet50_i8", "resnet152_i8"]
    for model in models:
        monitor_cmd = get_src_monitor_commands(soc_vir_host, hw, model)
        exec_cmd = get_exec_commands(soc_vir_soc, hw, model)
        pull_log_cmd = get_pull_monitor_log_command(soc_phy, hw, model)
        run_single_command(exec_cmd, monitor_cmd, pull_log_cmd)

    if os.path.exists("vir"):
        os.rmdir("vir")
    os.mkdir("vir")
    for f in os.listdir("."):
        if f.endswith(".usage") or f.endswith(".latency"):
            os.rename(f, os.path.join("vir", f))


if __name__ == "__main__":
    if sys.argv[1] == 'push':
        push_all_files()
    elif sys.argv[1] == 'run':
        for soc in [soc_phy, soc_vir_host, soc_vir_soc]:
            os.system(f"adb connect {soc}")
        run_all_phy()
        run_all_vir()