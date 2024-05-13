#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters"
    exit
fi

batchSize=$1
outFile=/workspace/resnet152_result/resnet152_v100_${batchSize}_energy.txt
resultFile=/workspace/resnet152_result/resnet152_v100_${batchSize}.txt
intvl="0.02s"
times=300

export CUDA_VISIBLE_DEVICES=0

if [ "$#" -eq 2 ]; then
	outFile=/workspace/resnet152_result/resnet152_v100_int8_${batchSize}_energy.txt
	resultFile=/workspace/resnet152_result/resnet152_v100_int8_${batchSize}.txt
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
touch $resultFile
(
	if [ "$#" -ne 2 ]; then
		trtexec --avgRuns=100 --deploy=/workspace/resnet152-v2/deploy_resnet152-v2.prototxt --batch=$batchSize --iterations=1000 --output=prob --useSpinWait 2> channel > $resultFile
	else
		trtexec --avgRuns=100 --deploy=/workspace/resnet152-v2/deploy_resnet152-v2.prototxt --batch=$batchSize --iterations=1000 --output=prob --useSpinWait --int8 2> channel > $resultFile
	fi
	echo "finish" >> channel
)&

while [ $(cat $resultFile | grep -c "Starting inference") -lt 1 ]
do
        sleep $intvl
done

cat $resultFile

echo "------------Work Stats-------------" >> $outFile
while [ $(cat channel | grep -c "finish") -lt 1 ]
do
        python3 /workspace/nvidia_power.py >> $outFile
        sleep $intvl
done

wait
rm -f channel
echo "finish!!!"
