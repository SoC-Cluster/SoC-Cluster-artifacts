import matplotlib.pyplot as plt

confs = {
    "linewidth": 1.5,
}

log_folders = {
    "SoC-CPU": "data/soc-cpu",
    "SoC-GPU": "data/soc-gpu",
    "GPU": "data/gpu-a100",
}

# color
hw2color = {
    "SoC-CPU": ["darkblue"],
    "Intel-CPU": ["darkgreen"],
    "GPU-A40": ["darkred"],
}


def parse_log(file):
    with open(file) as f:
        lines = f.readlines()
    stream_nums, stream_powers = [], []
    for line in lines:
        if line.startswith("0"):
            continue
        stream_nums.append(int(line.split()[0]))
        stream_powers.append(float(line.split()[1]))
    return stream_nums, stream_powers


hardwares = ["SoC-CPU", "Intel-CPU", "GPU-A40"]
hw2markers = {"SoC-CPU": ".", "Intel-CPU": "s", "GPU-A40": "^"}


def parse_video_logs(video):
    d = dict()
    # parse gpu log
    for hw in hardwares:
        gpu_file = f"data/{hw}/{video}.log"
        stream_nums, stream_powers = parse_log(gpu_file)
        d[hw] = dict(stream_nums=stream_nums, stream_powers=stream_powers)
    return d


abbr2video = {
    "pre": "V4: presentation",
    "hall": "V5: hall",
    "game3": "V3: game3",
    "chi": "V6: chicken",
    "holi": "V1: holi",
    "desk": "V2: desktop",
}


def plot_single(axis, video):
    print(f"Plotting energy scalability for {video}")
    d = parse_video_logs(video)

    lines = []
    for hw, val in d.items():
        stream_nums = val["stream_nums"]
        powers = val["stream_powers"]  # power per stream (Watt/stream)
        tpe = [1 / p for p in powers]  # stream number per Watt (streams/Watt)
        print(f"{video}, {hw}, {tpe}")
        # adjust marker size by hw type
        if hw == "GPU-A40" or hw == "Intel-CPU":
            line = axis.plot(
                stream_nums,
                tpe,
                label=hw,
                marker=hw2markers[hw],
                markersize=4,
                color=hw2color[hw][0],
            )
        else:
            line = axis.plot(
                stream_nums, tpe, label=hw, marker=hw2markers[hw], color=hw2color[hw][0]
            )
        lines += line

    axis.set_xlabel(f"Stream number\n{abbr2video[video]}", fontsize=13, weight="bold")
    axis.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20])
    legend_properties = {
        "weight": "bold",
        "size": 11,
    }
    axis.legend(prop=legend_properties)
    if video == "pre":
        axis.set_ylabel("TpE (streams/W)", fontsize=13, weight="bold")

    return lines


def plot_all():
    figure_mosaic = """
    AB
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(8, 2.3), dpi=100)

    plot_single(axes["A"], "pre")
    plot_single(axes["B"], "hall")

    plt.subplots_adjust(hspace=0.5)

    # plt.show()
    plt.savefig("per_stream_power_eff.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_all()
