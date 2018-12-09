import csv
import os

family_name = "tetrad_inversions"

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]

chord1 = [8, 10, 12, 15]

chord2 = [10, 12, 15, 18]

chord3 = [6, 8, 9, 10]

chord4 = [4, 5, 6, 9]

base_chords = [chord1, chord2, chord3, chord4]

chords = []

for chord in base_chords:

    chords.append([chord[0], chord[1], chord[2], chord[3]])
    chords.append([chord[2], chord[3], 2*chord[0], 2*chord[1]])
    chords.append([chord[1], chord[2], chord[3], 2 * chord[0]])
    chords.append([chord[3], 2 * chord[1], 2 * chord[2], 2 * chord[3]])

scales = []

for chord in chords:

    ratios = []

    for note in chord:
        ratio = [note, chord[0]]

        while ratio[0] > 2 * ratio[1]:

            ratio[1] *= 2

        ratios.append(ratio)

    print(ratios)
    scales.append(ratios)

scale_output = []

for scale in scales:

    print_row = []

    for ratio in scale:

        numerator = ratio[0]
        denominator = ratio[1]

        print_row.append(str(numerator) + "/" + str(denominator))

    scale_output.append(print_row)

print(scale_output)


for index, scale in enumerate(scale_output):

    with open("scale_defs/" + family_name + "/" + family_name + alphabet[index] + ".csv", "w") as outputfile:

        scale = [family_name + str(index)] + scale

        writer = csv.writer(outputfile)
        writer.writerow(scale)

