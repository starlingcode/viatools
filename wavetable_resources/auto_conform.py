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

    this_table = []

    with open(filename, "r") as csv_input:

        table_reader = csv.reader(csv_input, delimiter=",")
        for row in table_reader:
            if row[0] != "":
                this_table.append(row)

    return this_table

def array_to_csv(table, filename):

    with open(filename, "w") as csv_output:

        table_writer = csv.writer(csv_output, delimiter=",")
        for row in table:
            table_writer.writerow(row)


# messagebox.showinfo("Attack", "Hi, please specify the attack table CSV")
# attack_file = filedialog.askopenfilename(message="")
#
# messagebox.showinfo("Release", "Great, now please specify the release table CSV")
# release_file = filedialog.askopenfilename(message="")

attack_file = "table_sample_defs/trains_attack.csv"
release_file = "table_sample_defs/trains_release.csv"

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

    for sample in reversed(release):
        full_table.append(int(sample))

    tables.append(full_table)

x = np.linspace(0, 512, 512)

for table in tables:

    plt.plot(x, table)

    max_index = np.argmax(table)

    print(max_index)


plt.show()
