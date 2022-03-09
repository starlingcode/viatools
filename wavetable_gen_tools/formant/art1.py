# Bandhlimitedimpulse train through 3 biquad formants
# Adapted from Julius O. Smith's formant filtering example
# formant filter frequencies from cSound appendix 
# fundamental adapted from samplerate/10 and appropriate wavetable size

# artificial formants (bandpass filter bank)       
a1 = ([200.0, 300.0, 500.0, 700.0, 900.0])
a1bw = ([50.0, 75.0, 100.0, 150.0, 200.0])
a2 = ([400.0, 600.0, 800.0, 1000, 1200.0])
a2bw = ([75.0, 125.0, 150.0, 200.0, 300.0])
a3 = ([500.0, 900.0, 1300.0, 1500.0, 1900.0])
a3bw = ([100.0, 150.0, 200.0, 250.0, 375.0])
a4 = ([600.0, 1200.0, 1800.0, 2400.0, 3600.0])
a4bw = ([150.0, 200.0, 250.0, 350.0, 500.0])
a5 = ([900.0, 1500.0, 3000.0, 5000.0, 7000.0])
a5bw = ([200.0, 250.0, 350.0, 500.0, 1000.0])


spread1 = ([100.0, 200.0, 300.0, 400.0, 500.0])
spread1bw = ([25.0, 50.0, 75.0, 100.0, 125.0])
a2 = ([400.0, 600.0, 800.0, 1000, 1200.0])
a2bw = ([75.0, 125.0, 150.0, 200.0, 300.0])
a3 = ([500.0, 900.0, 1300.0, 1500.0, 1900.0])
a3bw = ([100.0, 150.0, 200.0, 250.0, 375.0])
a4 = ([600.0, 1200.0, 1800.0, 2400.0, 3600.0])
a4bw = ([150.0, 200.0, 250.0, 350.0, 500.0])
a5 = ([900.0, 1500.0, 3000.0, 5000.0, 7000.0])
a5bw = ([200.0, 250.0, 350.0, 500.0, 1000.0])

#a6 = ([1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0, 1700.0, 1800.0, 1900.0])
#a6bw = ([55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0])
a6 = ([1000.0, 1500.0, 2000.0, 2500.0, 3000.0])
a6bw = ([50.0, 75.0, 100.0, 125.0, 150.0])
scaleFactor = .4 
scaledbw = list(map(lambda x: x*scaleFactor, a6bw))
scaledfreq = list(map(lambda x: x*scaleFactor, a6))

name = "fbank9"

"""
OldRange = (max(spread1) - min(spread1))

for each spread in spread1:
	newspread
  
NewRange = (NewMax - NewMin)  
NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
"""

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

F = np.asarray(scaledfreq)
BW = np.asarray(scaledbw)

#F = np.asarray([700.0, 1220.0, 2600.0, 350.0]) # formant frequencies (Hz)
#BW = np.asarray([130.0, 70.0, 160.0, 110.0]) # formant bandwidths (Hz)
fs = 25600 # sample rate

nsecs = F.size
R = np.exp(-np.pi*BW/fs)
theta = 2*np.pi*F/fs
poles = np.multiply(R, np.exp(1j*theta)) # complex poles
B = 1
polesMatrix = np.matrix([poles, np.conj(poles)])
A = np.real(np.poly(polesMatrix.A1))

w, h = signal.freqz(B, A)

"""
freqPlot = plt.figure();
plt.title('Formant Filter Frequency Response')
ax1 = freqPlot.add_subplot(111)
plt.plot(w, 20 * np.log10(abs(h)), 'b')
plt.ylabel('amplitude[dB]', color = 'b')
plt.xlabel('frequency [rad/sample]')
ax2 = ax1.twinx()
angles = np.unwrap(np.angle(h))
plt.plot(w, angles, 'g')
plt.ylabel('Angle (radians)', color='g')
plt.grid()
plt.axis('tight')
plt.show()
"""

# convert to parallel complex one-poles (PFE):
[r, p, f] = signal.residuez([B], A)
As = np.zeros((nsecs,3), dtype=complex)
Bs = np.zeros((nsecs,3), dtype=complex)

#complex-conjugate pairs are adjacent in r and p:
for i in xrange (0, nsecs):
    k = i*2
    Bs[i] = [r[k]+r[k+1], -(r[k+1]*p[k]+r[k]*p[k+1]), 0]
    As[i] = [1, -(p[k]+p[k+1]), p[k]*p[k+1]]


sos = np.concatenate((Bs, As), axis=1) # standard second order system form (n*6 matrix)
iperr = np.linalg.norm(np.imag(sos) / np.linalg.norm(sos)) # make sure sos is ~real
sos = np.real(sos)


[Bh,Ah] = psos2tf(sos, 1)

# now synthesize the vowel

nsamps = 8000
f0 = 100.00 # Pitch in Hz
w0T = 2*np.pi*f0/fs; # radians per sample

nharm = np.floor((fs/2)/f0)  # number of harmonics
sig = np.zeros(nsamps)
n = (map(float,range(0,(nsamps))))

text_file = open("comb1.txt", "a")

# Synthesize bandlimited impulse train

limits = [24, 48]
for limit in limits:
	for j in xrange(1, limit+1):
		for i in xrange(1,int(j+1)):
   		 	harm = np.cos(map(lambda x: x*w0T*float(i), n))
    			sig = sig + harm
		print(i)
		sig = sig/np.max(sig)    
	speech = signal.filtfilt([1],A,sig);
#		plt.plot(n[0:256], sig[0:256])
	out = speech[4864:5121]
	#plt.plot(out[0:257])
	out = np.add(out, abs(np.min(out)))
	out = np.multiply(out, 1/(np.max(out)))
	out = np.multiply(out, -1)
	out = out + 1
	out = np.multiply(out, 32767)
	plt.plot(out[0:257])
	out = np.int0(out)
# symmetric
	text_file.write('static const uint16_t ')
	text_file.write(name)
	text_file.write(str(limit))
	text_file.write('Atk')
	text_file.write('[129] = {')
	for x in xrange(0, 129):
        	text_file.write(str(out[x]))
        	if x != 128:
               		text_file.write(', ')
	text_file.write('};\n')
"""# decay
	text_file.write('static const uint16_t ')
	text_file.write(name)
	text_file.write(str(limit))
	text_file.write('Rls')
	text_file.write('[129] = {')
	for x in reversed(xrange(128, 257)):
       		text_file.write(str(out[x]))
       		if x != 128:
               		text_file.write(', ')
	text_file.write('};\n')
"""
plt.show()

text_file.close()

