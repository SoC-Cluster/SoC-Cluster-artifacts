#!/bin/sh

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
	echo "Usage: run_yolo.sh <run time for 1 ite> <ites> <output:filename>"
	echo "Example: run_yolo.sh 4 10 "
    exit
fi

runTime=$1
ites=$2
log_file=$3
export LD_LIBRARY_PATH=/data/local/tmp/
mkdir -p /data/local/tmp/MNN_Models
rm -rf /data/local/tmp/MNN_Models/*
cp /data/local/tmp/yolov5x.mnn /data/local/tmp/MNN_Models/
command="/data/local/tmp/benchmark.out /data/local/tmp/MNN_Models 1 0 7 8"
cnt=0
while [ $cnt -lt $ites ]
do
    echo $cnt
    onetime=`(time ($command 2>&1) >> $log_file) 2>&1 | cut -d's' -f1`
	sec=`echo $onetime | cut -d'm' -f2`
    sleepTime=`echo "$runTime - $sec" | bc`
	echo $cnt" sleep "$sleepTime
    cnt=`expr $cnt + 1`
    if [ "${sleepTime:0:1}"x != "-"x ]
    then
        sleep $sleepTime
    fi
done
echo "Done"
