import pynvml
import time

pynvml.nvmlInit()


def printNvidiaGPU(gpu_id):
    gpu_device = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)

    powerUsage = pynvml.nvmlDeviceGetPowerUsage(gpu_device)
    powerState = pynvml.nvmlDeviceGetPowerState(gpu_device)
    print("PowerState: {0}".format(powerState))
    print(f"Cur time: {time.time()}, PowerUsage: {(powerUsage / 1000)}")
    return powerUsage / 1000


if __name__ == "__main__":
    powerUsages = []
    printNvidiaGPU(0)  # 0号gpu
