resnet_bs=(1 5 10 20 30 60 120 240 480 960 1440)
yolo_bs=(1 2 3 4 5 10 15 20 30 40 50 60)
resnet_idle=(999 998 997 994 993 987 975 951 912 827 740)
yolo_idle=(3991 3985 3980 3973 3968 3942 3911 3888 3832 3779 3724 3680)

mkdir eff_gpu_result
for (( i=1; i <= ${#resnet_bs[@]}; i++)); do
  resnet_filename=eff_gpu_result/resnet50_${resnet_bs[i]}.log
  resnet_energy_filename=eff_gpu_result/resnet50_${resnet_bs[i]}_energy.log
  intvl="0.02s"
  times=300
  export CUDA_VISIBLE_DEVICES=0
  while(( $times>0 ))
  do
          python3 /workspace/nvidia_power.py >> $resnet_energy_filename
          sleep $intvl
          let "times--"
  done
  echo "------------Prepare Stats-------------" >> $resnet_energy_filename

  rm -f channel
  touch channel
  touch $resnet_filename
  (
    trtexec --avgRuns=100 --deploy=/usr/local/tensorrt/data/resnet50/ResNet50_N2.prototxt --batch=${resnet_bs[i]} --idleTime=${resnet_idle[i]} --iterations=10 --output=prob --useSpinWait 2> channel > $resnet_filename
    echo "finish" >> channel
  )&
  while [ $(cat $resnet_filename | grep -c "Starting inference") -lt 1 ]
  do
    sleep $intvl
  done
  cat $resnet_filename
  echo "------------Work Stats-------------" >> $resnet_energy_filename
  while [ $(cat channel | grep -c "finish") -lt 1 ]
  do
    python3 /workspace/nvidia_power.py >> $resnet_energy_filename
    sleep $intvl
  done
  wait
  rm -f channel
done

for (( i=1; i <= ${#yolo_bs[@]}; i++)); do
  yolo_filename=eff_gpu_result/yolov5x_${yolo_bs[i]}.log
  yolo_energy_filename=eff_gpu_result/yolov5x_${yolo_bs[i]}_energy.log
  intvl="0.02s"
  times=300
  export CUDA_VISIBLE_DEVICES=0
  python /workspace/yolov5/export.py --weights /workspace/yolov5/models/yolov5x.pt --include torchscript onnx --batch-size=${yolo_bs[i]}
  while(( $times>0 ))
  do
          python3 /workspace/nvidia_power.py >> $yolo_energy_filename
          sleep $intvl
          let "times--"
  done
  echo "------------Prepare Stats-------------" >> $yolo_energy_filename

  rm -f channel
  touch channel
  touch $yolo_filename
  (
    trtexec --avgRuns=1 --onnx=/workspace/yolov5x/models/yolov5x.onnx --idleTime=${yolo_idle[i]} --iterations=10 --useSpinWait
    echo "finish" >> channel
  )&
  while [ $(cat $yolo_filename | grep -c "Starting inference") -lt 1 ]
  do
    sleep $intvl
  done
  cat $yolo_filename
  echo "------------Work Stats-------------" >> $yolo_energy_filename
  while [ $(cat channel | grep -c "finish") -lt 1 ]
  do
    python3 /workspace/nvidia_power.py >> $yolo_energy_filename
    sleep $intvl
  done
  wait
  rm -f channel
done