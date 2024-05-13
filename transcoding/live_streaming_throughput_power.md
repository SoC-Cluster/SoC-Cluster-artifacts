# Throughput/Power - Live Streaming Transcoding

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

To get the maximum stream number that Intel CPU can support, operator needs to start each transcoding process sequentially.
Operator should monitor the current ffmpeg process to identify whether the transcoding FPS meets the requirements (>= source video).
If so, start the next process else terminate the current process and log the number of ffmpeg processes.
Power consumption is logged using `turbostat`.

1. Setup command (modify the cpuset of docker container):

```
docker update ffmpeg_exp --cpuset-cpus="10-17"
```

2. FFmpeg commands:

```
# V1: holi
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/holi_854x480_30.mkv -c:v libx264 -threads 1 -b:v 819840 -maxrate 819840 -bufsize 819840 -preset veryfast -tune zerolatency -f null -

# V2: desktop
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/desktop_1280x720_30.mkv -c:v libx264 -threads 1 -b:v 90500.0 -maxrate 90500.0 -bufsize 90500.0 -preset veryfast -tune zerolatency -f null -

# V3: game3
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/game3_1280x720_59.mkv -c:v libx264 -threads 1 -b:v 2764800 -maxrate 2764800 -bufsize 2764800 -preset veryfast -tune zerolatency -f null -

# V4: presentation
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/presentation_1920x1080_25.mkv -c:v libx264 -threads 1 -b:v 215000.0 -maxrate 215000.0 -bufsize 215000.0 -preset superfast -tune zerolatency -f null -

# V5: hall
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/hall_1920x1080_29.mkv -c:v libx264 -threads 1 -b:v 4147200 -maxrate 4147200 -bufsize 4147200 -preset superfast -tune zerolatency -f null -

# V6: chicken
docker exec -i ffmpeg_exp ffmpeg -benchmark -re -stream_loop -1 -i /videos/chicken_3840x2160_30.mkv -c:v libx264 -threads 6 -b:v 16588800 -maxrate 16588800 -bufsize 16588800 -preset ultrafast -tune zerolatency -f null -
```

Monitor runtime power consumption:

```
turbostat --Summary --quiet --show PkgWatt,RAMWatt --interval 1 >> [video]_cpu_8_cores.log
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

3. Remember to stop container after benchmark:

```
docker stop ffmpeg_exp
```

### Exec

First, due to the lack of support of ffmpeg parameter `--stream_loop -1` on NVENC, we first need to repeat the same video 100 times and concat them into a whole.
Output videos will be in `videos/` with the `inf_` prefix. 

```
python3 nvidia_gpu.py concat
```

Use the following commands:

```
# V1: holi
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_holi_854x480_30.mkv -c:v h264_nvenc -b:v 819840 -maxrate 819840 -bufsize 819840 -preset p3 -tune ull -f null -

# V2: desktop
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_desktop_1280x720_30.mkv -c:v h264_nvenc -b:v 90500.0 -maxrate 90500.0 -bufsize 90500.0 -preset p3 -tune ull -f null -

# V3: game3
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_game3_1280x720_59.mkv -c:v h264_nvenc -b:v 2764800 -maxrate 2764800 -bufsize 2764800 -preset p3 -tune ull -f null -

# V4: presentation
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_presentation_1920x1080_25.mkv -c:v h264_nvenc -b:v 215000.0 -maxrate 215000.0 -bufsize 215000.0 -preset p2 -tune ull -f null -

# V5: hall
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_hall_1920x1080_29.mkv -c:v h264_nvenc -b:v 4147200 -maxrate 4147200 -bufsize 4147200 -preset p2 -tune ull -f null -

# V6: chicken
docker exec -it ffmpeg_exp ffmpeg -loglevel verbose -benchmark -hwaccel cuda -hwaccel_output_format cuda -extra_hw_frames 5 -re -i /videos/inf_chicken_3840x2160_30.mkv -c:v h264_nvenc -b:v 16588800 -maxrate 16588800 -bufsize 16588800 -preset p1 -tune ull -f null -
```

Monitor runtime power consumption:

```
nvidia-smi dmon --id $GPU_INDEX -d 1 -f [video]_gpu.log
```

## SoC-Cluster

### Setup

Push all videos and ffmpeg binary to SoC-Cluster:

```
python3 soc_cpu.py pre
```

### Exec

1. Connect to one of the SoCs in SOC-Cluster:

```
adb connect [ip]:[port]
```

2. Transcoding command on a single SoC in SoC-Cluster:

```
# V1: holi
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/holi_854x480_30.mkv -c:v libx264 -threads 1 -b:v 819840 -maxrate 819840 -bufsize 819840 -preset veryfast -tune zerolatency -f null -

# V2: desktop
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/desktop_1280x720_30.mkv -c:v libx264 -threads 1 -b:v 90500.0 -maxrate 90500.0 -bufsize 90500.0 -preset veryfast -tune zerolatency -f null -

# V3: game3
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/game3_1280x720_59.mkv -c:v libx264 -threads 1 -b:v 2764800 -maxrate 2764800 -bufsize 2764800 -preset veryfast -tune zerolatency -f null -

# V4: presentation
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/presentation_1920x1080_25.mkv -c:v libx264 -threads 1 -b:v 215000.0 -maxrate 215000.0 -bufsize 215000.0 -preset superfast -tune zerolatency -f null -

# V5: hall
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/hall_1920x1080_29.mkv -c:v libx264 -threads 1 -b:v 4147200 -maxrate 4147200 -bufsize 4147200 -preset superfast -tune zerolatency -f null -

# V6: chicken
adb shell /data/local/tmp/ffmpeg-x264 -benchmark -stream_loop -1 -re -i /data/local/tmp/videos/chicken_3840x2160_30.mkv -c:v libx264 -threads 8 -b:v 16588800 -maxrate 16588800 -bufsize 16588800 -preset ultrafast -tune zerolatency -f null -
```

Monitor SoC-Cluster's runtime power consumption: login to BMC and run the following command

```
while true; do
    pmbus get 1 | grep "DC 12V Output Power:"
done
```