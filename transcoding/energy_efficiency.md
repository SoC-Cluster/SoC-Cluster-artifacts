# Energy Efficiency

## Intel CPU

Run this benchmark for live streaming transcoding.
All videos will be repeatedly transcoded 10 times.

### Setup

Start the docker container:

```
bash pre_start_docker.sh
```

### Exec

```
python3 intel_cpu.py power-eff
```

Output logs: `cpu_power_eff_logs/`

## NVIDIA GPU

### Setup

1. Set `GPU_INDEX` environment variable to the GPU index you will use in this benchmark.
GPU index can be seen from `nvidia-smi` command. For example, use GPU with index=4:

```
export GPU_INDEX=4
```

2. Start docker container:

```
bash pre_start_docker.sh
```

3. Remember to terminate container after benchmark:

```
docker stop ffmpeg_exp
```

### Exec

```
python3 nvidia_gpu.py power-eff
```

Output logs: `gpu_power_eff_logs/`

## SoC-Cluster

### Setup

Push all videos and ffmpeg binary to SoC-Cluster:

```
python3 soc_cpu.py pre
```

### Exec

```
python3 soc_cpu.py power-eff
```