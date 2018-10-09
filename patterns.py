import csv

class Pattern:

    # pattern_data = ("tag", (pattern), float density)

    # from https://github.com/brianhouse/bjorklund
    def bjorklund(self, steps, pulses):
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


    # read csv and return a list of patterns sorted for density
    # return (pattern tag, (pattern), density)
    def parse_csv_euclidean(self, bank_name, pattern_set):
        a_patterns = []
        b_patterns = []

        with open("pattern_resources/" + bank_name + ".csv", newline="\n") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[0] != "":
                    a_pattern = [bank_name + "_" + str(row[0]) + "_" + str(row[1]),
                                 tuple(self.bjorklund(row[1], row[0])), float(row[0]) / float(row[1])]
                    a_pattern = tuple(a_pattern)
                    a_patterns.append(a_pattern)
                    pattern_set.add(a_pattern)
                    b_pattern = [bank_name + "_" + str(row[2]) + "_" + str(row[3]),
                                 tuple(self.bjorklund(row[3], row[2])), float(row[2]) / float(row[3])]
                    b_pattern = tuple(b_pattern)
                    b_patterns.append(b_pattern)
                    pattern_set.add(b_pattern)
            a_patterns = sorted(a_patterns, key=lambda x: float(x[2]))
            b_patterns = sorted(b_patterns, key=lambda x: float(x[2]))
        return [a_patterns, b_patterns, pattern_set]


    def read_data(self):
        pattern_set = set([])
        banks = []

        with open("pattern_resources/euclidean_banks.csv", newline="\n") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                this_bank = []
                if row[0] != "":
                    results = self.parse_csv_euclidean(row[0], pattern_set)
                    pattern_set = results[2]
                    this_bank.append([row[0], results[0], results[1]])
                banks.append(this_bank)
                # print(this_bank)
                this_bank = []

        # for bank in banks:
        #     print(bank[0][2])

        return pattern_set, banks

    def write_header(self, pattern_set, banks):

        text_file = open("generated_code/boolean_sequences.hpp", "w")
        text_file.truncate()

        stub = open("pattern_resources/header_stub.txt", "r")
        text_file.write(stub.read())

        for i in pattern_set:
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
        text_file.write("//////////////////////////////////////////////////////// \n\n")
        text_file.write("// Banks \n")
        text_file.write("//////////////////////////////////////////////////////// \n\n")

        for j in banks:
            index = banks.index(j)
            for i in banks[index]:
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
                            "static const uint32_t " + i[0] + "_aLengths[" + str(a_length) + "] = {" + str(
                                len(i[1][0][1])) + ", ")
                    elif index != (a_length - 1):
                        text_file.write(str(len(i[1][index][1])) + ", ")
                    else:
                        text_file.write(str(len(i[1][index][1])) + "}; \n\n")

                for index in range(0, a_length):
                    if index == 0:
                        text_file.write(
                            "static const uint32_t " + i[0] + "_bLengths[" + str(a_length) + "] = {" + str(
                                len(i[2][0][1])) + ", ")
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
                text_file.write("//////////////////////////////////////////////////////// \n\n")

        text_file.write("#endif")

        text_file.close()

    def write_gateseq_source(self, banks):

        text_file = open("generated_code/gateseq_pattern_init.c", "w")
        text_file.truncate()

        text_file.write('#include <gateseq.hpp>\n\n')

        text_file.write("void ViaGateseq::initializePatterns() {\n")
        for j in banks:
            bank_name = str(j[0][0])
            index = banks.index(j)
            text_file.write("   patternBank[" + str(index) + "] = &" + bank_name + ";\n")
        text_file.write("}\n")

        text_file.close()

    def generate_gateseq_code(self):

        result = self.read_data()

        pattern_set = result[0]

        banks = result[1]

        self.write_header(pattern_set, banks)
        self.write_gateseq_source(banks)





