# Energy Efficiency on SoC-Cluster

## Pre-requirements

We use [bb](https://github.com/dxxhjk/bb) to scheduling DL inference tasks to multiple SoCs.

## Setup

1. Checkout the setup guide in [deep learning latency & power consumption measurement](../../latency_power/soc_cluster/README.md) to upload all required files to SoC Cluster.

2. Upload scripts to SoC Cluster.

```
bb distribute_file -n 60 -f run_yolo.sh -d /data/local/tmp/
bb distribute_file -n 60 -f run_mnn.sh -d /data/local/tmp/
bb exec -c "chmod +x /data/local/tmp/run_mnn.sh"
bb exec -c "chmod +x /data/local/tmp/run_yolo.sh"
```

## Execution

Execute the following command on the host machine.

```shell
./soc_energy_eff.sh
```

## Results collection/processing

Get the power consumption logs from BMC.

```
scp -r bmc:/root/result .
```

Use the following commands to extract power consumption data.

```
python3 process_soc_energy_result.py {model}_{device}_{socnum}_{batchsize}_energy.log
```