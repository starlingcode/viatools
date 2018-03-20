# tool to generate scale code for the pll via

import numpy as np

from math import gcd

import csv

ratio_subset = []
ratio_table = []
scale_tags = []


scale_name = "modal5prime"



with open(scale_name + ".csv", newline="\n") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[0] != "":
            if row[1] == "":
                scale_tags.append(row[0])
                print(row[0])
            else:
                ratio = (int(row[0]), int(row[1]))
                ratio_subset.append(ratio)

        elif ratio_subset != []:
            ratio_table.append(ratio_subset)
            ratio_subset = []


print(ratio_table)
print(scale_tags)


text_file = open("modal5prime.txt", "a")
text_file.truncate()

calculated_table = []
pitch_class_set = set([])

for i in range(0, 8):

    calculated_row = []

    for j in range(0, 128):
    
        octave = int((j - 64)//12)
    
        numerator_int = int(ratio_table[i][(j + 8) % 12][0])
        denominator_int = int(ratio_table[i][(j + 8) % 12][1])
    
        if octave >= 0:
            temp_numerator = numerator_int * 2**octave
            divisor = gcd(int(temp_numerator), int(denominator_int))
            fundamental_divisor = int(denominator_int/divisor)
            ratio_tag = "ratio" + str(temp_numerator) + "_" + str(denominator_int)
    
        else:
            temp_denominator = denominator_int * 2**(-octave)
            divisor = gcd(int(numerator_int), int(temp_denominator))
            fundamental_divisor = int(temp_denominator/divisor)
            ratio_tag = "ratio" + str(numerator_int) + "_" + str(temp_denominator)
    
        fix32_calculation = int((numerator_int * 2**(48 + octave))/denominator_int)
    
        integer_part = fix32_calculation >> 32
    
        fractional_part = fix32_calculation - (integer_part << 32)

        ratio_holder = (ratio_tag, integer_part, fractional_part, fundamental_divisor)

        calculated_row.append(ratio_holder)

        if ratio_holder not in pitch_class_set:
            pitch_class_set.add(ratio_holder)

    print(len(calculated_row))
    calculated_table.append(calculated_row)

print(len(calculated_table))




for i in pitch_class_set:
    ratio_tag = i[0]
    integer_part = i[1]
    fractional_part = i[2]
    fundamental_divisor = i[3]
    text_file.write("const ScaleNote " + ratio_tag + " =  {" + str(integer_part) + ", " + str(fractional_part) + ", " + str(fundamental_divisor) + "}\n")

print(len(pitch_class_set))

text_file.write("\n\n\n")



for i in range(0,8):

    for j in range(0, 128):

        ratio_tag = str(calculated_table[i][j][0])

        if j == 0:
            text_file.write("const ScaleNote " + scale_tags[i] + "[128] = {" + ratio_tag + ", ")
        elif j != 127:
            if j%12 != 0:
                text_file.write(ratio_tag + ", ")
            else:
                text_file.write(ratio_tag + ", \n")
        else:
            text_file.write(ratio_tag + "}; \n\n")

text_file.write("\n\n\n")

for i in range(len(scale_tags)):

    if i == 0:
        text_file.write("const ScaleNote " + scale_name + "[128] = {" + scale_tags[i] + ", ")
    elif i != 7:
        text_file.write(scale_tags[i] + ", ")
    else:
        text_file.write(scale_tags[i] + "}; \n\n")






    



