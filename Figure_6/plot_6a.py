import matplotlib.pyplot as plt
import numpy as np

from data_tpe import online_CPU, online_GPU, online_SoC_SW, video_fps

th_times = [60, 10, 8]
units = [2, 4, 4]
online_data = [online_SoC_SW, online_CPU, online_GPU]


def plot_fps_stream_number(type, codec, metric):
    """
    plotting max stream numbers (online) or fps (offline) for each video
    type:
        - online: plotting [libx264 (SoC-CPU), mediacodec(SoC-HW), libx264 (CPU), nvenc (GPU)]
        - offline: plotting [libx264 (SoC-CPU), libx264 (CPU), nvenc (GPU)]
    codec: h264 or h265
    metric: tps or tpe
    """
    label_font_conf = {"weight": "bold", "size": "12"}
    # SoC-CPU, SoC-HW, CPU, GPU
    bar_confs = {
        "color": ["white", "white", "silver", "grey"],
        "linewidth": 1,
        "hatch": ["", "//", "", "//"],
        "edgecolor": "black",
    }

    figure_mosaic = """
    AAA.BBB.CCC.DDD.EEE.FFF
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(9, 2), dpi=100)
    bar_width = 0.03
    x = [0.1, 0.1 + bar_width * 2, 0.1 + bar_width * 4]
    bar_confs["color"] = bar_confs["color"][:1] + bar_confs["color"][2:]
    bar_confs["hatch"] = bar_confs["hatch"][:1] + bar_confs["hatch"][2:]
    if type == "online":
        data = online_data

    xlabels = ["V1", "V2", "V3", "V4", "V5", "V6"]
    ax = [axes["A"], axes["B"], axes["C"], axes["D"], axes["E"], axes["F"]]

    for i in range(len(axes)):
        ax[i].set_xlabel(xlabels[i], **label_font_conf)
        ax[i].set_xticks([])
        video_name = xlabels[i]  # video name
        if type == "online":
            if metric == "tpe":
                # frames can be processed per Joule: 1 / hw[video_name][1]
                # streams can be supported per Joule: (1 / hw[video_name][1]) / video_fps[video_name]
                h = [
                    (
                        (1 / hw[video_name][1]) / video_fps[video_name]
                        if hw[video_name][0] != -1
                        else 0
                    )
                    for hw in data
                ]  # throughput: maximum stream number per Joule per second (streams/Watts)
            ax[i].bar(x, h, width=bar_width, **bar_confs)
        ax[i].grid(axis="y", alpha=0.3)
        ax[i].set_xlim(min(x) - bar_width * 1.5, max(x) + bar_width * 1.5)
        ax[i].tick_params(direction="in")

        if metric == "tpe":
            print(
                f"V{i+1}, {type}, {metric}: {h}, times to Intel-CPU: {np.array(h) / h[1]}, times to GPU: {np.array(h) / h[2]}"
            )

        # if metric == "fps" and type == "offline" and (video_name == "V5" or video_name == "V6"):
        #     ax[i].set_yscale("log")

    if type == "online":
        if metric == "tpe":
            ax[0].set_ylabel("TpE (streams/W)", **label_font_conf)
        # https://matplotlib.org/stable/api/container_api.html#module-matplotlib.container
        bars = ax[0].containers[0].get_children()
        labels = ["SoC-CPU", "Intel-CPU", "GPU-A40"]
        legend_properties = {
            "weight": "bold",
            "size": 11,
        }
        ax[0].legend(
            bars,
            labels,
            ncol=4,
            loc="lower left",
            bbox_to_anchor=(1.6, 1),
            prop=legend_properties,
        )

    plt.subplots_adjust(wspace=1)

    # plt.show()
    plt.savefig(f"{type}_{codec}_{metric}.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_fps_stream_number("online", "h264", "tpe")
