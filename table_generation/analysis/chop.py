import soundfile as sf
import scipy
from scipy import fftpack
from tkinter import filedialog
from tkinter import messagebox
import csv
import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from scipy import signal
import numpy as np

import freq_est

messagebox.showinfo("Choose file", "Hello, please choose a wav file")
file_name = filedialog.askopenfilename(message="")

file_shorthand = file_name.split("/")[-1]

# get the raw samples and sample rate of the wav file
samples, samplerate = sf.read(file_name)
num_channels = samples[0].size

# grab just the left channel from stereo
sample_buffer = []

if num_channels is not 1:
    for sample in samples:
        sample_buffer.append(sample[0])
else:
    for sample in samples:
        sample_buffer.append(sample)

results = freq_est.period_from_autocorr(sample_buffer)
peak_period = int(results[0])
start = results[1]

in_fade = np.linspace(0.0, 1.0, peak_period)
out_fade = np.linspace(1.0, 0.0, peak_period)

wavetable = sample_buffer[start + peak_period: start + 2 * peak_period] * out_fade
last_table = sample_buffer[start:start + peak_period] * in_fade

wavetable += last_table

repeat = 0

wavetable_render = []

while repeat < 500:

    for sample in wavetable:
        wavetable_render.append(sample)

    repeat += 1

render = np.array(wavetable_render)

wavetable_render = scipy.signal.resample(wavetable_render, 512 * 500)

read_position = 512 * 3

wavetable = wavetable_render[read_position: read_position + 512]

# render
sf.write("test_chop1, wavetable_render, samplerate)

