# Bandlimited impulse train table family generator
# ascending from single harmonic to table size
# fundamental adapted from samplerate/10 and appropriate wavetable size

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

output_samples = 257
nsamps = output_samples * 10 + output_samples # extra samples so system can settle (causal filtering)

f0 = 100.00 # Pitch in Hz
fs = (output_samples)*f0*2 # sample rate is calculated per pitch and output table length, *2 so we get half the period
w0T = 2*np.pi*f0/fs; # radians per sample
nharm = 17  # number of harmonics (family size)
sig = np.zeros(nsamps)
n = (map(float,range(0,(nsamps))))

text_file = open("impulse.txt", "a")

# Synthesize bandlimited impulse train

for limit in xrange(2,int(nharm+2)):  # generate each table

    for i in xrange(1,limit): # summing each of the harmonics
        harm = np.cos(map(lambda x: x*w0T*float(i), n))
        sig = sig + harm

    offset = 10*output_samples ## for getting a result after the beginning
    out = sig[offset:offset + (output_samples)] # retrieve our samples
    out = np.add(out, abs(np.min(out))) #shift so lowest value is 0
    out = np.multiply(out, 1/(np.max(out))) #divide by max for 0-1 normalization
    out = np.multiply(out, -1) #invert
    out = np.add(out, 1) #add 1 to flip the table
    plt.plot(xrange(0, output_samples), out[0:output_samples])
    out = np.multiply(out, 32767) #scale to 15-bit value
    out = np.int0(out) #and constrain to integer
    text_file.write("static const uint16_t imp")
    text_file.write(str(output_samples))
    text_file.write("_")
    text_file.write(str(limit-1))
    text_file.write("[")
    text_file.write(str(output_samples))
    text_file.write("] = {")
    for x in xrange(0, output_samples):
                text_file.write(str(out[x]))
                if x != output_samples-1:
                        text_file.write(', ')
    text_file.write('};\n')

print(nharm)
plt.show()
text_file.close()
