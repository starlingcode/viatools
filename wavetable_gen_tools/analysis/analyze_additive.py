import soundfile as sf
import scipy
from scipy import fftpack
import matplotlib.pylab as plt

from scipy import signal
import numpy as np

import os

import csv

import freq_est


def spectral_resynthesize(file_name):

    file_shorthand = file_name.split("/")[-1]

    # number of additive partials
    num_harmonics = 256

    # "lowpass filter" as multiple of fundamental
    cutoff_overtone = 64

    # in case you need to make a noise record
    render_seconds = 4

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
    base_period = int(results[0])

    base_freq = samplerate/base_period

    print(base_freq)

    window = scipy.signal.blackmanharris(len(sample_buffer))

    fft = scipy.fftpack.fft(sample_buffer * window)

    # we just need one half
    fft = fft[:len(fft) >> 1]

    # get human readable frequencies and complex value for each bin
    freq_value_list = []

    for bin, value in enumerate(fft):

        normalized_freq = bin / (len(fft) * 2)

        normalized_freq *= samplerate

        freq_value_list.append([normalized_freq, value])

    # sort that for amplitude
    freq_value_list.sort(key=lambda r: np.real(r[1]))

    # discard all but the most signficant
    if num_harmonics > len(freq_value_list):
        num_harmonics = len(freq_value_list)

    signficant_frequences = freq_value_list[:num_harmonics]

    # render the additive sample
    render_length = np.linspace(0, samplerate * render_seconds, samplerate * render_seconds)

    write_array = np.zeros(samplerate * render_seconds)

    for value in signficant_frequences:

        amplitude = np.real(value[1])
        phase_shift = np.imag(value[1]) * 2 * np.pi
        freq = value[0]

        if freq < (base_freq * cutoff_overtone):

            write_array += np.sin(render_length/samplerate * 2 * np.pi * freq + phase_shift) * amplitude

    write_array = write_array / np.max(write_array)

    results = freq_est.period_from_autocorr(sample_buffer)
    peak_period = int(results[0])
    start = results[1]

    print("made it")

    in_fade = np.linspace(0.0, 1.0, peak_period)
    out_fade = np.linspace(1.0, 0.0, peak_period)

    wavetable = write_array[start + peak_period: start + 2*peak_period] * out_fade
    last_table = write_array[start:start + peak_period] * in_fade

    wavetable += last_table

    repeat = 0

    print(wavetable)

    wavetable_render = []

    while repeat < 500:

        print(repeat)

        for sample in wavetable:
            wavetable_render.append(sample)

        repeat += 1

    wavetable_render = scipy.signal.resample(wavetable_render, 512*500)

    print("resampled")

    read_position = 512*3

    wavetable = wavetable_render[read_position: read_position + 512]

    print("made it again 2")

    # render
    sf.write("test_outputs/test_output_" + file_shorthand, write_array, samplerate)

    # render
    sf.write("wavetable_renders/wavetable_output_" + file_shorthand, wavetable_render, samplerate)

    return wavetable, 0

table = input('Which subfolder in table_input should I use to make a Via wavetable: ')

table_samples = []

for sound in os.listdir("table_input/" + table):

    if sound != ".DS_Store":

        print(sound)

        analyze = spectral_resynthesize("table_input/" + table + "/" + sound)

        table_samples.append(analyze[0])
        print("spectral density = " + str(np.average(analyze[1])))

x = np.linspace(0, 1024, 1024)

with open("table_output/"+table+".csv", "w") as output:

    table_writer = csv.writer(output, delimiter=",")

    for table in table_samples:
        table_writer.writerow(table)
        two_tables = np.zeros(1024)
        two_tables[:512] = table
        two_tables[512:1024] = table
        plt.plot(x, two_tables)


plt.show()