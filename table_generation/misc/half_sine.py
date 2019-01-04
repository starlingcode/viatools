import csv
from matplotlib import pyplot as plt
import numpy as np

row0 = [1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1, 0]
row1 = [4, 1, 5, 2, 6, 3, 7, 8, 4, 7, 3, 6, 2, 5, 1, 0]
row2 = [2, 4, 6, 1, 3, 5, 7, 8, 6, 4, 2, 7, 5, 3, 1, 0]
row3 = [3, 6, 1, 4, 7, 2, 5, 8, 5, 2, 7, 4, 1, 6, 3, 0]
row4 = [3, 6, 4, 2, 5, 7, 6, 8, 6, 7, 5, 2, 6, 3, 1, 0]
row5 = [2, 4, 6, 5, 3, 1, 7, 8, 6, 4, 2, 3, 5, 7, 1, 0]
row6 = [1, 5, 7, 6, 3, 2, 4, 8, 7, 3, 1, 2, 5, 6, 4, 0]
row7 = [7, 1, 6, 5, 2, 4, 3, 8, 1, 7, 2, 6, 3, 5, 4, 0]
row8 = [1, 0, 3, 0, 5, 0, 7, 8, 6, 8, 4, 8, 2, 8, 4, 0]

rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8]

cos_domain = np.linspace(0, np.pi, 32)

half_cos = -np.cos(cos_domain)

half_cos += 1

half_cos /= 2

renders = []
unit_step = (2/8.0)
print(unit_step)

for row in rows:
    render = []
    for position, i in enumerate(row):
        last_height = row[position-1] * unit_step - 1
        this_height = i*unit_step - 1
        this_cos = half_cos*(this_height - last_height) + last_height
        for j in range(0, 32):
            render.append(this_cos[j])
        last_height = this_height
    renders.append(render)

plt.plot(renders[4])

file_name = input("whats it called? ")

with open("output/" + file_name + ".csv", "w") as output_file:
    output_write = csv.writer(output_file)
    for render in renders:
        output_write.writerow(render)
        plt.plot(render)

plt.show()