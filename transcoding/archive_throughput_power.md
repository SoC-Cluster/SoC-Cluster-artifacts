# Throughput/Power - Archive Transcoding

## Intel CPU

### Setup

Start docker container:

```
bash pre_start_docker.sh
```

Remember to stop container after benchmark:

```
docker stop ffmpeg_exp
```

### Exec

```
python3 intel_cpu.py offline
```

Output logs: `cpulogs/offline/`

Output videos: `videos/cpu_output_offline/`

## NVIDIA GPU

### Setup

1. Set `GPU_INDEX` environment variable to the GPU index you will use in this benchmark.
GPU index can be seen from `nvidia-smi` command. For example:

```
export GPU_INDEX=4
```

2. Start docker container:

```
bash pre_start_docker.sh
```

3. Remember to stop container after benchmark:

```
docker stop ffmpeg_exp
```

### Exec

Offline transcoding on NVIDIA GPU will repeat the transcoding process 10 times to get accurate power consumption.

```
python3 nvidia_gpu.py offline
```

Output logs: `gpulogs/offline/`


## SoC-Cluster

### Setup

Push all videos and ffmpeg binary to SoC-Cluster:

```
python3 soc_cpu.py pre
```

### Exec

1. First, we need to disable all LITTLE cores to get the best archive transcoding performance:

```
python3 soc_cpu.py disable
```

2. Run offline transcoding:

```
python3 soc_cpu.py offline
```

3. Re-enable all LITTLE cores:

```
python3 soc_cpu.py enable
```