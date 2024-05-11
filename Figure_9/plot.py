import matplotlib.pyplot as plt

from data_bitrate import soc_libx264_bitrate, soc_mediacodec_bitrate, target_bitrate

compare_bitrate_data = [soc_libx264_bitrate, soc_mediacodec_bitrate]


def add_target_bitrate(axis, bitrate_index, left, right):
    line = axis.hlines(
        y=target_bitrate[bitrate_index],
        xmin=left,
        xmax=right,
        linestyles="dashed",
        color="red",
        linewidth=2,
    )
    return line


def plot_video_bitrate():
    """
    plotting output bitrate generad by videos with SoC libx264 and SoC MediaCodec
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
    x = [0.1, 0.1 + bar_width * 2]

    xlabels = ["V1", "V2", "V3", "V4", "V5", "V6"]
    ax = [axes["A"], axes["B"], axes["C"], axes["D"], axes["E"], axes["F"]]

    plot_data = compare_bitrate_data
    bar_confs["color"] = bar_confs["color"][: len(plot_data)]
    bar_confs["hatch"] = bar_confs["hatch"][: len(plot_data)]

    bitrate_lines = []
    for i in range(len(axes)):
        ax[i].set_xlabel(xlabels[i], **label_font_conf)
        ax[i].set_xticks([])

        h = [data[i] for data in plot_data]
        ax[i].bar(x, h, width=bar_width, **bar_confs)

        ax[i].grid(axis="y", alpha=0.3)
        min_xaxis = min(x) - bar_width * 1.5
        max_xaxis = max(x) + bar_width * 1.5
        ax[i].set_xlim(min_xaxis, max_xaxis)
        ax[i].tick_params(direction="in")
        line = add_target_bitrate(ax[i], i, min_xaxis, max_xaxis)

    # legends
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
        bbox_to_anchor=(-0.5, 1),
        prop=legend_properties,
    )
    # lines legend
    bitrate_lines.append(line)
    bitrate_lines.reverse()
    line_labels = ["Target Bitrate"]
    ax[3].legend(
        bitrate_lines,
        line_labels,
        ncol=2,
        loc="lower left",
        bbox_to_anchor=(1.6, 1),
        prop=legend_properties,
    )

    ax[0].set_ylabel("Average Video\nBitrate (Mbps)", **label_font_conf)

    plt.subplots_adjust(wspace=1)
    plt.show()
    # plt.savefig(f"output_bitrate.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_video_bitrate()
