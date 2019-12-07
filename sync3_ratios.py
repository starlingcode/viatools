
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

    def fill_octave(self, ratios):

        numerators = []
        denominators = []

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
                numerators.append(int(ratio[0] / 2))
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
                denominators.append(int(ratio[1] / 2))
            else:
                numerators.append(int(ratio[0] * 2))
                denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_tritave(self, ratios):

        numerators = []
        denominators = []

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
                numerators.append(int(ratio[0] / 3))
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
                denominators.append(int(ratio[1] / 3))
            else:
                numerators.append(int(ratio[0] * 3))
                denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_2octave(self, ratios):

        numerators = []
        denominators = []

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

        return numerators, denominators

    def fill_doubled(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        return numerators, denominators

    def fill_default(self, ratios):

        numerators = []
        denominators = []

        for ratio in ratios:
            numerators.append(int(ratio[0]))
            denominators.append(int(ratio[1]))

        return numerators, denominators

    def render(self):

        for scale in self.scales:

            ratios = self.scales[scale]["raw_ratios"]

            mode = self.scales[scale]["method"]

            if mode == "octave":

                numerators, denominators = self.fill_octave(ratios)

            elif mode == "tritave":

                numerators, denominators = self.fill_tritave(ratios)

            elif mode == "2octave":

                numerators, denominators = self.fill_2octave(ratios)

            elif mode == "doubled":

                numerators, denominators = self.fill_doubled(ratios)

            else:

                numerators, denominators = self.fill_default(ratios)

            precalcs = []

            for index, denominator in enumerate(denominators):
                precalc = int((2 ** 32) / denominator) % 4294967296
                precalcs.append(precalc)

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

        self.write_line("\n\tstatic const struct Sync3Scale * scales[8];", end="\n\n")
        self.write_line("\tconst uint32_t * numerators = " + scale + ".numerators;", end="\n")
        self.write_line("\tconst uint32_t * denominators = " + scale + ".denominators;", end="\n")
        self.write_line("\tconst uint32_t * dividedPhases = " + scale + ".dividedPhases;", end="\n")
        self.write_line("\tconst uint32_t * precalcs = " + scale + ".precalcs;", end="\n")

        self.write_line("\n/// INSERT SCALES", end="")

import sys
from shutil import copyfile
import requests
import os

if not os.path.isdir("generated_code"):
    os.mkdir("generated_code")

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
