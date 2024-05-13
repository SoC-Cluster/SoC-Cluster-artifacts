#!/bin/bash

if [[ ! -z "$GPU_INDEX" ]]; then  
    echo "Use GPU: $GPU_INDEX"
else  
    GPU_INDEX=0
    echo "Use default GPU_INDEX: $GPU_INDEX"
    echo "Ignore this message if you are benchmarking video transcoding performance on CPU."
fi  

docker stop ffmpeg_exp && docker run --gpus all --env CUDA_VISIBLE_DEVICES=$GPU_INDEX --rm -t -d -v $(pwd)/videos:/videos --name ffmpeg_exp piaoliangkb/ffmpeg:nvidia-4.4 bash

