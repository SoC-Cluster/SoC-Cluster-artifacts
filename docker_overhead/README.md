# Docker Overhead on SoC Clusters

This experiment aims to measure the overhead of using Docker containers on SoC Clusters using deep learning inference.

## Setup

1. Compile binary to assess CPU usage, GPU busy percentage, and memory usage.

    Note: golang and Android NDK are required to be installed.

    ```
    go env -w GO111MODULE=off
    export ANDROID_NDK=/path/to/android_ndk
    ./build_go.sh get_cpu_usage.go
    ```

    Output: `get_cpu_usage` binary.

2. Push all required models and libraries to target SoCs. 

    - Follow the download guide in [README.md](../README.md) of the root folder.
    - Move the `dl/` folder in the current folder.
    - Configure SoCs in `test_dl.py`. For example,
        ```
        soc_phy = "192.168.1.180:5555"
        soc_vir_host = "192.168.1.180:5555"
        soc_vir_soc = "192.168.1.201:5555"
        ```
    - Call `python3 test_dl.py push` to push all scripts to SoCs.

## Exec

1. Run all experiments

    ```
    python3 test_dl.py run
    ```

2. Extract results

    ```
    python3 proc_usage.py vir/cpu_resnet50_fp32.usage vir/cpu_resnet152_fp32.usage/vir/cpu_yolov5x_fp32.usage vir/cpu_bert_fp32.usage

    # ...
    ```

    Extract latencies from raw logs: `vir/cpu_resnet50_fp32.latency`, ...



