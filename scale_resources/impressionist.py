import csv
import os

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

scale_dict = {
    "C": [1, 1],
    "C#": [17, 16],
    "D": [9, 8],
    "D#": [6, 5],
    "E": [5, 4],
    "F": [4, 3],
    "F#": [7, 5],
    "G": [3, 2],
    "G#": [8, 5],
    "A#": [9, 5],
    "A#low": [16, 9],
    "B": [15, 8]
}

row1 = [["C", 0], ["D#", 0], ["G", 0], ["G#", 0], ["C", 1], ["D#", 1], ["G", 1], ["B", 1]]
row2 = [["C", 0], ["D#", 0], ["G", 0], ["G#", 0], ["C", 1], ["D#", 1], ["A#", 1], ["C", 2]]
row3 = [["D", 0], ["F", 0], ["G", 0], ["G#", 0], ["C", 1], ["D", 1], ["G#", 1], ["C", 2]]
row4 = [["D", 0], ["F", 0], ["G", 0], ["G#", 0], ["C", 1], ["D", 1], ["G#", 1], ["C", 2]]
row5 = [["C#", 0], ["E", 0], ["G", 0], ["A#", 0], ["C#", 1], ["E", 1], ["G", 1], ["A#", 1]]
row6 = [["C#", 0], ["E", 0], ["G", 0], ["A#", 0], ["C#", 1], ["E", 1], ["G", 1], ["A#", 1]]
row7 = [["D", 0], ["G", 0], ["A#", 0], ["C", 0], ["D", 1], ["G", 1], ["A#", 1], ["D", 2]]
row8 = [["C", 0], ["G", 0], ["A#", 0], ["C", 0], ["D", 1], ["G", 1], ["A#", 1], ["C", 2]]
row9 = [["C#", 0], ["F", 0], ["G#", 0], ["C", 0], ["C#", 1], ["F", 1], ["G#", 1], ["C", 2]]
row10 = [["C#", 0], ["F", 0], ["G#", 0], ["A#", 0], ["C#", 1], ["F", 1], ["G#", 1], ["C", 2]]
row11 = [["C", 0], ["F", 0], ["G", 0], ["G#", 0], ["C", 1], ["F", 1], ["G#", 1], ["D", 2]]
row12 = [["C", 0], ["F", 0], ["G", 0], ["G#", 0], ["C", 1], ["F", 1], ["G#", 1], ["D", 2]]
row13 = [["D", 0], ["F", 0], ["G#", 0], ["B", 0], ["D", 1], ["F", 1], ["G#", 1], ["B", 1]]
row14 = [["D", 0], ["F", 0], ["G#", 0], ["B", 0], ["D", 1], ["F", 1], ["G#", 1], ["B", 1]]
row15 = [["C", 0], ["D#", 0], ["G", 0], ["B", 0], ["C", 1], ["D#", 1], ["G", 1], ["C", 2]]
row16 = [["C", 0], ["D#", 0], ["G", 0], ["B", 0], ["C", 1], ["D#", 1], ["G", 1], ["C", 2]]

rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12, row13, row14, row15, row16]

family_name = "impressionist"

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

