import csv

class Pattern:

    # pattern_data = ("tag", (pattern), float density)

    all_patterns = set([])
    seq1_bank = []
    seq2_bank = []

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
        patterns = []

        with open("pattern_resources/" + bank_name + ".csv", newline="\n") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                if row[0] != "":
                    pattern = [bank_name + "_" + str(row[0]) + "_" + str(row[1]),
                                 tuple(self.bjorklund(row[1], row[0])), float(row[0]) / float(row[1])]
                    pattern = tuple(pattern)
                    patterns.append(pattern)
                    pattern_set.add(pattern)
            patterns = sorted(patterns, key=lambda x: float(x[2]))
        return [patterns, pattern_set]


    def read_data(self):

        with open("pattern_resources/sequencer1banks.csv", newline="\n") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                this_bank = []
                if row[0] != "":
                    results = self.parse_csv_euclidean(row[0], self.all_patterns)
                    self.all_patterns |= results[1]
                    this_bank.append([row[0], results[0]])
                    self.seq1_bank.append(this_bank)

        with open("pattern_resources/sequencer2banks.csv", newline="\n") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                this_bank = []
                if row[0] != "":
                    results = self.parse_csv_euclidean(row[0], self.all_patterns)
                    self.all_patterns |= results[1]
                    this_bank.append([row[0], results[0]])
                self.seq2_bank.append(this_bank)

    def write_header(self):

        text_file = open("generated_code/boolean_sequences.hpp", "w")
        text_file.truncate()

        stub = open("pattern_resources/header_stub.txt", "r")
        text_file.write(stub.read())

        for pattern in self.all_patterns:
            tag = str(pattern[0])
            pattern = list(pattern[1])
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

        banks_written = set([])

        for j in self.seq1_bank:
            index = self.seq1_bank.index(j)
            for pattern_set in self.seq1_bank[index]:
                if pattern_set[0] not in banks_written:
                    num_patterns = len(pattern_set[1])
                    for index in range(0, num_patterns):
                        if index == 0:
                            text_file.write(
                                "static const uint32_t *" + pattern_set[0] + "[" + str(num_patterns) + "] = {" + str(pattern_set[1][0][0]) + ", ")
                        elif index != (num_patterns - 1):
                            text_file.write(str(pattern_set[1][index][0]) + ", ")
                        else:
                            text_file.write(str(pattern_set[1][index][0]) + "}; \n\n")

                    for index in range(0, num_patterns):
                        if index == 0:
                            text_file.write(
                                "static const uint32_t " + pattern_set[0] + "Lengths[" + str(num_patterns) + "] = {" + str(
                                    len(pattern_set[1][0][1])) + ", ")
                        elif index != (num_patterns - 1):
                            text_file.write(str(len(pattern_set[1][index][1])) + ", ")
                        else:
                            text_file.write(str(len(pattern_set[1][index][1])) + "}; \n\n")

                    text_file.write("static const booleanSequenceBank " + pattern_set[0] + "_bank = {\n")
                    text_file.write("   .patternBank = " + pattern_set[0] + ",\n")
                    text_file.write("   .lengths = " + pattern_set[0] + "Lengths,\n")
                    text_file.write("   .numPatterns = " + str(num_patterns) + "};\n")
                    text_file.write("//////////////////////////////////////////////////////// \n\n")

                banks_written.add(pattern_set[0])

        for j in self.seq2_bank:
            index = self.seq2_bank.index(j)
            for pattern_set in self.seq2_bank[index]:
                if pattern_set[0] not in banks_written:
                    num_patterns = len(pattern_set[1])
                    for index in range(0, num_patterns):
                        if index == 0:
                            text_file.write(
                                "static const uint32_t *" + pattern_set[0] + "[" + str(num_patterns) + "] = {" + str(pattern_set[1][0][0]) + ", ")
                        elif index != (num_patterns - 1):
                            text_file.write(str(pattern_set[1][index][0]) + ", ")
                        else:
                            text_file.write(str(pattern_set[1][index][0]) + "}; \n\n")

                    for index in range(0, num_patterns):
                        if index == 0:
                            text_file.write(
                                "static const uint32_t " + pattern_set[0] + "Lengths[" + str(num_patterns) + "] = {" + str(
                                    len(pattern_set[1][0][1])) + ", ")
                        elif index != (num_patterns - 1):
                            text_file.write(str(len(pattern_set[1][index][1])) + ", ")
                        else:
                            text_file.write(str(len(pattern_set[1][index][1])) + "}; \n\n")

                    text_file.write("static const booleanSequenceBank " + pattern_set[0] + "_bank = {\n")
                    text_file.write("   .patternBank = " + pattern_set[0] + ",\n")
                    text_file.write("   .lengths = " + pattern_set[0] + "Lengths,\n")
                    text_file.write("   .numPatterns = " + str(num_patterns) + "};\n")
                    text_file.write("//////////////////////////////////////////////////////// \n\n")


                banks_written.add(pattern_set[0])

        text_file.write("#endif")

        text_file.close()

    def write_gateseq_source(self):

        text_file = open("generated_code/gateseq_pattern_init.cpp", "w")
        text_file.truncate()

        text_file.write('#include <gateseq.hpp>\n\n')

        text_file.write("void ViaGateseq::initializePatterns() {\n")
        for j in self.seq1_bank:
            bank_name = str(j[0][0])
            index = self.seq1_bank.index(j)
            text_file.write("   seq1PatternBank[" + str(index) + "] = &" + bank_name + "_bank;\n")
        for j in self.seq2_bank:
            bank_name = str(j[0][0])
            index = self.seq2_bank.index(j)
            text_file.write("   seq2PatternBank[" + str(index) + "] = &" + bank_name + "_bank;\n")
        text_file.write("}\n")

        text_file.close()

    def generate_gateseq_code(self):

        self.read_data()
        self.write_header()
        self.write_gateseq_source()





