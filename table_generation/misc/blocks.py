import csv
from matplotlib import pyplot as plt

row0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1]
row1 = [0, 4, 1, 5, 2, 6, 3, 7, 8, 4, 7, 3, 6, 2, 5, 1]
row2 = [0, 2, 4, 6, 1, 3, 5, 7, 8, 6, 4, 2, 7, 5, 3, 1]
row3 = [0, 3, 6, 1, 4, 7, 2, 5, 8, 5, 2, 7, 4, 1, 6, 3]
row4 = [0, 3, 6, 4, 2, 5, 7, 6, 8, 6, 7, 5, 2, 6, 3, 1]
row5 = [0, 2, 4, 6, 5, 3, 1, 7, 8, 6, 4, 2, 3, 5, 7, 1]
row6 = [0, 1, 5, 7, 6, 3, 2, 4, 8, 7, 3, 1, 2, 5, 6, 4]
row7 = [0, 7, 1, 6, 5, 2, 4, 3, 8, 1, 7, 2, 6, 3, 5, 4]
row8 = [0, 1, 0, 3, 0, 5, 0, 7, 8, 6, 8, 4, 8, 2, 8, 0]

rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8]

renders = []
unit_step = (2/8.0)
print(unit_step)

for row in rows:
    render = []
    for i in row:
        for j in range(0, 32):
            render.append(i*unit_step - 1)
    renders.append(render)

file_name = input("whats it called? ")

with open("output/" + file_name + ".csv", "w") as output_file:
    output_write = csv.writer(output_file)
    for render in renders:
        output_write.writerow(render)
        plt.plot(render)

plt.show()