import matplotlib.pyplot as plt
import numpy as np

from data_psnr import cpu_libx264, nvenc, soc_mediacodec, soccpu_libx264


def get_data():
    print(
        f"mediacodec lower PNSR compare with libx264 SoC-CPU: {np.array(soccpu_libx264) / np.array(soc_mediacodec)}"
    )
    return soccpu_libx264, soc_mediacodec, cpu_libx264, nvenc


def plot_psnr():
    soccpu, mediacodec, cpu, gpu = get_data()

    confs = {
        "edgecolor": "black",
        "linewidth": 1.5,
    }

    xticks = ["V1", "V2", "V3", "V4", "V5", "V6"]
    x = np.arange(len(xticks))
    bar_width = 0.15

    fig, ax = plt.subplots(figsize=(9, 2), dpi=100)
    b1 = ax.bar(
        x - bar_width * 2,
        soccpu,
        width=bar_width,
        label="SoC-CPU (libx264)",
        color="white",
        **confs,
    )
    b2 = ax.bar(
        x - bar_width * 1,
        mediacodec,
        width=bar_width,
        label="SoC-HW (MediaCodec)",
        color="white",
        hatch="//",
        **confs,
    )
    b3 = ax.bar(
        x, cpu, width=bar_width, label="Intel-CPU (libx264)", color="silver", **confs
    )
    b4 = ax.bar(
        x + bar_width,
        gpu,
        width=bar_width,
        label="GPU-A40 (NVENC)",
        color="black",
        **confs,
    )

    ax.set_xticks(x, xticks, fontsize=14, weight="bold")
    # ax.set_xticklabels(xticks)
    ax.set_ylabel("PSNR (dB)", fontsize=14, weight="bold")
    # ax.legend(fontsize=10, loc="lower left", bbox_to_anchor=(0.12, 0.97), ncol=2)
    legend_properties = {
        "weight": "bold",
        "size": 12,
    }
    ax.legend(
        fontsize=10,
        loc="lower left",
        bbox_to_anchor=(0.1, 1),
        ncol=2,
        prop=legend_properties,
    )

    # plt.show()
    plt.savefig("psnr.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_psnr()
