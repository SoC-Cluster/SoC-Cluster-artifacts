import matplotlib.pyplot as plt
from data import get_data, gpu_names, hw2confs

confs = {
    "linewidth": 1,
}
bar_st_x = 1
x_lim_left = bar_st_x - 0.15
bar_width = 0.1


def plot_fp32(axis, model):
    """Draw FP32"""
    data = get_data(model)
    print(f"====================== {model} ======================")

    cur_x = bar_st_x
    bars = dict()

    for data_types, vals in data.items():
        if data_types == "FP32":
            print(f"{model=}, decimal precision={data_types}")
            for hw, val in vals.items():
                # default batch = 1
                batch = 1
                label = hw
                # GPU: ignore other batch size except 1 and 64
                if gpu_names[0] in hw or gpu_names[1] in hw:
                    batch = int(hw.split("-")[-1])
                    if batch != 64 and batch != 1:
                        continue
                    label = "-".join(
                        hw.split("-")[:-1]
                    )  # convert NV-GPU-V100-{N} to NV-GPU-V100
                elif "SoC-GPU-" in hw:
                    if hw == "SoC-GPU-1" and model == "ResNet-50":
                        continue
                    label = "-".join(hw.split("-")[:-1])
                color, hatch, edgecolor = hw2confs[hw]

                TpE = 1 / val[1]  # throughput per Joule

                bars[hw] = {
                    "TpE": TpE,
                    "batch": batch,
                    "label": label,
                    "color": color,
                    "hatch": hatch,
                    "edgecolor": edgecolor,
                }

    plot_orders = [
        "SoC-CPU",
        "SoC-GPU-1",
        "SoC-GPU-8",
        "SoC-DSP",
        "SoC-Mix",
        "Intel-CPU",
        f"{gpu_names[0]}-1",
        f"{gpu_names[0]}-64",
        f"{gpu_names[1]}-1",
        f"{gpu_names[1]}-64",
    ]
    ret = []  # used for legend
    for tag in plot_orders:
        if not tag in bars.keys():
            continue
        TpE = bars[tag]["TpE"]
        label = bars[tag]["label"]
        color = bars[tag]["color"]
        hatch = bars[tag]["hatch"]
        edgecolor = bars[tag]["edgecolor"]
        print(tag, bars[tag]["TpE"])
        if gpu_names[0] in tag or gpu_names[1] in tag:
            batch = int(tag.split("-")[-1])
            b = axis.bar(
                cur_x,
                TpE,
                width=bar_width,
                label=f"{label} (BS={batch})",
                color=color,
                hatch=hatch,
                edgecolor=edgecolor,
                **confs,
            )
        else:
            b = axis.bar(
                cur_x,
                TpE,
                width=bar_width,
                label=label,
                color=color,
                hatch=hatch,
                edgecolor=edgecolor,
                **confs,
            )

        if model == "ResNet-50":
            ret.append(b)
        cur_x += bar_width * 2

    if model == "ResNet-50":
        model = "ResNet-50 (FP32)"
    elif model == "ResNet-152":
        model = "ResNet-152 (FP32)"
    elif model == "YOLOv5x":
        model = "YOLOv5x (FP32)"
    elif model == "BERT":
        model = "BERT (FP32)"

    axis.set_xlabel(f"{model}", fontsize=12, weight="bold")

    axis.set_xticks([])
    axis.set_xlim(x_lim_left, cur_x - 0.05)
    axis.grid(axis="y", alpha=0.3)
    # axis.set_yscale("log")

    # print(f"=================== {model} finished ==================")
    return ret


def plot_quant(axis, model):
    """Draw INT8"""
    data = get_data(model)
    print(f"====================== {model} ======================")

    cur_x = bar_st_x
    bars = dict()  # hw_label: throughput

    for data_types, vals in data.items():
        if data_types == "I8":
            print(f"{model=}, decimal precision={data_types}")
            for hw, val in vals.items():
                # plot configurations: label, color, hatch, edgecolor
                batch = 1
                label = hw
                if gpu_names[0] in hw or gpu_names[1] in hw:
                    batch = int(hw.split("-")[-1])
                    # print(f"batch = {batch}")
                    if batch != 64 and batch != 1:  # use batch=1 or batch=64 on GPU
                        continue
                    label = "-".join(
                        hw.split("-")[:-1]
                    )  # convert NV-GPU-V100-{N} to NV-GPU
                color, hatch, edgecolor = hw2confs[hw]
                TpE = 1 / val[1]  # throughput per Joule

                bars[hw] = {
                    "TpE": TpE,
                    "batch": batch,
                    "label": label,
                    "color": color,
                    "hatch": hatch,
                    "edgecolor": edgecolor,
                }
    plot_orders = [
        "SoC-DSP",
        "Intel-CPU",
        f"{gpu_names[0]}-1",
        f"{gpu_names[0]}-64",
        f"{gpu_names[1]}-1",
        f"{gpu_names[1]}-64",
    ]
    ret = []  # used for legend
    for tag in plot_orders:
        if not tag in bars.keys():
            continue
        TpE = bars[tag]["TpE"]
        label = bars[tag]["label"]
        color = bars[tag]["color"]
        hatch = bars[tag]["hatch"]
        edgecolor = bars[tag]["edgecolor"]
        print(tag, TpE)
        if gpu_names[0] in tag or gpu_names[1] in tag:
            batch = int(tag.split("-")[-1])
            b = axis.bar(
                cur_x,
                TpE,
                width=bar_width,
                label=f"{label} (BS={batch})",
                color=color,
                hatch=hatch,
                edgecolor=edgecolor,
                **confs,
            )
        else:
            b = axis.bar(
                cur_x,
                TpE,
                width=bar_width,
                label=label,
                color=color,
                hatch=hatch,
                edgecolor=edgecolor,
                **confs,
            )
        if model == "ResNet-50" and tag == "SoC-DSP":
            ret.append(b)
        cur_x += bar_width * 2

    if model == "ResNet-50":
        model = "ResNet-50 (INT8)"
    elif model == "ResNet-152":
        model = "ResNet-152 (INT8)"

    axis.set_xlabel(f"{model}", fontsize=12, weight="bold")

    axis.set_xticks([])
    axis.set_xlim(x_lim_left, cur_x - 0.05)
    axis.grid(axis="y", alpha=0.3)
    # axis.set_yscale("log")

    # print(f"=================== {model} finished ==================")
    return ret


def plot_all():
    figure_mosaic = """
    ABCDEF
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(16, 1.8), dpi=100)

    # set background color of each subfigure, according to bars (soc_bars, intel_cpu_bars, nvidia_gpu_bars)
    # and before plotting bars
    # =====================================================================================================
    splegend_confs = {
        "soc_bars": {
            # "color": "whitesmoke",
            "color": "#ffffff",
            "alpha": 0.2,
        },
        "intel_cpu_bars": {
            # "color": "silver",
            "color": "#e0e0e0",
            "alpha": 0.8,
        },
        "nvidia_gpu_bars": {
            # "color": "skyblue",
            "color": "#d0e0f0",
            "alpha": 0.8,
        },
    }
    ABC_split_span = [[0.8, 1.3], [1.3, 1.5], [1.5, 2.4]]
    DEF_split_span = [[0.8, 1.1], [1.1, 1.3], [1.3, 2.2]]
    for subfig in ["A", "B", "C"]:
        axes[subfig].axvspan(
            ABC_split_span[0][0],
            ABC_split_span[0][1],
            facecolor=splegend_confs["soc_bars"]["color"],
            alpha=splegend_confs["soc_bars"]["alpha"],
        )
        axes[subfig].axvspan(
            ABC_split_span[1][0],
            ABC_split_span[1][1],
            facecolor=splegend_confs["intel_cpu_bars"]["color"],
            alpha=splegend_confs["intel_cpu_bars"]["alpha"],
        )
        axes[subfig].axvspan(
            ABC_split_span[2][0],
            ABC_split_span[2][1],
            facecolor=splegend_confs["nvidia_gpu_bars"]["color"],
            alpha=splegend_confs["nvidia_gpu_bars"]["alpha"],
        )
    for subfig in ["D", "E", "F"]:
        axes[subfig].axvspan(
            DEF_split_span[0][0],
            DEF_split_span[0][1],
            facecolor=splegend_confs["soc_bars"]["color"],
            alpha=splegend_confs["soc_bars"]["alpha"],
        )
        axes[subfig].axvspan(
            DEF_split_span[1][0],
            DEF_split_span[1][1],
            facecolor=splegend_confs["intel_cpu_bars"]["color"],
            alpha=splegend_confs["intel_cpu_bars"]["alpha"],
        )
        axes[subfig].axvspan(
            DEF_split_span[2][0],
            DEF_split_span[2][1],
            facecolor=splegend_confs["nvidia_gpu_bars"]["color"],
            alpha=splegend_confs["nvidia_gpu_bars"]["alpha"],
        )

    # plot bars
    # =========
    b1 = plot_fp32(axes["A"], "ResNet-50")
    plot_fp32(axes["B"], "ResNet-152")
    plot_fp32(axes["C"], "YOLOv5x")
    plot_fp32(axes["D"], "BERT")
    b2 = plot_quant(axes["E"], "ResNet-50")
    plot_quant(axes["F"], "ResNet-152")

    # reuse legend atop of Latency figure
    # so comment here
    # ====================================
    # bar_with_order = b1[:2] + b2 + b1[2:]
    # labels = [b.get_label() for b in bar_with_order]
    # legend_properties = {
    #     'weight':'bold',
    #     "size": 11,
    # }
    # axes["A"].legend(bar_with_order, labels, loc="lower left", bbox_to_anchor=(-0.5, 1), ncol=4, prop=legend_properties)

    # for ax in axes:
    #     for bars in axes[ax].containers:
    #         continue
    #         axes[ax].bar_label(bars, fmt="%.2f", fontsize=9, color="b", rotation=40, label_type="edge", padding=-1)

    fig.supylabel("TpE (frames/J)", fontsize=14, x=0.09, weight="bold")
    plt.subplots_adjust(hspace=1)
    # plt.show()

    plt.savefig("dl_tpe_all_onerow.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_all()
