# SoC Cluster Benchmark

This repository contains a collection of scripts/tools for measuring the performance of two typical edge applications: video transcoding and deep learning inference on SoC Clusters and traditional Intel-CPU/NVIDIA GPU server.

For artifact evaluation, checkout [exp/](./exp/) for raw data, post-processed data, and scripts for drawing all figures in our paper.

## Resources

All binaries/models/videos can be downloaded through [Google Drive](https://drive.google.com/drive/folders/1B3vnQUeN1rniQCeaH6CIuf1zYi2d4Z1B?usp=sharing).

Related Docker image:

- `piaoliangkb/ffmpeg:nvidia-4.4`

## Description

### Deep Learning Inference

Models: ResNet-50, ResNet-152, YOLOv5x, BERT

Software: TVM/TensorFlow (Intel CPU), TensorRT (NVIDIA GPU), TFLite/MNN (SoC CPU/GPU/DSP)

### Video Transcoding

We selected 6 video from [vbench](http://arcade.cs.columbia.edu/vbench/) in the video transcoding benchmark.

Subtasks:

- Live streaming transcoding

- Archive transcoding

Software:

- Intel CPU / NVIDIA GPU: FFmpeg (with libx264/NVENC/NVDEC support)

- SoC Cluster: cross-compiled FFmpeg for Android with libx264 support / [LiTr](https://github.com/linkedin/LiTr) (developed by LinkedIn)

### SoC Performance Evolution

Two tasks:

- Live streaming transcoding

    - Hardware: SoC CPU, SoC Hardware Codec

- Deep learning inference

    - Models: ResNet-50, YOLOv5x

    - Hardware: SoC CPU/GPU/DSP

Tests were performed on 6 Snapdragon SoC models released within 2017 - 2022, containing Qualcomm Snapdragon 835, 845, 855, 865, 888, and 8+ Gen 1.