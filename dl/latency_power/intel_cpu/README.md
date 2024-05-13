# DL inference on Intel CPU

## Setup

1. Using the Ubuntu 18.04 Docker image to create an Docker container, and builds [TVM v0.9.dev0](https://github.com/apache/tvm/releases/tag/v0.9.dev0).

2. Compile the [TensorFlow benchmark tool](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/benchmark).

3. Prepare the models

   - Upload models to the built Docker container by replacing the [container_id]

   ```
   docker cp models/cpu_bert/bert.pb [container_id]:/workspace/cpu_bert.pb
   docker cp models/cpu_yolov5x/yolov5x.onnx [container_id]:/workspace/cpu_yolov5x.onnx
   docker cp models/cpu_resnet50/resnet50.tflite [container_id]:/workspace/cpu_resnet50.tflite
   docker cp models/cpu_resnet152/resnet152.tflite [container_id]:/workspace/cpu_resnet152.tflite
   ```

   - Tune and compile the models using TVM

   ```
   python -mtvm.driver.tvmc tune --target "llvm -mcpu=cascadelake" --desired-layout NCHW --output cascadelake_resnet50.json cpu_resnet50.tflite
   python -mtvm.driver.tvmc compile --target "llvm -mcpu=cascadelake" --desired-layout NCHW --tuning cascadelake_resnet50.json --output resnet50.tar cpu_resnet50.tflite

   python -mtvm.driver.tvmc tune --target "llvm -mcpu=cascadelake" --desired-layout NCHW --output cascadelake_resnet152.json cpu_resnet152.tflite
   python -mtvm.driver.tvmc compile --target "llvm -mcpu=cascadelake" --desired-layout NCHW --tuning cascadelake_resnet152.json --output resnet152.tar cpu_resnet152.tflite

   python -mtvm.driver.tvmc tune --target "llvm -mcpu=cascadelake" --desired-layout NCHW --output cascadelake_yolov5xonnx.json cpu_yolov5x.onnx
   python -mtvm.driver.tvmc compile --target "llvm -mcpu=cascadelake" --desired-layout NCHW --tuning cascadelake_yolov5xonnx.json --output yolov5x.tar cpu_yolov5x.onnx
   ```

## Exec

On the host machine, execute the `tvm_work.sh` script by passing the [container_id] as the parameter.

```shell
./tvm_work.sh [container_id]
```

To run the BERT model using TensorFlow benchmark tool, using the following commands:

```
tensorflow/bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph="bert/bert.pb" --input_layer="input_ids,input_mask" --input_layer_shape="1,128:1,128" --output_layer="loss/Softmax" --input_layer_type="int32,int32" --show_run_order=false --show_time=false --show_type=false  --warmup_runs=100 --max_num_runs=16000 --max_time="30.0"
```

## Results collection/processing

All results are placed under in the `tvm_result` folder on the host machine.
Checkout files named `model_device_batchsize_core.log` to see inference latency, throughput, and power consumption.