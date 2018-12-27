import csv
from matplotlib import pyplot as plt


row0 = [0, 1]
row1 = [0, 1, 2, 1]
row2 = [0, 1, 2, 3, 2, 1]
row3 = [0, 1, 2, 3, 4, 3, 2, 1]
row4 = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1]
row5 = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
row6 = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1]
row7 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1]
row8 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]


rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8]

renders = []

for row in rows:

    unit_step = 2/max(row)
    print(unit_step)
    num_steps = len(row)
    num_samples = int(512/num_steps)
    remaining_samples = 512 - num_samples * num_steps
    print(remaining_samples)

    render = []

    for i in row:
        for j in range(0, num_samples):
            render.append(i * unit_step - 1)

    for j in range(0, remaining_samples):
        render.append(row[-1] * unit_step - 1)

    print(len(render))
    renders.append(render)


file_name = "steps"

with open("output/" + file_name + ".csv", "w") as output_file:
    output_write = csv.writer(output_file)
    for render in renders:
        output_write.writerow(render)
        plt.plot(render)

plt.show()