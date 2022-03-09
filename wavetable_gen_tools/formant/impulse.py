# Bandhlimited impulse train through 3 biquad formants
# Adapted from Julius O. Smith's formant filtering example
# formant filter frequencies from cSound appendix 
# fundamental adapted from samplerate/10 and appropriate wavetable size

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def psos2tf(sos, g):
    [nsecs, tmp] = sos.shape
    if nsecs < 1:
        B=[]
        A=[]
        return [B, A]
    Bs = sos[0:nsecs, 0:3]
    As = sos[0:nsecs, 3:6]
    B = Bs[0]
    A = As[0]
    for i in range(1, nsecs):
        B = np.convolve(B,As[i]) + np.convolve(A,Bs[i])
        A = np.convolve(A,As[i])
    return [B, A]

fs = 51400 # sample rate
nsamps = 6000

f0 = 100.00 # Pitch in Hz
w0T = 2*np.pi*f0/fs; # radians per sample

nharm = 17  # number of harmonics
sig = np.zeros(nsamps)
n = (map(float,range(0,(nsamps))))

text_file = open("impulse.txt", "a")

# Synthesize bandlimited impulse train

for j in xrange(2,int(nharm+2)):
    for i in xrange(1,j):
        harm = np.cos(map(lambda x: x*w0T*float(i), n))
        sig = sig + harm
    #plt.plot(n[0:129], sig[0:129])
    #plt.show()
    #sig = sig/np.max(sig)    
    out = sig[2570:2827]
    out = np.add(out, abs(np.min(out)))
    out = np.multiply(out, 1/(np.max(out)))
    out = np.multiply(out, -1)
    out = np.add(out, 1)
    plt.plot(n[2570:2827], out[0:257])
    out = np.multiply(out, 32767)
    out = np.int0(out)
    text_file.write("static const uint16_t impulse")
    text_file.write(str(j-1))
    text_file.write("[257] =")
    text_file.write(repr(out[0:257]))
    text_file.write('\n')

print(nharm)
plt.show()
text_file.close()
