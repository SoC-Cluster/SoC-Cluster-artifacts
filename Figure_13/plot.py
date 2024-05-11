import matplotlib.pyplot as plt

from data import *

soc_series = ["835", "845", "855", "865", "888", "8+Gen1"]
# TODO:
# soc_specs = ["835", "845", "855", "865", "888"]
# release_dates = ["02/2016", "02/2018", "01/2020", "03/2020", "06/2021"]

hw2color = {
    "SoC-CPU": "darkblue",
    "SoC-GPU": "darkred",
    "SoC-DSP": "darkgreen",
}
hw2marker = {
    "SoC-CPU": "s",
    "SoC-GPU": "^",
    "SoC-DSP": "h",
}
label_confs = {
    "fontsize": 12,
    "weight": "bold",
}


def plot_dl_single(axis, model):
    latency = resnet50_latency if model == "resnet50" else yolov5x_latency
    lines = []
    for hw, v in latency.items():
        print(f"Current hardware: {hw}")
        line = axis.plot(
            v.keys(),
            v.values(),
            marker=hw2marker[hw],
            markersize=4,
            label=hw[-3:],
            color=hw2color[hw],
        )
        lines += line

    # add y-value text for each point
    for hw, v in latency.items():
        for x, y in v.items():
            if hw == "SoC-CPU":
                vpos = "bottom"
                ypos = y * 1.1
            elif hw == "SoC-GPU":
                vpos = "top"
                ypos = y * 0.8
            elif hw == "SoC-DSP":
                vpos = "bottom"
                ypos = y + 0.1
            axis.text(
                x, ypos, f"{y:.1f}", fontsize=8, ha="center", va=vpos, weight="bold"
            )
    # adjust x/y-limit for better visualization
    axis.set_ylim(0.8, 400)
    axis.set_xlim(axis.get_xticks()[0] - 0.5, axis.get_xticks()[-1] + 0.3)

    # if model == "resnet50":
    #     axis.set_xlabel("ResNet-50", **label_confs)
    # else:
    #     axis.set_xlabel("YOLOv5x", **label_confs)

    axis.set_xticklabels(soc_series, rotation=45, ha="center")
    axis.set_yscale("log")
    axis.set_xlabel("DL Serving", **label_confs)


def plot_dl():
    figure_mosaic = """
    AB
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(7, 2), dpi=100)

    plot_dl_single(axes["A"], "resnet50")
    plot_dl_single(axes["B"], "yolov5x")

    axes["A"].legend(loc="lower left", bbox_to_anchor=(0.5, 1), ncol=3)

    fig.supylabel("Latency (ms)", fontsize=12, x=0.05, weight="bold")
    plt.subplots_adjust(wspace=0.2)
    # plt.show()
    plt.savefig("soc_dl.pdf", bbox_inches="tight", pad_inches=0)


def plot_video_single(axis, type):
    if type == "online":
        pre_data = pre_online_throughput
        hall_data = hall_online_throughput
    elif type == "offline":
        pre_data = pre_offline_throughput
        hall_data = hall_offline_throughput

    # get CPU data (onlien and offline)
    pre_cpu_data, hall_cpu_data = pre_data["SoC-CPU"], hall_data["SoC-CPU"]
    axis.plot(
        pre_cpu_data.keys(),
        pre_cpu_data.values(),
        marker="s",
        markersize=4,
        label="CPU (V4)",
        color="darkblue",
    )
    axis.plot(
        hall_cpu_data.keys(),
        hall_cpu_data.values(),
        marker="^",
        markersize=4,
        label="CPU (V5)",
        color="darkblue",
        linestyle="-.",
    )

    # get MediaCodec data (online)
    if type == "online":
        pre_hw_data, hall_hw_data = pre_data["SoC-HW"], hall_data["SoC-HW"]
        axis.plot(
            pre_hw_data.keys(),
            pre_hw_data.values(),
            marker="s",
            markersize=4,
            label="HWCodec (V4)",
            color="black",
        )
        axis.plot(
            hall_hw_data.keys(),
            hall_hw_data.values(),
            marker="^",
            markersize=4,
            label="HWCodec (V5)",
            color="black",
            linestyle="-.",
        )

    if type == "online":
        axis.set_xlabel("Live Streaming Transcoding", **label_confs)
    else:
        axis.set_xlabel("Archive Transcoding", **label_confs)
    axis.set_xticklabels(soc_series, rotation=45, ha="center")


def plot_video():
    figure_mosaic = """
    AB
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(7, 2), dpi=100)

    plot_video_single(axes["A"], "online")
    plot_video_single(axes["B"], "offline")

    axes["A"].legend(loc="lower left", bbox_to_anchor=(0.35, 0.95), ncol=2)

    fig.supylabel("Throughput (frames/s)", fontsize=12, x=0.04, weight="bold")
    plt.subplots_adjust(wspace=0.2)
    # plt.show()
    plt.savefig("soc_video.pdf", bbox_inches="tight", pad_inches=0)


def plot_one():
    figure_mosaic = """
    AB
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(7, 2), dpi=100)

    plot_dl_single(axes["A"], "resnet50")
    plot_video_single(axes["B"], "online")

    axes["A"].legend(loc="lower left", bbox_to_anchor=(-0.2, 1), ncol=3)
    axes["B"].legend(loc="lower left", bbox_to_anchor=(-0.2, 1), ncol=2)

    axes["A"].set_ylabel("Latency (ms)", **label_confs)
    axes["B"].set_ylabel("Throughput\n(frames/s)", **label_confs)

    plt.subplots_adjust(wspace=0.4)
    # plt.show()
    plt.savefig("soc_one.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    # Two saparate plots for DL and video
    # plot_dl()
    # plot_video()

    # One plot with DL (ResNet-50) and video (Live Streaming Transcoding)
    plot_one()
