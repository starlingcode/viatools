import numpy as np
from scipy import special
import matplotlib.pylab as plt

domain = np.linspace(0, 2 *np.pi, 512)

sinc_write = special.sinc(domain)

plt.plot(domain, sinc_write)

plt.show()