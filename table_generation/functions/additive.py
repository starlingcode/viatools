import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import csv

domain = np.linspace(0, np.pi * 2, 512)

base_sine = -np.cos(domain) + 1

window = signal.tukey(512)

result = base_sine

tables = [(base_sine - 1)]

for i in range(1, 9):
    freq_x2 = (-np.cos(domain * 2 * i + np.pi) + 1)
    result = result + freq_x2 * window * 2
    tables.append(result*2/np.max(result) - 1)
    print(np.argmax(result))

for table in tables:
    with open("output/additive_evens.csv", "w") as output_file:
        output_write = csv.writer(output_file)
        for table in tables:
            output_write.writerow(table)
            plt.plot(table)

plt.show()