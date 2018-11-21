import csv
import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy import signal

root = tk.Tk()
root.withdraw()

wave_edit_csv = filedialog.askopenfilename()

num_tables = input("How many tables? 3, 5, or 9?")

raw_table = []

with open(wave_edit_csv, "r") as csvfile:
    sample_read = csv.reader(csvfile, delimiter=",")
    for waveform in sample_read:
        wave = []
        for sample in waveform:
            wave.append(float(sample))
        raw_table.append(np.array(wave))

processed_table = []

for waveform in raw_table[0:int(num_tables)]:
    processed_waveform = signal.resample(waveform, 512)
    processed_waveform = np.roll(processed_waveform, -processed_waveform.argmin())
    processed_waveform -= np.amin(processed_waveform)
    processed_waveform *= (1/np.amax(processed_waveform))
    processed_waveform *= 32767
    processed_waveform = processed_waveform.astype(int)
    processed_table.append(processed_waveform)

attack_table = []
release_table = []

for waveform in processed_table:
    waveform = np.append(waveform, 0)
    attack_table.append(waveform[0:257])
    release_table.append(np.flip(waveform[256:513], axis=0))

print(attack_table)
print(release_table)

name = input("Enter the table name: ")

with open("table_sample_defs/" + name + '_attack.csv', "w") as output:
    output_write = csv.writer(output)
    for row in attack_table:
        print(len(row))
        output_write.writerow(row)

with open("table_sample_defs/" + name + '_release.csv', "w") as output:
    output_write = csv.writer(output)
    for row in release_table:
        print(len(row))
        output_write.writerow(row)
