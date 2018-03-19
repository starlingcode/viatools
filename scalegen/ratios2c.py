# tool to generate scale code for the pll via

import numpy as np

from math import gcd

text_file = open("chromatic5prime.txt", "a")

unison5prime = np.array([1, 1])
min_second5prime = np.array([15, 16])
maj_second5prime = np.array([9, 8])
min_third5prime = np.array([6, 5])
maj_third5prime = np.array([5, 4])
fourth5prime = np.array([4, 3])
tritone5prime = np.array([25, 18])
fifth5prime = np.array([3, 2])
min_sixth5prime = np.array([8, 5])
maj_sixth5prime = np.array([5, 3])
min_seventh5prime = np.array([9, 5])
maj_seventh = np.array([15, 8])

chromatic5prime_ratios = np.array([unison5prime, min_second5prime, maj_second5prime,
                   min_third5prime, maj_third5prime, fourth5prime,
                   tritone5prime, fifth5prime, min_sixth5prime,
                   maj_sixth5prime, min_seventh5prime, maj_seventh])

chromatic5prime_tags = ("unison5prime", "min_second5prime", "maj_second5prime",
                   "min_third5prime", "maj_third5prime", "fourth5prime",
                   "tritone5prime", "fifth5prime", "min_sixth5prime",
                   "maj_sixth5prime", "min_seventh5prime", "maj_seventh")


for i in range(0, 128):

    octave = int((i - 64)/12)

    numerator_int = int(chromatic5prime_ratios[(i - 64) % 12][0])
    denominator_int = int(chromatic5prime_ratios[(i - 64) % 12][1])

    if octave > 0:
        temp_numerator = numerator_int * 2**octave
        divisor = gcd(int(temp_numerator), int(denominator_int))
        fundamental_divisor = int(denominator_int/divisor)
    else:
        temp_denominator = denominator_int * 2**(-octave)
        divisor = gcd(int(numerator_int), int(temp_denominator))
        fundamental_divisor = int(temp_denominator/divisor)

    fix32_calculation = int((numerator_int * 2**(32 + octave))/denominator_int)

    integer_part = fix32_calculation >> 32

    fractional_part = fix32_calculation - integer_part

    ratio_tag = chromatic5prime_tags[(i - 64) % 12] + str(octave)

    text_file.write("#define " + ratio_tag + " {" + str(integer_part) + ", " + str(fractional_part) + ", " + str(fundamental_divisor) + "}\n")

for i in range(0, 128):

    octave = int((i - 64) / 12)

    ratio_tag = chromatic5prime_tags[(i - 64) % 12] + str(octave)

    if i == 0:
        text_file.write("const ScaleNote chromatic5prime[128] = {" + ratio_tag + ", ")
    elif i != 127:
        if i%12 != 0:
            text_file.write(ratio_tag + ", ")
        else:
            text_file.write(ratio_tag + ", \n")
    else:
        text_file.write(ratio_tag + "};")




