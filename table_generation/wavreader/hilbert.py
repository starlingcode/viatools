### tool for extracting the amplitude curve of an sample into Via envelopes

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, savgol_filter, argrelextrema, resample
from scipy.io import wavfile

def normalize_to_15bit(input):
    normalized = input - np.amin(input)
    normalized = (normalized/np.amax(normalized))*32767
    return normalized


def make_release_slope(input_array, table_size):

    max_index = np.nanargmax(input_array)
    min_index = np.nanargmin(input_array[max_index:])
    slope_raw = input_array[max_index:min_index]

    if (np.size(slope_raw) >= table_size):
        release_slope = np.zeros(table_size)
        for i in range(table_size):
             release_slope[i] = slope_raw[int((i * np.size(slope_raw)) / table_size)]

    else:

        release_slope = np.interp(range(table_size), range(np.size(slope_raw)), slope_raw)

    normalize_to_15bit(release_slope)

    return release_slope

def make_attack_slope(input_array, table_size):

    input_array = input_array[np.nonzero(input_array)]
    max_index = np.nanargmax(input_array)
    slope_raw = input_array[0:max_index]

    if (np.size(slope_raw) >= table_size):
        attack_slope = np.zeros(table_size)
        for i in range(table_size):
            attack_slope[i] = slope_raw[int((i * np.size(slope_raw)) / table_size)]

    else:

        attack_slope = np.interp(range(table_size), range(np.size(slope_raw)), slope_raw)

    normalize_to_15bit(attack_slope)

    return attack_slope

def calculate_rms(input_signal):
    
    calc = np.zeros(np.size(input_signal))

    running_sum = 0.0
    
    for i in range(1023):
        running_sum = running_sum + input_signal[i] ** 2

    for i in range(np.size(signal)):
        if (i - 1023) < 0:
            running_sum = running_sum + input_signal[i + 1024] ** 2
            calc[i] = np.sqrt(running_sum / 2048.0)
        elif (i + 1024) < np.size(signal):
            running_sum = running_sum + (input_signal[i + 1024] ** 2) - (input_signal[i - 1023] ** 2)
            calc[i] = np.sqrt(running_sum / 2048.0)
        else:
            running_sum = running_sum - input_signal[i - 1023] ** 2
            calc[i] = np.sqrt(running_sum / 2048.0)
    
    return calc


family_name = "testRMS"

sample_files = ["808kick16bit", "CLA76_1_16bit", "CLA76_CLA2A_1_16bit", "piano16bit", "bassplck16bit"]

text_file = open(family_name + ".csv", "w")
text_file.truncate()

for sample_file in sample_files:

    table_size = 257

    sample_rate, sample_data = wavfile.read(sample_file + ".wav")

    signal = sample_data

    t = range(np.size(signal))
    slope_length = range(table_size)


    analytic_signal = hilbert(signal)
    amplitude_envelope = np.abs(analytic_signal)

    rms = calculate_rms(signal)
    hilbert_rms = calculate_rms(signal)
    #hilbert_rms = calculate_rms(hilbert_rms) #add to further smooth hilbert approx

    hilbert_maxima_indices = argrelextrema(np.abs(hilbert_rms), np.greater)
    hilbert_maxima_values = np.abs(hilbert_rms[hilbert_maxima_indices[0]])
    hilbert_peaks = np.interp(t, hilbert_maxima_indices[0], hilbert_maxima_values)

    signal_maxima_indices = argrelextrema(np.abs(signal), np.greater)
    signal_maxima_values = np.abs(signal[signal_maxima_indices[0]])
    signal_peaks = np.interp(t, signal_maxima_indices[0], signal_maxima_values)

    hilbert_release = make_release_slope(amplitude_envelope, table_size)
    hilbert_release = savgol_filter(hilbert_release, 37, 2, 0, 1.0, 0, "nearest")
    hilbert_release = normalize_to_15bit(hilbert_release)
    peak_release = make_release_slope(signal_peaks, table_size)
    peak_release = savgol_filter(peak_release, 37, 2, 0, 1.0, 0, "nearest")
    peak_release = normalize_to_15bit(peak_release)
    rms_release = make_release_slope(rms, table_size)
    rms_release = savgol_filter(rms_release, 37, 2, 0, 1.0, 0, "nearest")
    rms_release = normalize_to_15bit(rms_release)
    hilbert_rms_release = make_release_slope(hilbert_rms, table_size)
    hilbert_rms_release = savgol_filter(hilbert_rms_release, 37, 2, 0, 1.0, 0, "nearest")
    hilbert_rms_release = normalize_to_15bit(hilbert_rms_release)


    hilbert_attack = make_attack_slope(amplitude_envelope, table_size)
    hilbert_attack = savgol_filter(hilbert_attack, 37, 2, 0, 1.0, 0, "nearest")
    hilbert_attack = normalize_to_15bit(hilbert_attack)
    peak_attack = make_attack_slope(signal_peaks, table_size)
    peak_attack = savgol_filter(peak_attack, 37, 2, 0, 1.0, 0, "nearest")
    peak_attack = normalize_to_15bit(peak_attack)
    rms_attack = make_attack_slope(rms, table_size)
    rms_attack = savgol_filter(rms_attack, 37, 2, 0, 1.0, 0, "nearest")
    rms_attack = normalize_to_15bit(rms_attack)



    fig = plt.figure()
    ax0 = fig.add_subplot(311)
    ax0.plot(t, signal, label='signal')
    ax0.plot(t, amplitude_envelope, label='envelope')
    ax0.plot(t, hilbert_rms, label='envelopeAverage')
    ax0.plot(t, signal_peaks, label='localPeaks')
    ax0.plot(t, rms, label='rms')
    ax0.plot(t, hilbert_peaks, label='hilbertPeaks')
    ax0.set_xlabel("time in samples")
    ax0.legend()
    ax1 = fig.add_subplot(312)
    ax1.plot(slope_length, hilbert_release, label='hilbert')
    ax1.plot(slope_length, peak_release, label='peak')
    ax1.plot(slope_length, rms_release, label='rms')
    # ax1.plot(slope_length, hilbert_rms_release, label='hilbert_rms')
    ax1.set_xlabel("time in samples")
    ax1.legend()
    ax2 = fig.add_subplot(313)
    ax2.plot(slope_length, hilbert_attack, label='hilbert')
    ax2.plot(slope_length, peak_attack, label='peak')
    ax2.plot(slope_length, rms_attack, label='rms')
    ax2.set_xlabel("time in samples")
    ax2.legend()
    plt.show()

    # attack
    text_file.write(sample_file)
    text_file.write('RMSAtk,')
    for x in range(0, table_size):
            text_file.write(str(int(rms_attack[x])))
            if x != table_size-1:
                    text_file.write(',')

    text_file.write('\n')

    text_file.write(sample_file)
    text_file.write('RMSRls,')

    for x in range(0, table_size):
            text_file.write(str(int(rms_release[table_size - 1 - x])))
            if x != table_size-1:
                    text_file.write(',')

    text_file.write('\n')

text_file.write(family_name + "RMSAtk,")

for sample in sample_files:
    text_file.write(sample + "RMSAtk,")

text_file.write("\n")

text_file.write(family_name + "RMSRls,")

for sample in sample_files:
    text_file.write(sample + "RMSRls,")



# # attack
# text_file.write('static const uint16_t ')
# text_file.write(sample_file)
# text_file.write('PeakAtk')
# text_file.write('[')
# text_file.write(str(table_size))
# text_file.write('] = {')
#
# for x in range(0, table_size):
#         text_file.write(str(int(peak_attack[x])))
#         if x != table_size-1:
#                	text_file.write(', ')
#
# text_file.write('};\n')
#
# text_file.write('static const uint16_t ')
# text_file.write(sample_file)
# text_file.write('PeakRls')
# text_file.write('[')
# text_file.write(str(table_size))
# text_file.write('] = {')
#
# for x in range(0, table_size):
#         text_file.write(str(int(peak_release[table_size - 1 - x])))
#         if x != table_size-1:
#                	text_file.write(', ')
#
# text_file.write('};\n')
#
# # attack
# text_file.write(sample_file)
# text_file.write('HilbertAtk, ')
# text_file.write(str(table_size))
# text_file.write('] = {')
#
# for x in range(0, table_size):
#         text_file.write(str(int(hilbert_attack[x])))
#         if x != table_size-1:
#                	text_file.write(', ')
#
# text_file.write('};\n')
#
# text_file.write('static const uint16_t ')
# text_file.write(sample_file)
# text_file.write('HilbertRls')
# text_file.write('[')
# text_file.write(str(table_size))
# text_file.write('] = {')
#
# for x in range(0, table_size):
#         text_file.write(str(int(hilbert_release[table_size - 1 - x])))
#         if x != table_size-1:
#                	text_file.write(', ')
#
# text_file.write('};\n')

