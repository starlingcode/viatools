import csv
import numpy as np
import os

family_name = "no_triplets"

try:
    os.mkdir("scale_defs/" + family_name)
except:
    pass

numerators = [1, 2, 2, 4, 4, 8, 8, 16]
denominators = [1, 2, 3, 4, 6, 8, 12, 16]

family = []

for denominator in denominators:

    ratios = []

    for numerator in numerators:

        ratios.append(str(numerator) + "/" + str(denominator))

    family.append(ratios)

print(family)

for index, scale in enumerate(family):

    with open("scale_defs/" + family_name + "/" + family_name + str(index) + ".csv", "w") as outputfile:

        scale = [family_name + str(index)] + scale

        writer = csv.writer(outputfile)
        writer.writerow(scale)

