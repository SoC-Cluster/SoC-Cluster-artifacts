# SoC-Cluster Artifacts

We provide raw data and post-processed data for plotting all figures in our study.

To plot all figures in each subdirectory, use the command `make all` (or plot individual ones using `make fig[x]`).

Data for plotting all figures are acquired through our benchmark suite.
For each figure/table, we also link corresponding code for generating the raw data or post-processed data.

## Figures

- Figure_1: CDF of resource subscription of VMs
    - Data type: raw data
    - Plotting command: `make fig1`

- Figure_5: Network throughput of an in-the-wild SoC Cluster
    - Data type: raw data
    - Plotting command: `make fig5`

- Figure_6: Transcoding energy efficiency
    - Data type: post-processed data
    - Code & doc: fig_6a: [transcoding/live_streaming_throughput_power.md](../transcoding/live_streaming_throughput_power.md), fig_6b: [transcoding/archive_throughput_power.md](../transcoding/archive_throughput_power.md)
    - Plotting command: `make fig6`

- Figure_7: Energy efficiency of live streaming transcoding with different number of live video streams
    - Data type: post-processed data
    - Code & doc: [transcoding/energy_efficiency.md](../transcoding/energy_efficiency.md)
    - Plotting command: `make fig7`

- Figure_8: Live streaming transcoding performance on SoC Cluster
    - Data type: post-processed data
    - Code & doc: [transcoding/live_streaming_throughput_power.md](../transcoding/live_streaming_throughput_power.md)
    - Plotting command: `make fig8`

- Figure_9: Target/output bitrate in live streaming transcoding
    - Data type: post-processed data
    - Code & doc: [transcoding/video_bitrate.md](../transcoding/video_bitrate.md)
    - Plotting command: `make fig9`

- Figure_10: Live streaming transcoding quality
    - Data type: post-processed data
    - Code & doc: [transcoding/video_quality.md](../transcoding/video_quality.md)
    - Plotting command: `make fig10`

- Figure_11: Deep learning performance on SoC Cluster and the traditional edge server
    - Data type: post-processed data
    - Code: [dl/latency_power/README.md](../dl/latency_power/README.md)
    - Plotting command: `make fig11`

- Figure_12: DL energy efficiency
    - Data type: post-processed data
    - Code: [dl/energy_efficiency/README.md](../dl/energy_efficiency/README.md)
    - Plotting command: `make fig12`

- Figure_13: Performance evolution of different SoC models
    - Data type: post-processed data
    - Code & doc: [soc_evol/README.md](../soc_evol/README.md)
    - Plotting command: `make fig13`

## Tables

- Table_2: Use the [Geekbench 5](https://www.geekbench.com/) on both traditional server and mobile SoC to get the target score.

- Table_4/5: Follow the instruction in "Section 6: Cost Analysis" to calculate all values.