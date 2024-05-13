#!/bin/bash

bss=(1 4)
# shellcheck disable=SC2068
for bs in ${bss[@]}
do
  devices=(cpu gpu dsp)
  for device in ${devices[@]}
  do
    bb exec -e -o "/root/result/resnet50_${device}_${bs}_energy.log" -c "/data/local/tmp/soc_inference.sh resnet50 $device $bs"
    bb collect_result -f /data/local/tmp/resnet50_${device}_${bs}.log
    sleep 30
    bb exec -e -o "/root/result/resnet152_${device}_${bs}_energy.log" -c "/data/local/tmp/soc_inference.sh resnet152 $device $bs"
    bb collect_result -f /data/local/tmp/resnet152_${device}_${bs}.log
    sleep 30
  done
  devices=(cpu gpu)
  for device in ${devices[@]}
  do
    bb exec -e -o "/root/result/yolov5x_${device}_${bs}_energy.log" -c "/data/local/tmp/soc_inference.sh yolov5x $device $bs"
    bb collect_result -f /data/local/tmp/yolov5x_${device}_${bs}.log
    sleep 30
  done
  bb exec -e -o "/root/result/bert_cpu_${bs}_energy.log" -c "/data/local/tmp/soc_inference.sh bert cpu $bs"
  bb collect_result -f /data/local/tmp/bert_cpu_${bs}.log
done

