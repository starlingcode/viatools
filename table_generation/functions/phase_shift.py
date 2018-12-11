import numpy as np
from scipy import signal
from scipy import special
import csv
import matplotlib.pylab as plt

tables = []

plot_space = np.linspace(0, 1, 512)

for offset in range(0,5):

    start = (offset/5) * 2*np.pi;

    end = 2*np.pi + start

    domain = np.linspace(start, end, 512)

    sine_window = np.sin(domain)

    tables.append(sine_window)

    print(sine_window)

    plt.plot(plot_space, sine_window)

with open("output/sin_phase_shift.csv", "w") as output_file:

    output_write = csv.writer(output_file)
    for table in tables:
        output_write.writerow(table)

plt.show()