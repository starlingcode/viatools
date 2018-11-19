import soundfile as sf
import scipy
from scipy import fftpack
import matplotlib.pylab as plt

from scipy import signal
import numpy as np

file_name = "future_exceprt_2"  # without extension

# get the raw samples and sample rate of the wav file
samples, samplerate = sf.read(file_name + ".wav")
num_channels = samples[0].size

# grab just the left channel from stereo
sample_buffer = []

if num_channels is not 1:
    for sample in samples:
        sample_buffer.append(sample[0])
else:
    for sample in samples:
        sample_buffer.append(sample)

