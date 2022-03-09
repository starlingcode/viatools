import numpy as np
import matplotlib.pylab as plt
from scipy import signal
import csv

tables = []

write = np.zeros(512)
domain = np.linspace(-2*np.pi, 2*np.pi, 512)
np.sinh(domain, write)
tables.append(write)

write = np.zeros(512)
domain = np.linspace(-np.pi, np.pi, 512)
np.sinh(domain, write)
tables.append(write)

tables.append(domain)

write = np.zeros(512)
domain = np.linspace(-np.pi * 0.5, np.pi * 0.5, 512)
np.tanh(domain, write)
tables.append(write)

write = np.zeros(512)
domain = np.linspace(-np.pi, np.pi, 512)
np.tanh(domain, write)
tables.append(write)

with open("output/hyperbolic_shapers.csv", "w") as output_file:

    output_write = csv.writer(output_file)
    for table in tables:
        plt.plot(domain, table / np.max(table))
        output_write.writerow(table)

plt.show()

