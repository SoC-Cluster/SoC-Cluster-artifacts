import matplotlib.pyplot as plt
import numpy as np

from data_soc_compare import online_soc_libx264, online_soc_mediacodec, video_fps

online_data = [online_soc_libx264, online_soc_mediacodec]


def plot_soc_perf(metric):
    """
    plotting soc performance
    """
    label_font_conf = {"weight": "bold", "size": "14"}
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
    plot_data = online_data
    bar_confs["color"] = bar_confs["color"][: len(plot_data)]
    bar_confs["hatch"] = bar_confs["hatch"][: len(plot_data)]

    x = [0.1, 0.1 + bar_width * 2]

    xlabels = ["V1", "V2", "V3", "V4", "V5", "V6"]
    ax = [axes["A"], axes["B"], axes["C"], axes["D"], axes["E"], axes["F"]]

    for i in range(len(axes)):
        ax[i].set_xlabel(xlabels[i], **label_font_conf)
        ax[i].set_xticks([])
        if metric == "tps":
            # h = [data[i][2] * 30 for data in plot_data]  # throughput per U (30 SoCs)
            # Modified by zl. 2023-01-12
            h = [
                data[i][2] * 60 for data in plot_data
            ]  # throughput of the whole server (60 SoCs)
            print(f"{xlabels[i]}: {metric}, tps times to SoC-CPU {np.array(h) / h[0]}")
        elif metric == "tpe":
            # 1. cal the processed frame number per Joule
            # 2. according to the above results, cal the processed stream nums
            h = [(1 / data[i][1]) / video_fps[i] for data in plot_data]
            print(
                f"{xlabels[i]}: {metric}, {h}, tpe times to SoC-CPU {np.array(h) / h[0]}"
            )
        ax[i].bar(x, h, width=bar_width, **bar_confs)

        ax[i].grid(axis="y", alpha=0.3)
        min_xaxis = min(x) - bar_width * 1.5
        max_xaxis = max(x) + bar_width * 1.5
        ax[i].set_xlim(min_xaxis, max_xaxis)
        ax[i].tick_params(direction="in")

    if metric == "tps":
        ax[0].set_ylabel("Throughput\n(streams)", **label_font_conf)
    elif metric == "tpe":
        ax[0].set_ylabel("TpE\n(streams/W)", **label_font_conf)
    # https://matplotlib.org/stable/api/container_api.html#module-matplotlib.container
    bars = ax[0].containers[0].get_children()
    labels = ["SoC-CPU (libx264)", "SoC-HW (MediaCodec)"]
    legend_properties = {
        "weight": "bold",
        "size": 12,
    }
    ax[0].legend(
        bars,
        labels,
        ncol=4,
        loc="lower left",
        bbox_to_anchor=(1.3, 1),
        prop=legend_properties,
    )

    plt.subplots_adjust(wspace=1)
    # plt.show()
    plt.savefig(f"soc_compare_{metric}.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    print("====== tps results")
    plot_soc_perf("tps")
    print("====== tpe results")
    plot_soc_perf("tpe")
