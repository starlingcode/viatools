import csv
import numpy as np
import os

family_name = "poly_div_resets"

try:
    os.mkdir("scale_defs/" + family_name)
except:
    pass

numerators = [1, 2, 3, 4, 6, 8, 16, 24]
denominators = [1, 2, 3, 4, 5, 6, 7, 8]
resets = [4, 4, 8, 8, 16, 16, 32, 32]

family = []

for i, denominator in enumerate(denominators):

    ratios = []

    reset = resets[i]

    for numerator in numerators:

        if reset < denominator/numerator:
            reset_write = denominator
        else:
            reset_write = reset

        ratios.append(str(numerator) + "/" + str(denominator) + "-" + str(reset_write))

    family.append(ratios)

print(family)

for index, scale in enumerate(family):

    with open("scale_defs/" + family_name + "/" + family_name + str(index) + ".csv", "w") as outputfile:

        scale = [family_name + str(index)] + scale

        writer = csv.writer(outputfile)
        writer.writerow(scale)

