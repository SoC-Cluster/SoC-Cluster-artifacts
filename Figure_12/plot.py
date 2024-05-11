import os

import matplotlib.pyplot as plt
import numpy as np

confs = {
    "linewidth": 1.5,
}

log_folders = {
    "SoC-CPU": "data/soc-cpu",
    "SoC-GPU": "data/soc-gpu",
    "GPU": "data/gpu-a100",
}

# linestype, color
hw2confs = {
    "SoC-CPU": ["--", "blue"],
    "SoC-GPU": ["-.", "red"],
    "CPU": ["-", "black"],
    "GPU": ["--", "grey"],
    "Device": [":", "orange"],
}


def parse_gpu_log(file):
    throughputs, powers_per_frame = [], []
    with open(file) as f:
        lines = f.readlines()
    for line in lines[1:]:
        items = line.split()
        throughputs.append(float(items[0]))
        powers_per_frame.append(float(items[1]))
    return throughputs, powers_per_frame


hardwares = ["SoC-GPU", "GPU-A100"]

"""
2022-08-27, V1:  yolo first 9 points, resnet first 6 points
2022-08-27, V2:  resnet first 6 points
"""


def parse_logs(model):
    path = os.path.join("data", model)
    d = dict()
    for hw in hardwares:
        file = os.path.join(path, f"{hw}.log")
        if "GPU" in hw and not "SoC" in hw:
            th, powers = parse_gpu_log(file)
            if model == "YOLOv5x":
                th = [t * 4 for t in th]
        elif "SoC" in hw:
            th, powers = parse_gpu_log(file)
            if model == "YOLOv5x":
                th = [t * 4 for t in th]

        # V1
        # if model == "YOLOv5x":
        #     th = th[:9]
        #     powers = powers[:9]
        # elif model == "ResNet-50":
        #     th = th[:6]
        #     powers = powers[:6]

        # V2
        # if model == "ResNet-50":
        #     th = th[:6]
        #     powers = powers[:6]

        d[hw] = [th, 1 / np.array(powers)]
    return d


def plot_single(axis, model):
    print(f"Plotting energy scalability for {model}")
    d = parse_logs(model)
    print(d)

    lines = []
    if model == "ResNet-50":
        axins = axis.inset_axes([0.25, 0.3, 0.3, 0.3])
        axins.set_xlim(0, 70)
        axins.set_ylim(0, 8)

    for hw, val in d.items():
        if "GPU-" in hw:
            th, po = val
            axis.plot(th, po, marker=".", color="darkred", label=hw, alpha=0.8)

            if model == "ResNet-50":
                axins.plot(th, po, marker=".", color="darkred", label=hw, alpha=0.8)
        elif "SoC-GPU" in hw:
            th, po = val
            axis.plot(th, po, marker="1", color="darkblue", label=hw)

            if model == "ResNet-50":
                axins.plot(th, po, marker="1", color="darkblue", label=hw)

    if model == "ResNet-50":
        model = f"{model} (FP32)"
        axis.set_xlabel(f"Input loads (frames/s)\n{model}", fontsize=13, weight="bold")
        axis.indicate_inset_zoom(axins, edgecolor="black")
    elif model == "YOLOv5x":
        model = f"{model} (FP32)"
        axis.set_xlabel(f"Input loads (frames/4s)\n{model}", fontsize=13, weight="bold")
    axis.grid(axis="both", alpha=0.3)
    legend_properties = {
        "weight": "bold",
        "size": 11,
    }
    axis.legend(prop=legend_properties)

    return lines


def plot_all():
    figure_mosaic = """
    AB
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(8, 2.3), dpi=100)

    plot_single(axes["A"], "ResNet-50")
    plot_single(axes["B"], "YOLOv5x")

    plt.subplots_adjust(hspace=0.5)
    fig.supylabel("TpE (frames/J)", fontsize=14, x=0.035, weight="bold")

    # plt.show()
    plt.savefig("energy_scalability.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_all()
