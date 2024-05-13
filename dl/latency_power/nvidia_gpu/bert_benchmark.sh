#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters"
    exit
fi

batchSize=$1
outFile=/workspace/bert_result/bert_v100_${batchSize}_energy.txt
resultFile=/workspace/bert_result/bert_v100_${batchSize}.txt
intvl="0.02s"
times=300

export CUDA_VISIBLE_DEVICES=0

if [ "$#" -ne 2 ]; then
	python /workspace/tensorrt/demo/BERT/builder.py -m /workspace/tensorrt/demo/BERT/models/fine-tuned/bert_tf_ckpt_base_qa_squad2_amp_128/model.ckpt -o /workspace/tensorrt/demo/BERT/engines/bert_base_128.engine -s 128 -c /workspace/tensorrt/demo/BERT/models/fine-tuned/bert_tf_ckpt_base_qa_squad2_amp_128 -b $batchSize
else
	python /workspace/tensorrt/demo/BERT/builder.py -m /workspace/tensorrt/demo/BERT/models/fine-tuned/bert_tf_ckpt_base_qa_squad2_amp_128/model.ckpt -o /workspace/tensorrt/demo/BERT/engines/bert_base_128.engine -s 128 -c /workspace/tensorrt/demo/BERT/models/fine-tuned/bert_tf_ckpt_base_qa_squad2_amp_128 -v /workspace/tensorrt/demo/BERT/models/fine-tuned/bert_tf_ckpt_base_qa_squad2_amp_128/vocab.txt --int8 -b $batchSize
	outFile=/workspace/bert_result/bert_v100_int8_${batchSize}_energy.txt
	resultFile=/workspace/bert_result/bert_v100_int8_${batchSize}.txt
fi

while(( $times>0 ))
do
  python3 /workspace/nvidia_power.py >> $outFile
  sleep $intvl
  let "times--"
done

echo "start!!!"
echo "------------Prepare Stats-------------" >> $outFile

rm -f channel
touch channel
(
	python /workspace/tensorrt/demo/BERT/perf.py -e /workspace/tensorrt/demo/BERT/engines/bert_base_128.engine -b $batchSize -s 128 -i 1000 > $resultFile
	echo "finish" >> channel
)&

echo "------------Work Stats-------------" >> $outFile
while [ $(cat channel | grep -c "finish") -lt 1 ]
do
  python3 /workspace/nvidia_power.py >> $outFile
  sleep $intvl
done

wait
rm -f channel
echo "finish!!!"
