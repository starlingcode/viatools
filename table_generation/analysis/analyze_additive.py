import soundfile as sf
import scipy
from scipy import fftpack
import matplotlib.pylab as plt

from scipy import signal
import numpy as np


file_name = "foghorn"  # without extension

# number of additive partials
num_harmonics = 4096

# in case you need to make a noise record
render_seconds = 4

# number of most significant frequencies from which to choose the lowest
fundamental_threshold = 64

# lower the detected fundamental frequency
period_multiply = 2

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

while repeat < 1000:

    for sample in wavetable:
        wavetable_render.append(sample)

    repeat += 1

# render
sf.write("test_output_" + file_name + ".wav", write_array, samplerate)

# render
sf.write("wavetable_output_" + file_name + ".wav", wavetable_render, samplerate)

plt.plot(np.linspace(0, peak_period, peak_period), wavetable)
plt.show()

