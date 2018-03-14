# Model a saw wave through an idealized transistor ladder filter
# Transfer function courtesy of Tim Stinchecomb

from scipy import signal
import numpy
import matplotlib.pyplot as plt

# set a resonance value between 1 and 5
resonance = 2

# set the constants for the polynomial
# in the numerator and denominator of 
# the transfer function
num = [1]
den = [1, 4, 6, 4, resonance]

# construct the transfer function
system = signal.TransferFunction(num, den)

for i in range(0,9):
# define an oscillator frequency. filter cutoff is 1
    freq = (1.5**i)*.01

# define the timebase of the simulation
    t = numpy.linspace(0, (6 * numpy.pi) / freq, 387)

# generate a sawtooth using our timebase
# default period is 2pi. 
# scale our time array to change frequency
#    u = (2**14) * (signal.sawtooth(t * freq))
    u = (2**14) * (signal.square(t * freq))

# perform our simulation
    tout, y, x = signal.lsim(system, u, t)

# print a nice array of integers chopping out an attack and release slope
    intcopy = numpy.rint(y) + 2**14
    attackside = intcopy[258:323]
    releaseside = numpy.flip(intcopy[322:387], 0)
    print(numpy.array2string(attackside, separator=', '))
    print(numpy.array2string(releaseside, separator=', '))


# plot our simulated output and input
plt.plot(t, y)
plt.plot(t, u)
plt.show()


