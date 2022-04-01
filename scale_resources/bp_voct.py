import csv
import os
import numpy as np

scales = []

file_names = []

for root, dirs, files in os.walk("scale_defs/bohlenPeirce/"):
    for file in files:

        file_names.append(file[:-4])

        with open("scale_defs/bohlenPeirce/" + file) as input_file:

            scale_reader = csv.reader(input_file)
            for row in scale_reader:
                this_scale = []
                for cell in row:
                    this_scale.append([int(cell.split('/')[0]), int(cell.split('/')[1])])
                scales.append(this_scale)

indices = []

for scale in scales:

    these_indices = []

    for ratio in scale:

        calculated = ratio[0]/ratio[1]

        index = int(((calculated - 1)/2) * 19)

        these_indices.append(index)

    if these_indices[1] == 0:

        these_indices[1] = 1;

    if these_indices[2] == 1:

        these_indices[2] = 2;

    indices.append(these_indices)


tiles = []

for scale_position, scale in enumerate(scales):

    these_indices = indices[scale_position]

    this_tile = []

    for ratio_position, ratio in enumerate(scale):

        first_index = these_indices[ratio_position]
        if ratio_position == len(scale) - 1:
            last_index = 19
        else:
            last_index = these_indices[ratio_position + 1]

        for repeat in range(0, last_index-first_index):

            this_tile.append(ratio)

    tiles.append(this_tile)

numerator_multiplier = []
denominator_multiplier = []

for i in range(0, 64):
    numerator_multiplier.append(1)
    denominator_multiplier.append(3**int(abs(i - (63 + 19))/19))
for i in range(0, 64):
    numerator_multiplier.append(3**int(i/19))
    denominator_multiplier.append(1)

print(numerator_multiplier)
print(denominator_multiplier)

print(len(numerator_multiplier))
print(len(denominator_multiplier))

first_index = 12

full_rows = []

for tile in tiles:

    full_row = []

    for index in range(0, 128):

        this_ratio = tile[(index + first_index) % 19]

        numerator = this_ratio[0] * numerator_multiplier[index]
        denominator = this_ratio[1] * denominator_multiplier[index]

        full_row.append(str(numerator) + "/" + str(denominator))

    print(len(full_row))
    full_rows.append(full_row)

print(file_names)

for write_index, write_row in enumerate(full_rows):

    file_name = file_names[write_index] + "voct.csv"


    with open("scale_defs/bohlenPeircevoct/" + file_name, "w") as write_file:

        write_bot = csv.writer(write_file)
        write_bot.writerow(write_row)