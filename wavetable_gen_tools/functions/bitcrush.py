import numpy as np
import matplotlib.pylab as plt
from scipy import signal
import csv

domain = np.linspace(0, 32767, 512)

tables = []

for i in range(0,5):

    output = []

    for sample in domain:

        output.append(int(sample) & ~int(2**(14 - i) - 1))

    tables.append(output)

with open("output/bitcrush.csv", "w") as output_file:

    output_write = csv.writer(output_file)
    tables.reverse()
    for table in tables:
        plt.plot(domain, table)
        output_write.writerow(table)

plt.show()

