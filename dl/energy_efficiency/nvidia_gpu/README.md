# Energy Efficiency Measurement on NVIDIA GPU

## Setup

1. Checkout the setup guide in [deep learning latency & power consumption measurement](../../latency_power/nvidia_gpu/README.md) to get the Docker container.

2. Upload scripts to Docker container by replacing the [container_id]:

```
docker cp eff_gpu.sh [container_id]:/workspace
```

## Execution

Execution the following scripts inside the Docker container.

```
./eff_gpu.sh
```

## Results collection/processing

Results are saved in the folder named `eff_gpu_result`.
Power consumption logs are named `{model}_{batchsize}_energy.log`.

To get the power consumption, use the following scripts:

```
python3 process_nvidia_power.py {model}_{batchsize}_energy.log
```