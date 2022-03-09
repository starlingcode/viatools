import numpy as np
from scipy import signal
from scipy import special
import csv
import matplotlib.pylab as plt

tables = []

#endpoints = [7.5, 14.3, 20.8, 27.2, 33.5]



plot_space = np.linspace(0, 1, 512)

for order in range(0,5):

    domain = np.linspace(0, 10*np.pi, 512)

    bessel = special.jv(order * 2, domain)

    tables.append(bessel)

    print(bessel)

    plt.plot(plot_space, bessel)

with open("output/bessel_1_alt.csv", "w") as output_file:

    output_write = csv.writer(output_file)
    for table in tables:
        output_write.writerow(table)

plt.show()