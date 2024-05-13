# Video Transcoding Quality

This benchmark is specific for live streaming video transcoding with bitrate constraint.

## Intel CPU

### Setup

Start the docker container

```
bash pre_start_docker.sh
```

### Exec

We need to save the output videos in live streaming transcoding.

1. Run live streaming transcoding commands to generate videos:

```
python3 intel_cpu.py online
```

Output videos: `videos/cpu_output_online/`

2. Compare PSNR:

```
python3 compare_psnr.py cpu
```

## NVIDIA GPU

### Setup

1. Set `GPU_INDEX` environment variable to the GPU index you will use in this benchmark.
GPU index can be seen from `nvidia-smi` command.
For example:

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

1. Run live streaming transcoding to generate videos:

```
python3 nvidia_gpu.py online
```

2. Compare PSNR:

```
python3 compare_psnr.py gpu
```

## SoC-Cluster

### Setup

Push all videos and ffmpeg binary to SoC-Cluster:

```
python3 soc_cpu.py pre
```

### Exec

On SoC-CPU:

1. Live streaming transcoding commands:

```
python3 soc_cpu.py online
```

2. Compare PSNR:

```
python3 compare_psnr.py soc_cpu
```

On SoC-HW (MediaCodec):

See our docs for [video bitrate comparison](./video_bitrate.md) to generate videos using the LiTr application.
