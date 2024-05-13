# DL inference on SoC-Cluster

## Pre-requirements

We use [bb](https://github.com/dxxhjk/bb) to scheduling DL inference tasks to multiple SoCs.

## Setup

Upload all exec scripts, models, and benchmark binary to SoC Cluster

   ```
   bb distribute_file -f soc_inference.sh -d /data/local/tmp/
   bb exec -c "chmod 777 /data/local/tmp/soc_inference.sh"

   bb distribute_file -f models/soc_resnet50/resnet50.tflite -d /data/local/tmp/
   bb distribute_file -f models/soc_resnet50/resnet50_quant.tflite -d /data/local/tmp/
   bb distribute_file -f models/soc_resnet152/resnet152.tflite -d /data/local/tmp/
   bb distribute_file -f models/soc_resnet152/resnet152_quant.tflite -d /data/local/tmp/
   bb distribute_file -f models/soc_bert/bert.tflite -d /data/local/tmp/
   bb distribute_file -f models/soc_yolov5x/yolov5x.mnn -d /data/local/tmp/

   bb distribute_file -f libs/* -d /data/local/tmp/
   ```

## Execution

Execute the following script on the host machine.

```
./soc_work.sh
```

## Results collection/processing

Results are automatically collected and saved in `path_to_bb/result/`, where each folder contain the execution result from one SoC.

Power consumption logs need to be manually collected from BMC:

```
scp -r bmc:/root/result .
```

Two steps to process results:

1. Get the latency

```
# resnet50、resent152、bert
python3 process_soc_result.py tfl {model}_{device}_{batchsize}.log path_to_bb
# yolov5x
python3 process_soc_result.py mnn {model}_{device}_{batchsize}.log path_to_bb
```

2. Get the power consumption

```
python3 process_soc_energy_result.py {model}_{device}_{batchsize}_energy.log
```