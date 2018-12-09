import numpy as np
import matplotlib.pylab as plt
from scipy import signal
import csv

domain = np.linspace(-np.pi, np.pi, 512)

tables = []

for i in range(0,5):

    tanh_write = np.zeros(512)
    np.tanh(domain, tanh_write)

    sine = np.sin(i*domain)
    window = signal.triang(512)

    output = tanh_write + (.25 * sine * window)

    plt.plot(domain, tanh_write)
    plt.plot(domain, output)

    tables.append(output)

plt.show()

with open("output/tanh_res.csv", "w") as output_file:

    output_write = csv.writer(output_file)
    for table in tables:
        output_write.writerow(table)

