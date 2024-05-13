#!/bin/bash

models=(resnet50 resnet152 yolov5x)
# shellcheck disable=SC2068
for model in ${models[@]}
do
  bss=(1 4 16 64)
  for bs in ${bss[@]}
  do
    command="/workspace/${model}_benchmark.sh ${bs}"
    quant_command="/workspace/${model}_benchmark.sh ${bs} int8"
    eval $command
    sleep 60
    eval $quant_command
    sleep 60
  done
done

cd /workspace/tensorrt/demo/BERT
bss=(1 4 16 64)
# shellcheck disable=SC2068
for bs in ${bss[@]}
do
  command="/workspace/bert_benchmark.sh ${bs}"
  quant_command="/workspace/bert_benchmark.sh ${bs} int8"
  eval $command
  sleep 60
  eval $quant_command
  sleep 60
done
