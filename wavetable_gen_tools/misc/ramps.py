import csv
from matplotlib import pyplot as plt
import numpy as np

row0 = [8, 0]
row1 = [6, 8, 2, 0]
row2 = [4, 6, 2, 8, 4, 2, 6, 0]
row3 = [5, 4, 1, 6, 7, 2, 3, 8, 3, 4, 7, 2, 1, 6, 5, 0]

rows = [row0, row1, row2, row3]

renders = []
unit_step = (2/8.0)
print(unit_step)

for row in rows:
    render = []
    for position, i in enumerate(row):
        last_height = row[position - 1] * unit_step - 1;
        this_height = i * unit_step - 1
        ramp = np.linspace(last_height, this_height, int(512/len(row)) + 1)
        for sample in ramp[:-1]:
            render.append(sample)
    renders.append(render)

file_name = input("whats it called? ")

with open("output/" + file_name + ".csv", "w") as output_file:
    output_write = csv.writer(output_file)
    for render in renders:
        output_write.writerow(render)
        plt.plot(render)

plt.show()