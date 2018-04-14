# helper functions to generate scale code for the pll via

import math

import csv

def makeScaleFullSpan(scale_name):

    # initialize lists to parse the csv
    ratio_subset = []
    ratio_table = []
    scale_tags = []



    # # parse the csv for integer ratios and calculate an interval in terms of octaves
    # with open(scale_name + ".csv", newline="\n") as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    #     for row in spamreader:
    #         if row[0] != "":
    #             if row[1] == "":
    #                 scale_tags.append(row[0])
    #                 print(row[0])
    #             else:
    #                 ratio = [int(row[0]), int(row[1])]
    #                 ratio_subset.append(ratio)
    #
    #         elif ratio_subset != []:
    #             ratio_table.append(ratio_subset)
    #             ratio_subset = []

    # parse the csv for integer ratios and calculate an interval in terms of octaves
    # scale per row format
    with open(scale_name + ".csv", newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != "":
                scale_tags.append(row[0])
                print(row[0])
                for cell in row[1:]:
                    if "/" in cell:
                        delim1 = cell.index("/")
                        if "-" in cell:
                            delim2 = cell.index("-")
                            ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:delim2]), int(cell[delim2+1:])]
                        else:
                            ratio = [int(cell[0:delim1]), int(cell[delim1+1:])]
                        ratio_subset.append(ratio)
                ratio_table.append(ratio_subset)
                ratio_subset = []

    num_scales = len(scale_tags)
    pitch_set = set([])
    full_scale = []
    full_row = []

    for i in ratio_table:

        row_pointer = ratio_table.index(i)

        j = 0

        while j < 128:

            numerator_int = int(ratio_table[row_pointer][int(j * len(i)/128)][0])

            denominator_int = int(ratio_table[row_pointer][int(j * len(i)/128)][1])

            divisor = math.gcd(int(numerator_int), int(denominator_int))

            if len(ratio_table[row_pointer][int(j * len(i)/128)]) == 3:
                fundamental_divisor = ratio_table[row_pointer][int(j * len(i)/128)][2]
                ratio_tag = "ratio" + str(int(numerator_int / divisor)) + "_" + str(int(denominator_int / divisor)) + "_" + str(fundamental_divisor)

            else:
                fundamental_divisor = int(denominator_int/divisor)
                ratio_tag = "ratio" + str(int(numerator_int / divisor)) + "_" + str(int(denominator_int / divisor))

            fix32_calculation = int(numerator_int * 2 ** 48 / denominator_int)

            integer_part = fix32_calculation >> 32

            fractional_part = fix32_calculation - (integer_part << 32)

            ratio_holder = (ratio_tag, integer_part, fractional_part, fundamental_divisor)

            if ratio_holder not in pitch_set:
                pitch_set.add(ratio_holder)

            full_row.append(ratio_holder)

            j += 1


        full_scale.append(full_row)
        full_row = []

    print(ratio_table)

    return [full_scale, pitch_set, scale_tags, num_scales]
