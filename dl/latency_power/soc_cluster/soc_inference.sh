#!/bin/sh

if [ "$#" -ne 3 ]; then
  echo "Illegal number of parameters"
	echo "Usage: soc_inference.sh <model_name: resnet50/resnet152/bert/yolov5x> <device: CPU/GPU/DSP> <batch_size>"
	echo "Example: soc_inference.sh resnet152 GPU 16"
  exit
fi

model_name=$1
device=$2
batch_size=$3
output_name=/data/local/tmp/${model_name}_${device}_${batch_size}.log
export LD_LIBRARY_PATH=/data/local/tmp/
mkdir -p /data/local/tmp/MNN_Models
echo $model_name
echo "start!!!"
if [ $model_name = "yolov5x" ]; then
	echo "MNN"
	rm -rf /data/local/tmp/MNN_Models/*
	cp /data/local/tmp/${model_name}.mnn /data/local/tmp/MNN_Models/
	if [ $device = "CPU" ]; then
		echo "CPU"
		dev="0"
	elif [ $device = "GPU" ]; then
		echo "GPU"
		dev="7"
	else
    echo "Illegal number of parameters"
    echo "Usage: soc_inference.sh <model_name: resnet50/resnet152/bert/yolov5x> <device: CPU/GPU/DSP> <batch_size>"
    echo "Example: soc_inference.sh resnet152 GPU 16"
    exit
	fi
  /data/local/tmp/benchmark.out /data/local/tmp/MNN_Models 100 5 ${dev} 4 >$output_name 2>&1
elif [ $model_name = "resnet50" ] || [ $model_name = "resnet152" ]; then
	echo "TFL"
	if [ $device = "CPU" ]; then
		echo "CPU"
		dev=""
	elif [ $device = "GPU" ]; then
		echo "GPU"
		dev="--use_gpu=true"
	elif [ $device = "DSP" ]; then
		echo "GPU"
		dev="--use_hexagon=true --hexagon_profiling=true"
		fileName=${fileName}_quant
	else
    echo "Illegal number of parameters"
    echo "Usage: soc_inference.sh <model_name: resnet50/resnet152/bert/yolov5x> <device: CPU/GPU/DSP> <batch_size>"
    echo "Example: soc_inference.sh resnet152 GPU 16"
    exit
	fi
	/data/local/tmp/benchmark_model --graph=/data/local/tmp/${model_name}.tflite  --num_threads=4 --input_layer=input --input_layer_shape=${batch_size},224,224,3 ${dev} >$output_name 2>&1
elif [ $model_name = "bert" ]; then
	echo "TFL"
	if [ $device = "CPU" ]; then
		echo "CPU"
		dev=""
	else
    echo "Illegal number of parameters"
    echo "Usage: soc_inference.sh <model_name: resnet50/resnet152/bert/yolov5x> <device: CPU/GPU/DSP> <batch_size>"
    echo "Example: soc_inference.sh bert CPU 1"
    exit
	fi
	/data/local/tmp/benchmark_model --graph=/data/local/tmp/${fileName}.tflite --num_threads=4 >${output_name} 2>&1
else
  echo "Illegal number of parameters"
  echo "Usage: soc_inference.sh <model_name: resnet50/resnet152/bert/yolov5x> <device: CPU/GPU/DSP> <batch_size>"
  echo "Example: soc_inference.sh resnet152 GPU 16"
  exit
fi
echo "Done"