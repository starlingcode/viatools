# Bandhlimited impulse train through 3 biquad formants
# Adapted from Julius O. Smith's formant filtering example
# formant filter frequencies from cSound appendix 
# fundamental adapted from samplerate/10 and appropriate wavetable size

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

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

F = np.asarray(ta) # formant frequencies (Hz)
BW = np.asarray(tabw) # formant bandwidths (Hz)
name = "tenorA"
text_file = open("tenorA_formant.txt","a")

f0 = 100 # fundamental pitch of excitation impulse
nharm = 30 # number of harmonics in impulse
nsamps = 8000 # number of samples to collect
output_samples = 512 # number of samples per table (attack AND decay)
table_size = 257 # length of each wavetable
nsamps = output_samples * 11 # number of samples to process. offset = 10 cycles, + output 
fs = output_samples*f0 # sample rate

nsecs = F.size
R = np.exp(-np.pi*BW/fs)
theta = 2*np.pi*F/fs
poles = np.multiply(R, np.exp(1j*theta)) # complex poles
B = 1
polesMatrix = np.matrix([poles, np.conj(poles)])
A = np.real(np.poly(polesMatrix.A1))
w, h = signal.freqz(B, A)


"""

# plot formant filter frequency response

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

w0T = 2*np.pi*f0/fs; # radians per sample
sig = np.zeros(nsamps)
n = (map(float,range(0,(nsamps))))

# Synthesize bandlimited impulse train

for j in xrange(1, nharm+1):
	for i in xrange(1,int(j+1)):
 	 	harm = np.cos(map(lambda x: x*w0T*float(i), n))
  		sig = sig + harm
	print(i)
	sig = sig/np.max(sig)    
sig = (sig * -1) + 1
speech = np.zeros(nsamps)
speech = signal.lfilter([1],A,sig);
#plt.plot(n[offset:offset+output_samples], sig[offset:offset+output_samples])
phasecorrection = output_samples - 52
range = speech[8*output_samples:10*output_samples];
offset = 8*output_samples + np.amin(np.argmax(range)); # for getting a result after the beginning
out = speech[offset:offset + output_samples]; # retrieves our samples for a and r
#plt.plot(out)
out = np.add(out, abs(np.amin(out))) # shift so lowest value is 0
out = np.multiply(out, 1/(np.max(out))) # divide by max for 0-1 normalization
out = np.multiply(out, -1) # invert
out = np.add(out, 1) # add 1 to flip the table
#plt.plot(out[0:output_samples])
out = np.multiply(out, 32767) # scale to 15-bit value
out = np.int0(out) # and constrain to integer
#plt.plot(out[offset:offset+output_samples])
plt.plot(out[0:output_samples])
# attack
text_file.write('static const uint16_t ')
text_file.write(name)
text_file.write(str(table_size))
text_file.write('Atk')
text_file.write('[')
text_file.write(str(table_size))
text_file.write('] = {')

for x in xrange(0, table_size):
        text_file.write(str(out[x]))
        if x != table_size-1:
               	text_file.write(', ')

text_file.write('};\n')
# decay
text_file.write('static const uint16_t ')
text_file.write(name)
text_file.write(str(table_size))
text_file.write('Rls')
text_file.write('[')
text_file.write(str(table_size))
text_file.write('] = {')

for x in reversed(xrange(table_size, output_samples)):
       	text_file.write(str(out[x]))
       	if x != table_size:
               	text_file.write(', ')

text_file.write('};\n')

plt.show()
text_file.close()
