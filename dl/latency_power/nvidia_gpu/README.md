# DL inference on NVIDIA GPU

## Setup

1. Creating a Docker container with TensorRT v8.2.1.

2. Prepare the models

   - Upload models to the built Docker container by replacing the [container_id]

   ```
   docker cp models/cpu_bert/bert.pb [container_id]:/workspace/cpu_bert.pb
   docker cp models/cpu_yolov5x/yolov5x.onnx [container_id]:/workspace/cpu_yolov5x.onnx
   docker cp models/cpu_resnet50/resnet50.tflite [container_id]:/workspace/cpu_resnet50.tflite
   docker cp models/cpu_resnet152/resnet152.tflite [container_id]:/workspace/cpu_resnet152.tflite
   ```

   - Upload exec scripts

   ```shell
   docker cp ../../nvidia_power.py [container_id]:/workspace
   docker cp bert_benchmark.sh [container_id]:/workspace
   docker cp yolov5x_benchmark.sh [container_id]:/workspace
   docker cp resnet50_benchmark.sh [container_id]:/workspace
   docker cp resnet152_benchmark.sh [container_id]:/workspace
   docker cp trt_work.sh [container_id]:/workspace
   ```

## Exec

Execute the following script inside the Docker container.

```shell
./trt_work.sh
```

## Results collection/processing

Results are saved in folders named `resnet50`, `resnet152`, `yolov5x`, `bert`.
In each folder, there are files named `model_gpu_(int8)_batchsize.txt` and `model_gpu_(int8)_batchsize_energy.txt` that log inference latency, throughput and power consumption.

To get the average power consumption, use the following commands:

```
python3 process_nvidia_power.py resnet50_a100_1_energy.txt
```