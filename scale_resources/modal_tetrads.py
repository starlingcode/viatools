import csv
import os

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

scale_dict = {
    "C": [1, 1],
    "D": [9, 8],
    "E": [5, 4],
    "F": [4, 3],
    "G": [3, 2],
    "A": [27, 16],
    "A#": [9, 5],
    "A#low": [16, 9],
    "B": [15, 8]
}

row1 = [["C", 0], ["E", 0], ["G", 0], ["B", 0]]
row2 = [["D", 0], ["F", 0], ["A", 0], ["C", 1]]
row3 = [["E", 0], ["G", 0], ["B", 0], ["D", 1]]
row4 = [["F", 0], ["A", 0], ["C", 1], ["E", 1]]
row5 = [["G", 0], ["B", 0], ["D", 1], ["F", 1]]
row6 = [["A", 0], ["C", 1], ["E", 1], ["G", 1]]
row7 = [["B", 0], ["D", 1], ["F", 1], ["A", 1]]
row8 = [["C", 1], ["E", 1], ["G", 1], ["A#", 1]]


rows = [row1, row2, row3, row4, row5, row6, row7, row8]

family_name = "modal_tetrads"

scale_output = []

for row in rows:

    print_row = []

    for ratio in row:

        numerator = scale_dict[ratio[0]][0] * (2**ratio[1])
        denominator = scale_dict[ratio[0]][1]

        print_row.append(str(numerator) + "/" + str(denominator))

    scale_output.append(print_row)

print(scale_output)


for index, scale in enumerate(scale_output):

    with open("scale_defs/" + family_name + "/" + family_name + alphabet[index] + ".csv", "w") as outputfile:

        scale = [family_name + str(index)] + scale

        writer = csv.writer(outputfile)
        writer.writerow(scale)

