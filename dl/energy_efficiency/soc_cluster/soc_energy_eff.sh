#!/bin/bash

resnet_soc=(1 5 10 20 30)
resnet_bs=(1 2 4 8 16 24)
resnet_delay=(0.958 0.938 0.907 0.847 0.719 0.595)
for soc_num in ${resnet_soc[@]}
do
  bb exec -i -n $soc_num -e -o "workload_result/resnet_gpu_soc${soc_num}_bs1_energy.log" -c "/data/local/tmp/benchmark_model --graph=/data/local/tmp/my_resnet_v1_50.tflite --use_gpu=true --num_threads=4 --run_delay=${resnet_delay[0]} --input_layer=input --input_layer_shape=1,224,224,3 > /data/local/tmp/workload_result/resnet_gpu_soc${soc_num}_bs1.log"
  bb collect_result -f /data/local/tmp/workload_result/resnet_gpu_soc${soc_num}_bs1.log
  sleep 30
done
for (( i=0; i < ${#resnet_bs[@]}; i++ ))
do
  bb exec -i -e -o "workload_result/resnet_gpu_soc60_bs${resnet_bs[i]}_energy.log" -c "/data/local/tmp/benchmark_model --graph=/data/local/tmp/my_resnet_v1_50.tflite --use_gpu=true --num_threads=4 --run_delay=${resnet_delay[i]} --input_layer=input --input_layer_shape=${resnet_bs[i]},224,224,3 > /data/local/tmp/workload_result/resnet_gpu_soc60_bs${resnet_bs[i]}.log"
  bb collect_result -f /data/local/tmp/workload_result/resnet_gpu_soc60_bs${resnet_bs[i]}.log
  sleep 30
done

yolo_soc=(1 2 3 4 5 10 15 20 30 40 50 60)
yolo_delay=4
for soc_num in ${yolo_soc[@]}
do
  bb exec -i -n $soc_num -e -o "workload_result/mnn_gpu_soc${soc_num}_bs1_energy.log" -c "/data/local/tmp/run_mnn.sh ${yolo_delay} 10 /data/local/tmp/energy_eff_result/mnn_gpu_soc${soc_num}_bs1.log"
  bb collect_result -f /data/local/tmp/energy_eff_result/mnn_gpu_soc${soc_num}_bs1.log
  sleep 30
  bb exec -i -n $soc_num -e -o "workload_result/yolo_gpu_soc${soc_num}_bs1_energy.log" -c "/data/local/tmp/run_yolo.sh ${yolo_delay} 10 /data/local/tmp/energy_eff_result/yolo_gpu_soc${soc_num}_bs1.log"
  bb collect_result -f /data/local/tmp/energy_eff_result/yolo_gpu_soc${soc_num}_bs1.log
  sleep 30
done