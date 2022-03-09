### tool for extracting the amplitude curve of an sample into Via envelopes

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, savgol_filter, argrelextrema, resample
from scipy.io import wavfile
import os
import csv

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

def csv_to_array(filename):

    table = []

    with open(filename, "r") as csv_input:

        table_reader = csv.reader(csv_input, delimiter=",")
        for row in table_reader:
            if row[0] != "":
                table.append(row)

    return table

def array_to_csv(table, filename):

    with open(filename, "w") as csv_output:

        table_writer = csv.writer(csv_output, delimiter=",")
        for row in table:
            table_writer.writerow(row)

family_name = input("which table: ")

sample_files = []

for root, dirs, files in os.walk("input/" + family_name):
    for file in files:
        sample_files.append(file)

attack_tables = []
release_tables = []

for sample_file in sample_files:

    table_size = 257

    sample_rate, sample_data = wavfile.read("input/" + family_name + "/" + sample_file)

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

    print(len(rms_attack))
    print(len(rms_release))

    attack_tables.append([int(i) for i in rms_attack])
    release = [int(i) for i in rms_release]
    release.reverse()
    release_tables.append(release)

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

print(attack_tables)
print(release_tables)

release_integrals = []

for table in release_tables:
    sum = 0
    for i in table:
        sum += i
    release_integrals.append(sum)

sorted_indices = sorted(range(len(release_tables)), key=lambda k: release_integrals[k])

sorted_attacks = []
sorted_releases = []

for i in sorted_indices:
    sorted_attacks.append(attack_tables[i])
    sorted_releases.append(release_tables[i])

array_to_csv(sorted_attacks, "output/" + family_name + "_attack.csv")
array_to_csv(sorted_releases, "output/" + family_name + "_release.csv")

plt.show()



