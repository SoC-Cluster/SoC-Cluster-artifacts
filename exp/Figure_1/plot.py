import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


confs = {
    "linewidth": 3,
}
label_font_conf = {"weight": "bold", "size": "12"}
legend_properties = {
    "weight": "bold",
    "size": 11,
}


def edge_filter(data: pd.DataFrame):
    filtered_df = data.loc[
        (data["cores"] <= 8)
        & (data["memory"] <= 12 * 1000)
        & (data["storage"] <= 256 * 1000)
    ]
    print(len(filtered_df))


def azure_filter():
    data_path = "azure2019_data/vmtable.csv"
    headers = [
        "vmid",
        "subscriptionid",
        "deploymentid",
        "vmcreated",
        "vmdeleted",
        "maxcpu",
        "avgcpu",
        "p95maxcpu",
        "vmcategory",
        "vmcorecountbucket",
        "vmmemorybucket",
    ]
    data = pd.read_csv(
        data_path, header=None, index_col=False, names=headers, delimiter=","
    )
    print(len(data))
    filtered_df = data.loc[
        (
            (data["vmcorecountbucket"] == "2")
            | (data["vmcorecountbucket"] == "4")
            | (data["vmcorecountbucket"] == "8")
        )
        & (
            (data["vmmemorybucket"] == "2")
            | (data["vmmemorybucket"] == "4")
            | (data["vmmemorybucket"] == "8")
        )
    ]
    print(len(filtered_df))


def parse_azure_data():
    with open("azure2019_data/cores.txt") as f:
        lines = f.readlines()
    cores, cores_cumulative_prob = [], []
    for line in lines[1:]:
        cores.append(int(line.split()[0]))
        cores_cumulative_prob.append(float(line.split()[1]) / 100)
    cores_cumulative_prob = np.cumsum(cores_cumulative_prob)

    with open("azure2019_data/memory.txt") as f:
        lines = f.readlines()
    mem, mem_cumulative_prob = [], []
    for line in lines[1:]:
        mem.append(int(line.split()[0]))
        mem_cumulative_prob.append(float(line.split()[1]) / 100)
    mem_cumulative_prob = np.cumsum(mem_cumulative_prob)

    return cores, cores_cumulative_prob, mem, mem_cumulative_prob


def parse_ens_data():
    data = pd.read_csv("aliens_data/e_vm_instance.csv")
    cores = data["cores"].values
    mem = data["memory"].values / 1000  # convert to GB
    storage = data["storage"].values / 1000  # convert to GB
    print(len(cores))

    # filters
    edge_filter(data)

    return cores, mem, storage


def plot_spec_cdf(hw_type, axis, edge_values, azvalues=None, azprob=None):
    sorted_edge_values = np.sort(edge_values)
    edge_cumulative_prob = np.arange(1, len(sorted_edge_values) + 1) / len(
        sorted_edge_values
    )
    print(
        f"min {np.min(sorted_edge_values)}, median {np.median(sorted_edge_values)}, max {np.max(sorted_edge_values)}"
    )

    if azvalues is not None:
        axis.plot(
            azvalues,
            azprob,
            label="Microsoft Azure VMs",
            linewidth=confs["linewidth"],
            color="darkgreen",
            linestyle="--",
        )
    axis.plot(
        sorted_edge_values,
        edge_cumulative_prob,
        label="Alibaba ENS VMs",
        linewidth=confs["linewidth"],
        color="darkblue",
    )

    # set x and y grid
    axis.grid(axis="both", alpha=0.3, linestyle="--")
    # axis.tick_params(direction="in")

    if hw_type == "CPU":
        axis.set_xlabel("CPU Cores", **label_font_conf)
        edge_y_value = np.interp(8, sorted_edge_values, edge_cumulative_prob)
        az_y_value = np.interp(8, azvalues, azprob)
        print(f"8, {edge_y_value}, {az_y_value}")
        axis.set_xticks([2, 8, 16, 32, 64])
        axis.set_yticks([0, 0.5, 1])
        axis.set_xlim(0, 33)
        axis.set_ylabel("CDF", **label_font_conf)
    if hw_type == "Mem":
        axis.set_xlabel("Memory (GB)", **label_font_conf)
        edge_y_value = np.interp(12, sorted_edge_values, edge_cumulative_prob)
        az_y_value = np.interp(12, azvalues, azprob)
        axis.set_xticks([12, 32, 64])
        axis.set_yticks([0, 0.5, 1])
        axis.set_xlim(0, 69)
        print(f"12, {edge_y_value}, {az_y_value}")
    if hw_type == "Storage":
        axis.set_xlabel("Storage (GB)", **label_font_conf)
        edge_y_value = np.interp(256, sorted_edge_values, edge_cumulative_prob)
        print(f"256, {edge_y_value}")
        axis.set_xlim(0, sorted_edge_values[-10])
        axis.set_xticks([256, 512, 1024])
        axis.set_yticks([0, 0.5, 1])
        axis.set_xlim(0, 1024)


def plot_all():
    figure_mosaic = """
    ABC
    """
    fig, axes = plt.subplot_mosaic(mosaic=figure_mosaic, figsize=(6, 1.7), dpi=100)

    ens_data = parse_ens_data()
    azcores, azcores_prob, azmem, azmem_prob = parse_azure_data()
    plot_spec_cdf("CPU", axes["A"], ens_data[0], azcores, azcores_prob)
    plot_spec_cdf("Mem", axes["B"], ens_data[1], azmem, azmem_prob)
    plot_spec_cdf("Storage", axes["C"], ens_data[2])

    # aure_data = parse_azure_data()
    # plot_spec_cdf("CPU", axes["A"], aure_data[0])
    # plot_spec_cdf("Mem", axes["B"], aure_data[1])
    axes["A"].legend(
        prop=legend_properties, loc="lower left", bbox_to_anchor=(0, 1), ncol=2
    )

    plt.subplots_adjust(wspace=0.5)

    # plt.show()
    plt.savefig("edgevm_specs.pdf", bbox_inches="tight", pad_inches=0)


if __name__ == "__main__":
    plot_all()
    # azure_filter()
