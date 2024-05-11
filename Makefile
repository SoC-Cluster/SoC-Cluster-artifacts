.PHONY: all

all: fig1 fig5 fig6 fig7 fig8 fig9 fig10 fig11 fig12 fig13

fig1:
    python3 Figure_1/plot.py

fig5:
    python3 Figure_5/plot.py

fig6:
    python3 Figure_6/plot_6a.py
    python3 Figure_6/plot_6b.py

fig7:
    python3 Figure_7/plot.py

fig8:
    python3 Figure_8/plot.py

fig9:
    python3 Figure_9/plot.py

fig10:
    python3 Figure_10/plot.py

fig11:
    python3 Figure_11/plot_11a.py
    python3 Figure_11/plot_11b.py

fig12:
	python3 Figure_12/plot.py

fig13:
	python3 Figure_13/plot.py

clean:
	rm Figure_1/*.pdf
	rm Figure_5/*.pdf
	rm Figure_6/*.pdf
	rm Figure_7/*.pdf
	rm Figure_8/*.pdf
	rm Figure_9/*.pdf
	rm Figure_10/*.pdf
	rm Figure_11/*.pdf
	rm Figure_12/*.pdf
	rm Figure_13/*.pdf