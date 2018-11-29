import csv
import math
import os

class Scales:

    scales = []

    scale_holder = []
    global_pitch_set = set([])

    def read_scale_set(self):

        # iterate through ViaScales.csv, get scale names and generation qualifiers

        with open("scale_resources/scale_set.csv", newline="\n") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row[0] != "":
                    self.scales.append([row[0], row[1], row[2], row[3]])

        print(self.scales)

    def parse_scale_set(self):

        # initialize an array and a set to collect the scale data from the CSV per scale in ViaScales
        # the set keeps us from redundantly defining ratio structs

        # iterate through the scales and parse the CSV for each scale with the appropriate function
        # see fullspangenerator.py and onevoltoctgenerator.py for details on the parsing

        for i in self.scales:

            scale_name = i[0]

            is_1voct = i[1]

            # not yet implemented
            # is_pitch_class_set = i[2]

            # not yet implemented
            # is_pretiled = i[3]

            # call the the CSV parsing function
            if is_1voct == "on":
                scale_parser = self.generate_tiled(scale_name)
            else:
                scale_parser = self.generate_full_span(scale_name)

            # the parsing functions return an array with 4 complex entries in the first dimension
            # we assign legible variables to those

            # the actual ratios comprising the scale in a 2d array
            full_scale = scale_parser[0]

            # the ratio data, reduced to a set
            pitch_set = scale_parser[1]

            # the string names for each row in full_scale
            scale_tags = scale_parser[2]

            # the number of rows in this scale (a power of 2)
            num_scales = scale_parser[3]

            # add the pitch set to the global pitch set that we are collecting
            self.global_pitch_set = self.global_pitch_set | pitch_set

            # the "scale holder" array translates this data to the code generation routine below
            self.scale_holder.append([full_scale, scale_tags, num_scales])

    def write_scale_header(self):

        text_file = open("generated_code/scales.hpp", "w")
        text_file.truncate()

        stub = open("scale_resources/scale_header.txt", "r")

        for line in stub:
            text_file.write(line)

        stub.close()

        text_file.write("\n\n")

        # write all the ratios used throughout our scales

        for i in self.global_pitch_set:
            ratio_tag = i[0]
            integer_part = i[1]
            fractional_part = i[2]
            fundamental_divisor = i[3]
            text_file.write("static const ScaleNote " + ratio_tag + " = {" + str(integer_part) + ", " + str(
                fractional_part) + ", " + str(fundamental_divisor) + "};\n")

        text_file.write("\n\n\n")

        # initialize an empty set to make sure we don't define any scale rows more than once

        scale_set = set([])

        for s in self.scales:

            full_scale = self.scale_holder[self.scales.index(s)][0]
            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]

            print(num_scales)
            print(scale_tags)
            print(s[0])

            for i in range(0, num_scales):

                # see if the row has been defined yet

                if scale_tags[i] not in scale_set:

                    # if not, print the 128 value array of pointers to the ratio structs defined earlier

                    for j in range(0, 128):

                        ratio_tag = str(full_scale[i][j][0])

                        if j == 0:
                            text_file.write(
                                "static const ScaleNote * const " + scale_tags[i] + "[128] = {&" + ratio_tag + ", ")
                        elif j != 127:
                            if j % 12 != 0:
                                text_file.write("&" + ratio_tag + ", ")
                            else:
                                text_file.write("&" + ratio_tag + ", \n")
                        else:
                            text_file.write("&" + ratio_tag + "}; \n\n")

                # add the scale we just printed to the set to avoid defining it again

                scale_set.add(scale_tags[i])

            text_file.write("\n\n")

        text_file.write("\n\n\n")

        # define the "grids" used by our scales by specifying a set of rows as defined above

        for s in self.scales:

            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]
            scale_name = s[0]

            for i in range(len(scale_tags)):

                if i == 0:
                    text_file.write(
                        "static const ScaleNote* const*" + scale_name + "Grid[" + str(num_scales) + "] = {" + scale_tags[
                            i] + ", ")
                elif i != (len(scale_tags) - 1):
                    text_file.write(scale_tags[i] + ", ")
                else:
                    text_file.write(scale_tags[i] + "}; \n\n")

        text_file.write("\n\n\n")

        # define the actual scale structs

        for s in self.scales:
            scale_name = s[0]
            if s[1] == "on":
                one_v_oct_on = str(1)
            else:
                one_v_oct_on = str(0)
            num_scales = self.scale_holder[self.scales.index(s)][2]
            # calculate the size of the bitshift needed to scale the T2 control across full set of rows
            t2bitshift = str(int(math.log(4095 // num_scales, 2) + 1))
            text_file.write("static const Scale " + scale_name + " = {\n")
            text_file.write("   .grid = " + scale_name + "Grid,\n")
            text_file.write("   .t2Bitshift = " + t2bitshift + ",\n")
            text_file.write("   .oneVoltOct = " + one_v_oct_on + "};\n\n")

        text_file.write("#endif /* INC_SCALES_HPP_ */")

        text_file.close()

    def write_scale_code(self):

        text_file = open("generated_code/sync_scales.cpp", "w")
        text_file.truncate()

        text_file.write("\n#include \"sync.hpp\"\n\n")

        text_file.write("void ViaSync::initializeScales() {\n")
        for i in range(0, 16):
            scale_name = self.scales[i][0]
            text_file.write("   scaleArray[" + str(int(i/4)) + "][" + str(i % 4) + "] = &" + scale_name + ";\n")
        text_file.write("}\n")

    def generate_tiled(self, scale_name):

        # initialize lists to parse the csv
        ratio_subset = []
        ratio_table = []
        interval_subset = []
        interval_table = []
        scale_tags = []

        # parse the csv for integer ratios and calculate an interval in terms of octaves

        for root, dirs, files in os.walk("scale_resources/scale_defs/" + scale_name):
            for file in files:
                with open("scale_resources/scale_defs/" + scale_name + "/" + file, newline="\n") as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        if row[0] != "":
                            # the first column is the string identifier for the row
                            scale_tags.append(file.rstrip(".csv"))
                            # each following column contains a ratio
                            for cell in row:
                                # a required slash separates numerator from denominator
                                if "/" in cell:
                                    delim1 = cell.index("/")
                                    # an optional dash separates the ratio from the PLL divider
                                    if "-" in cell:
                                        delim2 = cell.index("-")
                                        ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:delim2]), int(cell[delim2 + 1:])]
                                    else:
                                        ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:])]
                                    # store the ratio as a list
                                    ratio_subset.append(ratio)
                                    # calculate the interval from the fundamental (1/1) in octaves
                                    interval_subset.append(math.log(float(ratio[0] / ratio[1]), 2))
                            # collect the rows of ratios and intervals
                ratio_table.append(ratio_subset)
                ratio_subset = []
                interval_table.append(interval_subset)
                interval_subset = []

        # Calculate octave bin for each interval in each scale and append to the first table

        row_pointer = 0
        octave_spans = []

        for i in interval_table:

            row_pointer = interval_table.index(i)

            print(scale_tags[row_pointer])
            print(scale_name)

            # figure out the octave relation to the fundamental that forms a lower bound

            lower_bound = 8

            # assume that the highest interval is less than 8 octaves lower than the fundamental

            octave_checker_positive = -8

            # see if thats true, if not, check the octave above and above ...

            while max(interval_table[row_pointer]) > octave_checker_positive:
                octave_checker_positive = octave_checker_positive + 1

            # perform the analogous check with the lowest interval, starting at 8 octaves up

            octave_checker_negative = 8

            while min(interval_table[row_pointer]) < octave_checker_negative:
                octave_checker_negative = octave_checker_negative - 1

            # this allows us to determine the span in octaves that contains all of our intervals

            octave_checker = octave_checker_positive - octave_checker_negative

            interval_pointer = 0

            for j in interval_table[row_pointer]:
                # iterate through our intervals and define them in semi-tones by multiplying by 12

                ratio_table[row_pointer][interval_pointer].append(
                    int(12 * interval_table[row_pointer][interval_pointer]))
                interval_pointer = interval_pointer + 1

            # sort those for ascending order

            ratio_table[row_pointer].sort(key=lambda x: int(x[2]))

            # store the octave span

            octave_spans.append(octave_checker)
            row_pointer = row_pointer + 1

        num_scales = len(scale_tags)

        # get start and end indices for each scale in the n octave tile of best fit
        # there are 12 entries per octave, so we might want to evenly space 4 intervals across 1 octave
        # this function gives the index range for each interval within the 12 indices that comprise the octave

        start_end_table = []
        start_end_subset = []

        for i in ratio_table:

            row_pointer = ratio_table.index(i)

            # figure out the octave relation to the fundamental that forms a lower bound

            lower_bound = 8

            while (min(interval_table[row_pointer])) < lower_bound:
                lower_bound = lower_bound - 1

            # use this to offset our indices to start at 0

            pad = -lower_bound * 12

            for j in ratio_table[row_pointer]:

                interval_pointer = ratio_table[row_pointer].index(j)

                # set the start and end indices to the average between the interval and the ones above and below
                # since we epressed our intervals in semitones, that translates naturally to tile indices
                # (12 indices per octave)
                if interval_pointer == 0:

                    start = 0
                    end = pad + int(
                        (ratio_table[row_pointer][interval_pointer][2] + ratio_table[row_pointer][interval_pointer + 1][
                            2]) / 2)
                    start_end_subset.append([start, end])

                elif interval_pointer != (len(ratio_table[row_pointer]) - 1):

                    start = start_end_subset[interval_pointer - 1][1] + 1
                    end = pad + int(
                        (ratio_table[row_pointer][interval_pointer][2] + ratio_table[row_pointer][interval_pointer + 1][
                            2]) / 2)
                    start_end_subset.append([start, end])

                else:

                    start = start_end_subset[interval_pointer - 1][1] + 1
                    end = octave_spans[row_pointer] * 12 - 1
                    start_end_subset.append([start, end])

            start_end_table.append(start_end_subset)
            start_end_subset = []

        # generate the n octave sized tile for each row using the indices from above

        subtile = []
        tiles = []

        for i in ratio_table:

            row_pointer = ratio_table.index(i)

            print(scale_tags[row_pointer])

            for j in ratio_table[row_pointer]:

                interval_pointer = ratio_table[row_pointer].index(j)

                starting_index = start_end_table[row_pointer][interval_pointer][0]

                last_index = start_end_table[row_pointer][interval_pointer][1]

                idx = starting_index

                while idx <= last_index:
                    subtile.append(tuple(ratio_table[row_pointer][interval_pointer][0:2]))
                    idx += 1

            tiles.append(subtile)

            subtile = []

        # use those tiles to map out a 1vOct space across 128 indices (10 and 2/3 octaves)
        # precalculate the ratio to fix48
        # calculate the fundamental divisor if it was not specified in the scale CSV

        full_scale = []
        full_row = []
        pitch_set = set([])

        for i in tiles:

            row_pointer = tiles.index(i)

            j = 0

            while j < 64:

                octave = int(j // len(i)) * octave_spans[row_pointer]

                numerator_int = int(tiles[row_pointer][j % len(i)][0])

                denominator_int = int(tiles[row_pointer][j % len(i)][1])

                temp_numerator = numerator_int * 2 ** octave

                divisor = math.gcd(int(temp_numerator), int(denominator_int))

                fundamental_divisor = int(denominator_int / divisor)

                ratio_tag = "ratio" + str(int(temp_numerator / divisor)) + "_" + str(int(denominator_int / divisor))

                fix32_calculation = int(temp_numerator * 2 ** 48 / denominator_int)

                integer_part = fix32_calculation >> 32

                fractional_part = fix32_calculation - (integer_part << 32)

                ratio_holder = (ratio_tag, integer_part, fractional_part, fundamental_divisor)

                if ratio_holder not in pitch_set:
                    pitch_set.add(ratio_holder)

                full_row.append(ratio_holder)

                j += 1

            j = 63

            while j >= 0:
                octave = abs((j - 64) // len(i)) * octave_spans[row_pointer]

                numerator_int = int(tiles[row_pointer][(len(i) - (64 - j)) % len(i)][0])

                denominator_int = int(tiles[row_pointer][(len(i) - (64 - j)) % len(i)][1])

                temp_denominator = denominator_int * 2 ** octave

                divisor = math.gcd(int(numerator_int), int(temp_denominator))

                fundamental_divisor = int(temp_denominator / divisor)

                ratio_tag = "ratio" + str(int(numerator_int / divisor)) + "_" + str(int(temp_denominator / divisor))

                fix32_calculation = int(numerator_int * 2 ** 48 / temp_denominator)

                integer_part = fix32_calculation >> 32

                fractional_part = fix32_calculation - (integer_part << 32)

                ratio_holder = (ratio_tag, integer_part, fractional_part, fundamental_divisor)

                full_row.insert(0, ratio_holder)

                j -= 1

                if ratio_holder not in pitch_set:
                    pitch_set.add(ratio_holder)

            full_scale.append(full_row)
            full_row = []

        print(full_scale)

        return [full_scale, pitch_set, scale_tags, num_scales]

    def generate_full_span(self, scale_name):

        # initialize lists to parse the csv
        ratio_subset = []
        ratio_table = []
        scale_tags = []

        # parse the csv for integer ratios
        # scale per row format
        for root, dirs, files in os.walk("scale_resources/scale_defs/" + scale_name):
            for file in files:
                with open("scale_resources/scale_defs/" + scale_name + "/" + file, newline="\n") as csvfile:
                    scale_tags.append(file.rstrip(".csv"))
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        for cell in row:
                            if "/" in cell:
                                delim1 = cell.index("/")
                                if "-" in cell:
                                    delim2 = cell.index("-")
                                    ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:delim2]), int(cell[delim2 + 1:])]
                                else:
                                    ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:])]
                                ratio_subset.append(ratio)
                ratio_table.append(ratio_subset)
                ratio_subset = []

        num_scales = len(scale_tags)
        pitch_set = set([])
        full_scale = []
        full_row = []

        # spread each row evenly across the full 128 index span

        # calculate the ratio in Q16.48

        # calcualte the PLL divisor if we didn't specify it in the CSV

        for i in ratio_table:

            row_pointer = ratio_table.index(i)

            j = 0

            while j < 128:

                print(scale_tags[row_pointer])

                numerator_int = int(ratio_table[row_pointer][int(j * len(i) / 128)][0])

                denominator_int = int(ratio_table[row_pointer][int(j * len(i) / 128)][1])

                divisor = math.gcd(int(numerator_int), int(denominator_int))

                if len(ratio_table[row_pointer][int(j * len(i) / 128)]) == 3:
                    fundamental_divisor = ratio_table[row_pointer][int(j * len(i) / 128)][2]
                    ratio_tag = "ratio" + str(int(numerator_int / divisor)) + "_" + str(
                        int(denominator_int / divisor)) + "_" + str(fundamental_divisor)

                else:
                    fundamental_divisor = int(denominator_int / divisor)
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
