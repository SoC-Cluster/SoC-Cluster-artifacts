This folder contains two benchmarks scripts for assessing the latency, power consumption, and energy efficiency under dynamic workloads in deep learning inference tasks.

This deep learning inference benchmark involves (1) Intel CPU; (2) NVIDIA GPU (A40, A100); and (3) SoC Cluster (SoC CPU/GPU/DSP), and four models (1) ResNet-50; (2) ResNet-152; (3) YOLOv5x; and (4) BERT.
We also test int-8 quantized ResNet-50 and ResNet-152 models.


## Structure

- latency_power/: benchmark scripts for latency & power consumption in deep learning inference

    - intel_cpu/: script for running DL inference using TVM on Intel CPU

    - nvidia_gpu/: script for running DL inference using TensorRT

    - soc_cluster/: scripts for running DL inference on SoC CPU/GPU/DSP

- energy_efficiency/: benchmark scripts for measuring energy efficiency with dynamic input loads on [SoC GPU](./energy_efficiency/soc_cluster/) and [NVIDIA A100 GPU](./energy_efficiency/nvidia_gpu/) on two models: ResNet-50 and YOLOv5x.

- Other three Python utilization scripts for processing collected logs (more details in subfolders of each benchmark).