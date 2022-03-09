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

peak_period = 512

in_fade = np.linspace(0.0, 1.0, peak_period)
out_fade = np.linspace(1.0, 0.0, peak_period)

table_samples = []

start = 512

wavetable = sample_buffer[start + peak_period: start + 2 * peak_period] * out_fade
last_table = sample_buffer[start:start + peak_period] * in_fade

# wavetable += last_table

repeat = 0

wavetable_render = []

while repeat < 500:

    for sample in wavetable:
        wavetable_render.append(sample)

    repeat += 1

render = np.array(wavetable_render)

table_name = input("What shall we call it?")

with open("table_output/" + table_name + ".csv", "w") as output:

    table_writer = csv.writer(output, delimiter=",")

    for table in table_samples:

        table_writer.writerow(table)

sf.write("test_outputs/" + table_name + ".wav", render, samplerate)







