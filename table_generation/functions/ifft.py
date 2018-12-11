import numpy as np
from scipy import signal
from scipy import special
import csv
import matplotlib.pylab as plt



tables = []

input_domain = np.linspace(0, 2*np.pi, 32)

input_sig = np.sin(input_domain)
input_sig += np.sin(2.7438 * input_domain)

freqs = np.fft.fft(input_sig)
reconstruction = np.fft.ifft(freqs)

plt.subplot(2, 1, 1)
plt.plot(freqs)
plt.subplot(2, 1, 2)
plt.plot(input_sig)
plt.subplot(2, 1, 2)
plt.plot(reconstruction)


# with open("output/sin_phase_shift.csv", "w") as output_file:
#
#     output_write = csv.writer(output_file)
#     for table in tables:
#         output_write.writerow(table)

plt.show()