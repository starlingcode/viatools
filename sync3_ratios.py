
def csv_to_array(file):

    output = []

    with open(file) as file_input:

        for line in file_input.readlines():

            line = line.rstrip("\n")

            output.append(line.split(","))

    return output

class Sync3Ratios:

    text_out = ""

    def write_line(self, main, end="\n"):

        self.text_out += main + end

    def csv_to_array(self, file):

        output = []

        with open(file) as file_input:
            for line in file_input.readlines():
                line = line.rstrip("\n")

                output.append(line.split(","))

        return output

    scales = {}
    #
    # scales["perfect"] = [[[1, 32], [1, 16], [1, 12], [1, 8], [1, 6], [1, 4], [1, 3], [1, 2],
    #                      [1, 1], [2, 1], [3, 1], [4, 1], [6, 1], [8, 1], [12, 1], [16, 1]], "doubled"]
    #
    # scales["simpleRhythms"] = [[[1, 32], [1, 16], [1, 8], [1, 6], [1, 4], [1, 3], [1, 2], [2, 3],
    #                             [1, 1], [4, 3], [3, 2], [2, 1], [8, 3], [3, 1], [4, 1], [8, 1]], "doubled"]
    #
    # scales["ints"] = [[], "full set"]
    #
    # for integer in range(-16, 0):
    #     scales["ints"][0].append([1, -integer])
    #
    # for integer in range(1, 17):
    #     scales["ints"][0].append([integer, 1])
    #
    # scales["circleFifths"] = [[[1, 8], [16, 81], [1, 4], [8, 27], [4, 9], [1, 2], [2, 3], [1, 1],
    #                             [1, 1], [3, 2], [2, 1], [9, 4], [27, 8], [4, 1], [81, 16], [8, 1]], "doubled"]
    #
    # scales["fourthsFifths"] = [[[1, 1], [4, 3], [3, 2], [16, 9], [2, 1], [9, 4], [8, 3], [3, 1]], "2octave"]
    #
    # scales["minorArp"] = [[[1, 1], [6, 5], [3, 2], [9, 5], [2, 1], [9, 4], [3, 1], [16, 5]], "2octave"]
    #
    # scales["evenOdds"] = [[[1, 1], [9, 8], [7, 6], [5, 4], [11, 8], [3, 2], [5, 3], [7, 4]], "octave"]
    #
    # scales["bP"] = [[[1, 1], [9, 7], [7, 5], [5, 3], [9, 5], [15, 7], [7, 3], [25, 9]], "tritave"]

    def load_scales(self):

        self.scales = {}

        for line in self.csv_to_array("sync3scales/manifest.csv"):

            tag = line[0]

            data = self.csv_to_array("sync3scales/" + tag + ".csv")

            self.scales[tag] = {}

            self.scales[tag]["raw_ratios"] = []

            for line in data[1:]:
                self.scales[tag]["raw_ratios"].append([int(line[0]), int(line[1])])

            self.scales[tag]["method"] = data[0][0]

    def render(self):

        for scale in self.scales:

            ratios = self.scales[scale]["raw_ratios"]

            mode = self.scales[scale]["method"]

            numerators = []
            denominators = []

            if mode == "octave":

                for ratio in ratios:
                    if (ratio[0] % 4 == 0):
                        numerators.append(int(ratio[0] / 4))
                        denominators.append(int(ratio[1]))
                    elif (ratio[0] % 2 == 0):
                        numerators.append(int(ratio[0] / 2))
                        denominators.append(int(ratio[1] * 2))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 4))

                for ratio in ratios:
                    if (ratio[0] % 2 == 0):
                        numerators.append(int(ratio[0]/2))
                        denominators.append(int(ratio[1]))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 2))

                for ratio in ratios:
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))

                for ratio in ratios:
                    if (ratio[1] % 2 == 0):
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1]/2))
                    else:
                        numerators.append(int(ratio[0] * 2))
                        denominators.append(int(ratio[1]))

            elif mode == "tritave":

                for ratio in ratios:
                    if (ratio[0] % 9 == 0):
                        numerators.append(int(ratio[0] / 9))
                        denominators.append(int(ratio[1]))
                    elif (ratio[0] % 3 == 0):
                        numerators.append(int(ratio[0] / 3))
                        denominators.append(int(ratio[1] * 3))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 9))

                for ratio in ratios:
                    if (ratio[0] % 3 == 0):
                        numerators.append(int(ratio[0]/3))
                        denominators.append(int(ratio[1]))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 3))

                for ratio in ratios:
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))

                for ratio in ratios:
                    if (ratio[1] % 3 == 0):
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1]/3))
                    else:
                        numerators.append(int(ratio[0] * 3))
                        denominators.append(int(ratio[1]))

            elif mode == "2octave":

                for ratio in ratios:

                    if (ratio[0] % 16 == 0):
                        numerators.append(int(ratio[0] / 16))
                        denominators.append(int(ratio[1]))
                    elif (ratio[0] % 8 == 0):
                        numerators.append(int(ratio[0] / 8))
                        denominators.append(int(ratio[1] * 2))
                    elif (ratio[0] % 4 == 0):
                        numerators.append(int(ratio[0] / 4))
                        denominators.append(int(ratio[1] * 4))
                    elif (ratio[0] % 2 == 0):
                        numerators.append(int(ratio[0] / 2))
                        denominators.append(int(ratio[1] * 8))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 16))

                for ratio in ratios:

                    if (ratio[0] % 4 == 0):
                        numerators.append(int(ratio[0] / 4))
                        denominators.append(int(ratio[1]))
                    elif (ratio[0] % 2 == 0):
                        numerators.append(int(ratio[0] / 2))
                        denominators.append(int(ratio[1] * 2))
                    else:
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] * 4))

                for ratio in ratios:
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))

                for ratio in ratios:

                    if (ratio[1] % 4 == 0):
                        numerators.append(int(ratio[0]))
                        denominators.append(int(ratio[1] / 4))
                    elif (ratio[1] % 2 == 0):
                        numerators.append(int(ratio[0] * 2))
                        denominators.append(int(ratio[1] / 2))
                    else:
                        numerators.append(int(ratio[0] * 4))
                        denominators.append(int(ratio[1]))

            elif mode == "doubled":

                for ratio in ratios:
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))

            else:

                for ratio in ratios:
                    numerators.append(int(ratio[0]))
                    denominators.append(int(ratio[1]))

            precalcs = []

            # self.write_line(scale)

            for index, denominator in enumerate(denominators):
                precalc = int((2 ** 32) / denominator) % 4294967296
                precalcs.append(precalc)
                # self.write_line(numerators[index]/denominator, end=" ")
                # self.write_line(numerators[index], end=" ")
                # self.write_line(denominator, end=" ")
                # self.write_line(precalc)

            ratios_used = set()

            keys = []

            key = 0

            for index, numerator in enumerate(numerators):

                ratio = (numerator, denominators[index])

                if ratio not in ratios_used:

                    ratios_used.add(ratio)
                    key += 1

                keys.append(key)

            self.scales[scale]["numerators"] = numerators
            self.scales[scale]["denominators"] = denominators
            self.scales[scale]["precalcs"] = precalcs
            self.scales[scale]["keys"] = keys

    def write_source(self):

        self.text_out = ""

        self.write_line('#include "sync3.hpp"', end="\n\n")

        for tag in self.scales:
            
            scale = self.scales[tag]

            self.write_line("const ViaSync3::Sync3Scale ViaSync3::" + tag + " = {")
            self.write_line("\t{", end="")
            for number in scale["numerators"][0:-1]:
                self.write_line(str(number), end=", ")
            self.write_line(str(scale["numerators"][-1]) + "},")
            self.write_line("\t{", end="")
            for number in scale["denominators"][0:-1]:
                self.write_line(str(number), end=", ")
            self.write_line(str(scale["denominators"][-1]) + "},")
            self.write_line("\t{", end="")
            for number in scale["precalcs"][0:-1]:
                self.write_line(str(number), end=", ")
            self.write_line(str(scale["precalcs"][-1]) + "},")
            self.write_line("\t{", end="")
            for number in scale["keys"][0:-1]:
                self.write_line(str(number), end=", ")
            self.write_line(str(scale["keys"][-1]) + "},")
            self.write_line("\t0")
            self.write_line("};")

            self.write_line('\n')

        self.write_line("const struct ViaSync3::Sync3Scale * ViaSync3::scales[8] = {", end="")

        for scale in self.scales:
            self.write_line("&ViaSync3::" + scale, end=", ")
        self.text_out = self.text_out.rstrip(", ")
        self.write_line("", end="};")

    def write_header(self):

        self.text_out = "/// INSERT SCALES\n\n"

        for scale in self.scales:
            self.write_line("\tstatic const struct Sync3Scale " + scale, end=";\n")

        self.write_line("\n/// INSERT SCALES", end="")

import sys
from shutil import copyfile
import requests

worker = Sync3Ratios()
worker.load_scales()
worker.render()
worker.write_header()
header = worker.text_out
worker.write_source()
source = worker.text_out

with open("generated_code/sync3_scales.cpp", "w") as source_file:

    source_file.write(source)

# This should pull the file from github

r = requests.get("https://raw.githubusercontent.com/starlingcode/Via/master/modules/inc/sync3.hpp")

with open("sync3scales/sync3.hpp", "w") as template:

    template.write(r.text)

with open("sync3scales/sync3.hpp", "r") as template:

    text = template.read()

    sections = text.split("/// INSERT SCALES")

    with open("generated_code/sync3.hpp", "w") as source_file:
        source_file.write(sections[0] + header + sections[2])

if (len(sys.argv)) > 1:

    if sys.argv[1] == "copy":

        copyfile("/vagrant/viatools/generated_code/sync3_scales.cpp",
                 "/vagrant/via_hardware_executables/hardware_drivers/Via/modules/sync3/sync3_scales.cpp")

        copyfile("/vagrant/viatools/generated_code/sync3.hpp",
                 "/vagrant/via_hardware_executables/hardware_drivers/Via/modules/inc/sync3.hpp")
