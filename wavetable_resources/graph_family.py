import numpy as np
import matplotlib.pyplot as plt
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

ax.plot_wireframe(X, Y, Z, rcount=morph_size, ccount=256, alpha=0.4, cmap=cm.coolwarm)
plt.axis('off')

fig = plt.figure(3)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(X, Y, Z, rcount=morph_size, ccount=256, alpha=0.8, cmap=cm.coolwarm)
plt.axis('off')

fig = plt.figure(4)
subplot_hack = 331

for table in tables:
    ax = fig.add_subplot(subplot_hack)
    plt.plot(table)
    plt.axis('off')
    subplot_hack += 1



plt.show()



