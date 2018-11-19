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
    num_harmonics = 4096

    # in case you need to make a noise record
    render_seconds = 4

    # use autocorrelation?
    use_auto_corr = True

    # number of most significant frequencies from which to choose the lowest
    fundamental_threshold = 16

    # lower the detected fundamental frequency
    period_multiply = 4

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

        print(freq)
        print(amplitude)

        write_array += np.sin(render_length/samplerate * 2 * np.pi * freq + phase_shift) * amplitude

    write_array = write_array / np.max(write_array)


    if use_auto_corr:

        peak_period = int(freq_est.period_from_autocorr(sample_buffer))

    else:

        # find the lowest frequency above a significance threshold

        base = 20000

        for freq in signficant_frequences[:fundamental_threshold]:

            if freq[0] < base and freq[0] != 0:

                base = freq[0]

        peak_period = int(samplerate/base) * period_multiply

    window = scipy.signal.tukey(peak_period)

    wavetable = write_array[:peak_period] * window

    repeat = 0

    wavetable_render = []

    while repeat < 500:

        for sample in wavetable:
            wavetable_render.append(sample)

        repeat += 1

    render = np.array(wavetable_render)

    wavetable_render = scipy.signal.resample(wavetable_render, 512*500)

    read_position = 512*3

    wavetable = wavetable_render[read_position: read_position + 512]

    # render
    sf.write("test_outputs/test_output_" + file_shorthand, write_array, samplerate)

    # render
    sf.write("wavetable_renders/wavetable_output_" + file_shorthand, wavetable_render, samplerate)

    return wavetable

table = input('Which subfolder in table_input should I use to make a Via wavetable: ')

table_samples = []

for sound in os.listdir("table_input/" + table):

    print(sound)

    table_samples.append(spectral_resynthesize("table_input/" + table + "/" + sound))

x = np.linspace(0, 512, 512)

with open("table_output/"+table+".csv", "w") as output:

    table_writer = csv.writer(output, delimiter=",")

    for table in table_samples:
        table_writer.writerow(table)
        plt.plot(x, table)

plt.show()