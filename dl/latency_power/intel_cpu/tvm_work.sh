#!/bin/bash

idle="sudo turbostat --Summary --quiet --show PkgWatt docker exec $1 sleep 30 "
mkdir tvm_result
cores=(8 16 32 80)
# shellcheck disable=SC2068
for core in ${cores[@]}
do
    # shellcheck disable=SC2046
    docker update $1 --cpuset-cpus 0-`expr $core - 1`
    bss=(1)
    for bs in ${bss[@]}
    do
        sleep 60
        echo "model:bert, bs:$bs, core:$core, core-1:`expr $core - 1`"
        bert_out_file="tvm_result/bert_cpu_bs${bs}_core${core}.log"
        bert_command="sudo turbostat --Summary --quiet --show PkgWatt docker exec $1 /bin/bash -c \"/workspace/tensorflow/bazel-bin/tensorflow/tools/benchmark/benchmark_model --graph=\\\"/workspace/cpu_bert.pb\\\" --input_layer=\\\"input_ids,input_mask\\\" --input_layer_shape=\\\"1,128:1,128\\\" --output_layer=\\\"loss/Softmax\\\" --input_layer_type=\\\"int32,int32\\\" --num_threads=4 --show_run_order=false --show_time=false --show_type=false  --warmup_runs=100 --max_num_runs=16000 --max_time=\\\"30.0\\\"\""
        (eval $idle 2>&1) >> $bert_out_file
        (eval $bert_command 2>&1) >> $bert_out_file
        (eval $idle 2>&1) >> $bert_out_file
        models=(resnet50 resnet152 yolov5x)
        for model in ${models[@]}
        do
          sleep 60
          echo "model:$model, bs:$bs, core:$core, core-1:`expr $core - 1`"
          out_file="tvm_result/${model}_cpu_bs${bs}_core${core}.log"
          command="sudo turbostat --Summary --quiet --show PkgWatt docker exec $1 python -mtvm.driver.tvmc run --print-time --repeat 500 /workspace/${model}.tar"
          (eval $idle 2>&1) >> $out_file
          (eval $command 2>&1) >> $out_file
          (eval $idle 2>&1) >> $out_file
        done
    done
done