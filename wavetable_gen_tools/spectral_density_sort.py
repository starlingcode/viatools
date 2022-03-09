from __future__ import division
import numpy as np
from scipy import signal
from scipy import fftpack
from numpy import abs, sum, linspace
from numpy.fft import rfft
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import csv
import sys
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

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

def centroid(signal):

    spectrum = abs(rfft(signal))
    weighting_function = linspace(1, 32, len(spectrum))
    normalized_spectrum = spectrum / sum(spectrum * weighting_function)  # like a probability mass function
    normalized_frequencies = linspace(0, 1, len(spectrum))
    spectral_centroid = sum(normalized_frequencies * normalized_spectrum)

    return spectral_centroid

messagebox.showinfo("Attack", "Hi, please specify the attack table CSV")
attack_file = filedialog.askopenfilename(message="")

messagebox.showinfo("Release", "Great, now please specify the release table CSV")
release_file = filedialog.askopenfilename(message="")

attack_table = csv_to_array(attack_file)
release_table = csv_to_array(release_file)

print(str(len(attack_table)) + " slopes in attack")
print(str(len(release_table)) + " slopes in release")

if len(attack_table) != len(release_table):
    abort = input("The table sizes  don't match, shall we stop and try again? 'y' or 'n': ")
    if abort == "y":
        sys.exit()

tables = []

for index, table in enumerate(attack_table):

    full_table = []

    for sample in table[:256]:
        full_table.append(int(sample))

    release = release_table[index][1:]

    release.reverse()

    print(release)

    for sample in release:
        full_table.append(int(sample))

    tables.append(full_table)

print(attack_table)

x = np.linspace(0, 512, 512)

density_per_index = []

for index, table in enumerate(tables):

    density_per_index.append([np.average(centroid(table)), index])

density_per_index.sort(key=lambda pair: pair[0])

reordered_attack = []
reordered_release = []

for record in density_per_index:

    print(attack_table[record[1]])
    print(release_table[record[1]])

    reordered_attack.append(attack_table[record[1]])
    reordered_release.append(release_table[record[1]])

array_to_csv(reordered_attack, attack_file)
array_to_csv(reordered_release, release_file)


