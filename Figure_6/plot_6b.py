import matplotlib.pyplot as plt
import numpy as np

from data_tpe import offline_CPU, offline_GPU, offline_SoC_SW, video_fps

th_times = [60, 10, 8]
units = [2, 4, 4]
offline_data = [offline_SoC_SW, offline_CPU, offline_GPU]


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
    if type == "offline":
        data = offline_data

    xlabels = ["V1", "V2", "V3", "V4", "V5", "V6"]
    ax = [axes["A"], axes["B"], axes["C"], axes["D"], axes["E"], axes["F"]]

    for i in range(len(axes)):
        ax[i].set_xlabel(xlabels[i], **label_font_conf)
        ax[i].set_xticks([])
        video_name = xlabels[i]  # video name
        if type == "offline":
            if metric == "tpe":
                h = [
                    1 / hw[video_name][1] for hw in data if hw[video_name][1] != -1
                ]  # power
            ax[i].bar(x, h, width=bar_width, **bar_confs)
        ax[i].grid(axis="y", alpha=0.3)
        ax[i].set_xlim(min(x) - bar_width * 1.5, max(x) + bar_width * 1.5)
        ax[i].tick_params(direction="in")

        print(
            f"V{i+1}, {type}, {metric}: {h}, times to Intel-CPU: {h[1] / np.array(h)}, times to GPU: {h[2] / np.array(h)}"
        )

    if type == "offline":
        if metric == "tpe":
            ax[0].set_ylabel("TpE (frames/J)", **label_font_conf)
        bars = ax[0].containers[0].get_children()
        labels = ["SoC-CPU", "Intel-CPU", "GPU-A40"]
        legend_properties = {
            "weight": "bold",
            "size": 11,
        }
        ax[0].legend(
            bars,
            labels,
            ncol=3,
            loc="lower left",
            bbox_to_anchor=(1.6, 1),
            prop=legend_properties,
        )

    plt.subplots_adjust(wspace=1)
    plt.savefig(f"{type}_{codec}_{metric}.pdf", bbox_inches="tight", pad_inches=0)
    # plt.show()


if __name__ == "__main__":
    plot_fps_stream_number("offline", "h264", "tpe")
