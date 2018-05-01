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


a_patterns = []
b_patterns = []
pattern_set = set([])

with open("euclidean.csv", newline="\n") as csvfile:
    euclidreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in euclidreader:
        if row[0] != "":
            a_pattern = ["eucludean" + str(row[0]) + "_" + str(row[1]),
                              tuple(bjorklund(row[1], row[0]))]
            a_pattern = tuple(a_pattern)
            a_patterns.append(a_pattern)
            pattern_set.add(a_pattern)
            b_pattern = ["eucludean" + str(row[2]) + "_" + str(row[3]),
                              tuple(bjorklund(row[3], row[2]))]
            b_pattern = tuple(b_pattern)
            b_patterns.append(b_pattern)
            pattern_set.add(b_pattern)

print(a_patterns)
print(b_patterns)
print(pattern_set)

text_file = open("patterns.h", "w")
text_file.truncate()

text_file.write('#include "stm32f3xx_hal.h"\n')
text_file.write('#include "stm32f3xx.h"\n')
text_file.write('#include "stm32f3xx_it.h"\n')
text_file.write("\n\n\n")
text_file.write("typedef struct {\n")
text_file.write("	const uint32_t *aPattern;\n")
text_file.write("	const uint32_t *bPattern;\n")
text_file.write("	const uint32_t aLength;\n")
text_file.write("	const uint32_t bLength;\n")
text_file.write("} pattern;\n")
text_file.write("\n\n\n")

for i in pattern_set:
    tag = str(i[0])
    pattern = list(i[1])
    length = len(pattern)
    print(pattern)
    print(tag)
    print(length)
    for index in range(0, len(pattern)):
        print(index)
        if index == 0:
            text_file.write(
                "static const uint32_t " + tag + "[" + str(length) + "] = {" + str(pattern[0]) + ", ")
        elif index != (length - 1):
            text_file.write(str(pattern[index]) + ", ")
        else:
            text_file.write(str(pattern[index]) + "}; \n\n")



