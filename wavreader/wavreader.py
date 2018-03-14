import numpy as np
from scipy.io import wavfile
from scipy import signal


sampleRate, sampleData = wavfile.read("MaxV - PACBD.wav")

peaks = signal.argrelextrema(np.absolute(sampleData), np.greater)

print(sampleRate)

print(peaks)