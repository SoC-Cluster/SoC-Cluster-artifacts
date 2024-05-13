import matplotlib.pyplot as plt

confs = {
    "linewidth": 3,
}
label_font_conf = {"weight": "bold", "size": "12"}
legend_properties = {
    "weight": "bold",
    "size": 11,
}


# return:
#   - timestamp in milliseconds; relative to the first sampling time
#   - throughput in Mbps
def parse_traffic_log(file):
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    ts, throughput = [], []
    for line in lines:
        t, tp = line.split(", ")
        ts.append(float(t) / 1000 / 60 / 60)
        throughput.append(float(tp) / 1000)
    return ts, throughput


def plot():
    fig, axes = plt.subplot_mosaic(mosaic="A", figsize=(6, 1.7), dpi=100)

    ts1, tp1 = parse_traffic_log("data/inbound_traffic.csv")
    ts2, tp2 = parse_traffic_log("data/outbound_traffic.csv")
    axes["A"].plot(ts1, tp1, label="Inbound Traffic", color="grey")
    axes["A"].plot(ts2, tp2, label="Outbound Traffic", color="darkblue")

    axes["A"].set_ylim(-0.2, 3.2)
    axes["A"].set_xlim(-1, 39)

    axes["A"].set_ylabel("Network\nThroughput\n(Gbps)", **label_font_conf)
    axes["A"].set_xlabel("Time of Day", **label_font_conf)

    axes["A"].set_xticks(
        ticks=[0, 14, 24, 38], labels=["00:00", "14:00", "00:00", "14:00"]
    )
    axes["A"].tick_params(axis="both", which="major", labelsize=11, direction="in")

    axes["A"].grid(True, alpha=0.3)

    axes["A"].legend(
        prop=legend_properties, loc="lower left", bbox_to_anchor=(0.05, 0.95), ncol=2
    )
    # plt.show()
    plt.savefig("net_var.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot()
