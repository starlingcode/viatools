import sys
import csv

# from https://github.com/brianhouse/bjorklund


def bjorklund(steps, pulses):
    steps = int(steps)
    pulses = int(pulses)
    if pulses > steps:
        raise ValueError
    pattern = []
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    while True:
        counts.append(divisor / remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)
    
    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)
        else:
            for i in range(0, int(counts[level])):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)

    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]
    return pattern

# read csv and return

def parse_csv_euclidean(bank_name, pattern_set):

    a_patterns = []
    b_patterns = []

    with open(bank_name + ".csv", newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if row[0] != "":
                a_pattern = [bank_name + "_" + str(row[0]) + "_" + str(row[1]),
                             tuple(bjorklund(row[1], row[0]))]
                a_pattern = tuple(a_pattern)
                a_patterns.append(a_pattern)
                pattern_set.add(a_pattern)
                b_pattern = [bank_name + "_" + str(row[2]) + "_" + str(row[3]),
                             tuple(bjorklund(row[3], row[2]))]
                b_pattern = tuple(b_pattern)
                b_patterns.append(b_pattern)
                pattern_set.add(b_pattern)
    return [a_patterns, b_patterns, pattern_set]


current_pattern_set = set([])
banks = []

with open("euclidean_banks.csv", newline="\n") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        if row[0] != "":
            results = parse_csv_euclidean(row[0], current_pattern_set)
            current_pattern_set = results[2]
            banks.append([row[0], results[0], results[1]])






text_file = open("patterns.h", "w")
text_file.truncate()

text_file.write('#include "stm32f3xx_hal.h"\n')
text_file.write('#include "stm32f3xx.h"\n')
text_file.write('#include "stm32f3xx_it.h"\n')
text_file.write("\n\n\n")
text_file.write("typedef struct {\n")
text_file.write("	const uint32_t **aPatternBank;\n")
text_file.write("	const uint32_t **bPatternBank;\n")
text_file.write("	const uint32_t *aLengths;\n")
text_file.write("	const uint32_t *bLengths;\n")
text_file.write("	const uint32_t aNumPatterns;\n")
text_file.write("	const uint32_t bNumPatterns;\n")
text_file.write("} pattern_bank;\n")
text_file.write("\n\n\n")

for i in current_pattern_set:
    tag = str(i[0])
    pattern = list(i[1])
    length = len(pattern)
    for index in range(0, len(pattern)):
        if index == 0:
            text_file.write(
                "static const uint32_t " + tag + "[" + str(length) + "] = {" + str(pattern[0]) + ", ")
        elif index != (length - 1):
            text_file.write(str(pattern[index]) + ", ")
        else:
            text_file.write(str(pattern[index]) + "}; \n\n")

text_file.write("\n\n\n")

for i in banks:
    a_length = len(i[1])
    b_length = len(i[2])
    for index in range(0, a_length):
        if index == 0:
            text_file.write(
                "static const uint32_t *" + i[0] + "_a[" + str(a_length) + "] = {" + str(i[1][0][0]) + ", ")
        elif index != (a_length - 1):
            text_file.write(str(i[1][index][0]) + ", ")
        else:
            text_file.write(str(i[1][index][0]) + "}; \n\n")

    for index in range(0, b_length):
        if index == 0:
            text_file.write(
                "static const uint32_t *" + i[0] + "_b[" + str(b_length) + "] = {" + str(i[2][0][0]) + ", ")
        elif index != (b_length - 1):
            text_file.write(str(i[2][index][0]) + ", ")
        else:
            text_file.write(str(i[2][index][0]) + "}; \n\n")

    for index in range(0, a_length):
        if index == 0:
            text_file.write(
                "static const uint32_t " + i[0] + "_aLengths[" + str(a_length) + "] = {" + str(len(i[1][0][1])) + ", ")
        elif index != (a_length - 1):
            text_file.write(str(len(i[1][index][1])) + ", ")
        else:
            text_file.write(str(len(i[1][index][1])) + "}; \n\n")

    for index in range(0, a_length):
        if index == 0:
            text_file.write(
                "static const uint32_t " + i[0] + "_bLengths[" + str(a_length) + "] = {" + str(len(i[2][0][1])) + ", ")
        elif index != (a_length - 1):
            text_file.write(str(len(i[2][index][1])) + ", ")
        else:
            text_file.write(str(len(i[2][index][1])) + "}; \n\n")


    text_file.write("static const pattern_bank " + i[0] + " = {\n")
    text_file.write("   .aPatternBank = " + i[0] + "_a,\n")
    text_file.write("   .bPatternBank = " + i[0] + "_b,\n")
    text_file.write("   .aLengths = " + i[0] + "_aLengths,\n")
    text_file.write("   .bLengths = " + i[0] + "_bLengths,\n")
    text_file.write("   .aNumPatterns = " + str(a_length) + ",\n")
    text_file.write("   .bNumPatterns = " + str(b_length) + "};\n\n")








