import csv
import numpy as np
import os

family_name = "rhythm_integers"

os.mkdir("scale_defs/" + family_name)

choices = [1, 2, 3, 4, 6, 9, 12, 16, 24]

family = []

for denominator in choices:

    ratios = []

    for numerator in choices:

        ratios.append(str(numerator) + "/" + str(denominator))

    family.append(ratios)

print(family)

for index, scale in enumerate(family):

    with open("scale_defs/" + family_name + "/" + family_name + str(index) + ".csv", "w") as outputfile:

        scale = [family_name + str(index)] + scale

        writer = csv.writer(outputfile)
        writer.writerow(scale)

