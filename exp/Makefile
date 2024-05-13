.PHONY: all fig1 fig5 fig6 fig7 fig8 fig9 fig10 fig11 fig12 fig13 clean

all: fig1 fig5 fig6 fig7 fig8 fig9 fig10 fig11 fig12 fig13

fig1:
	cd Figure_1 && python3 plot.py && mv edgevm_specs.pdf fig1.pdf

fig5:
	cd Figure_5 && python3 plot.py && mv net_var.pdf fig5.pdf

fig6:
	cd Figure_6 && python3 plot_6a.py && mv online_h264_tpe.pdf fig6a.pdf
	cd Figure_6 && python3 plot_6b.py && mv offline_h264_tpe.pdf fig6b.pdf

fig7:
	cd Figure_7 && python3 plot.py && mv per_stream_power_eff.pdf fig7.pdf

fig8:
	cd Figure_8 && python3 plot.py && mv soc_compare_tps.pdf fig8a.pdf && mv soc_compare_tpe.pdf fig8b.pdf

fig9:
	cd Figure_9 && python3 plot.py && mv output_bitrate.pdf fig9.pdf

fig10:
	cd Figure_10 && python3 plot.py && mv psnr.pdf fig10.pdf

fig11:
	cd Figure_11 && python3 plot_11a.py && mv dl_latency_all_onerow.pdf fig11a.pdf
	cd Figure_11 && python3 plot_11b.py && mv dl_tpe_all_onerow.pdf fig11b.pdf

fig12:
	cd Figure_12 && python3 plot.py && mv energy_scalability.pdf fig12.pdf

fig13:
	cd Figure_13 && python3 plot.py && mv soc_one.pdf fig13.pdf

clean:
	find . -name "*.pdf" -type f -delete