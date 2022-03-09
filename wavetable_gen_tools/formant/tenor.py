# Bandhlimited impulse train through 3 biquad formants
# Adapted from Julius O. Smith's formant filtering example
# formant filter frequencies from cSound appendix 
# fundamental adapted from samplerate/10 and appropriate wavetable size

# tenor (rendered with 109.090909 Hz fundamental)
ta = ([650.0, 1080.0, 2650.0, 2900.0, 3250.0])
tabw = ([80.0, 90.0, 120.0, 130.0, 140.0])
te = ([400.0, 1700.0, 2600.0, 3200.0, 3580.0])
tebw = ([70.0, 80.0, 100.0, 120.0, 120.0])
ti = ([290.0, 1870.0, 2800.0, 3250.0, 3540.0])
tibw = ([40.0, 90.0, 100.0, 120.0, 120.0])
to = ([400.0, 800.0, 2600.0, 2800.0, 3000.0])
tobw = ([40.0, 80.0, 100.0, 120.0, 120.0])
tu = ([350.0, 600.0, 2700.0, 2900.0, 3300.0])
tubw = ([40.0, 80.0, 100.0, 120.0, 120.0])

# tenor, 3 formant
t3a = ([650.0, 1080.0, 2650.0,])
t3abw = ([80.0, 90.0, 120.0])
t3e = ([400.0, 1700.0, 2600.0])
t3ebw = ([70.0, 80.0, 100.0])
t3i = ([290.0, 1870.0, 2800.0])
t3ibw = ([40.0, 90.0, 100.0])
t3o = ([400.0, 800.0, 2600.0])
t3obw = ([40.0, 80.0, 100.0])
t3u = ([350.0, 600.0, 2700.0])
t3ubw = ([40.0, 80.0, 100.0])

# soprano (rendered with 218.181818 Hz fundamental)
sa = ([800.0, 1150.0, 2900.0, 3900.0, 4950.0])
sabw = ([80.0, 90.0, 120.0, 130.0, 140.0])
se = ([350.0, 2000.0, 2800.0, 3600.0, 4950.0])
sebw = ([60.0, 100.0, 120.0, 150.0, 200.0])
si = ([270.0, 2140.0, 2950.0, 3900.0, 4950.0])
sibw = ([60.0, 90.0, 100.0, 120.0, 120.0])
so = ([450.0, 800.0, 2830.0, 3800.0, 4950.0])
sobw = ([70.0, 80.0, 100.0, 130.0, 135.0])
su = ([325.0, 700.0, 2700.0, 3800.0, 4950.0])
subw = ([50.0, 60.0, 170.0, 180.0, 200.0])

# soprano, 3 formant
s3a = ([800.0, 1150.0, 2900.0])
s3abw = ([80.0, 90.0, 120.0])
s3e = ([350.0, 2000.0, 2800.0])
s3ebw = ([60.0, 100.0, 120.0])
s3i = ([270.0, 2140.0, 2950.0])
s3ibw = ([60.0, 90.0, 100.0])
s3o = ([450.0, 800.0, 2830.0])
s3obw = ([70.0, 80.0, 100.0])
s3u = ([325.0, 700.0, 2700.0])
s3ubw = ([50.0, 60.0, 170.0])


# soprano (rendered with 218.181818 Hz fundamental)
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

F = np.asarray(a1)
BW = np.asarray(a1bw)
name = "artificial1"
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

text_file = open("artif.txt", "a")

# Synthesize bandlimited impulse train

limits = [12, 16, 24, 60]
for limit in limits:
	for j in xrange(1, limit+1):
		for i in xrange(1,int(j+1)):
   		 	harm = np.cos(map(lambda x: x*w0T*float(i), n))
    			sig = sig + harm
		print(i)
		sig = sig/np.max(sig)    
	speech = signal.lfilter([1],A,sig);
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
# attack
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
# decay
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
plt.show()
text_file.close()
