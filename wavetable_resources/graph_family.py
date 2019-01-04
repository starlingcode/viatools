import numpy as np
import matplotlib.pyplot as plt, mpld3
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import csv

def csv_to_array(filename):

    table = []

    with open(filename, "r") as csv_input:

        table_reader = csv.reader(csv_input, delimiter=",")
        for row in table_reader:
            if row[0] != "":
                table.append(row)

    return table

table_def_dump = csv_to_array("table_definitions.csv")

table_defs = {}

for row in table_def_dump:

    table_defs[row[0]] = [row[1], row[2]]

table_to_plot = input("Which table should we look at? ")

attack_file = table_defs[table_to_plot][0]
release_file = table_defs[table_to_plot][1]

attack_table = csv_to_array("table_sample_defs/" + attack_file + ".csv")
release_table = csv_to_array("table_sample_defs/" + release_file + ".csv")

tables = []

for index, table in enumerate(attack_table):

    full_table = []

    for sample in table[:256]:
        full_table.append(int(sample))

    release = release_table[index][1:]

    release.reverse()

    for sample in release:
        full_table.append(int(sample))

    tables.append(full_table)

morph_size = len(tables)

print(morph_size)

yrange = np.arange(0, morph_size, 1)
xrange = np.arange(0, 512, 1)
X, Y = np.meshgrid(xrange, yrange)

Z = np.array(tables)

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')

ax.contour(X, Y + 1, Z, zdir="y")
plt.axis('off')

fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor((0, 0, 0))
ax.view_init(elev=85, azim=-50)
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)

ax.plot_wireframe(X, Y, Z, rcount=morph_size, ccount=256, alpha=0.4, color=(240/256, 200/256, 50/256))
plt.axis('off')

fig.savefig('test_wireframe.svg', transparent=True)

fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, rcount=morph_size, ccount=256, alpha=0.8, cmap=cm.coolwarm)
plt.axis('off')

fig = plt.figure(4, facecolor='black')
subplot_hack = 331

for table in tables:
    ax = fig.add_subplot(subplot_hack)
    ax.set_facecolor((0, 0, 0))
    fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
    plt.plot(table, color=(240/256, 200/256, 50/256), linewidth=2)
    plt.axis('off')
    subplot_hack += 1

fig.savefig('test_waveforms.svg', transparent=True)

fig = plt.figure(5)
subplot_hack = 331

for table in tables:
    ax = fig.add_subplot(subplot_hack)
    fft_reading = np.abs(np.fft.rfft(table))
    fft_reading = np.log(fft_reading[:128])
    plt.plot(fft_reading)
    plt.axis('off')
    subplot_hack += 1

plt.show()



