import struct
import math
import numpy as np
from viatools.via_resource import ViaResource, ViaResourceSet

# looks like scale grids have a fixed size, 128 ratios by 8 rows
# ratios are packed, grid is a 2d array of addresses to ratios (offsets from start of ratio blob)
# grid might be able to be reduced to 16 bit int
# a scale is a pointer for the grid, the t2 bitshift struct member is constant, does the voct flag need to be there?

class SyncScale(ViaResource):

    def bake(self):
        self.baked = self.expand_scale(self.data)

    def expand_scale(self, recipe):

        ratios = recipe['grid']
        mode = recipe['method']

        baked = {}

        self.expand_modes = {
                        'octave': self.expand_octave,
                        'tritave': self.expand_tritave,
                        'expand': self.expand
                    }    

        expanded = self.expand_modes[mode](ratios)
        numerators = [ratio[0] for ratio in expanded]
        denominators = [ratio[1] for ratio in expanded]

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

        baked['numerators'] = numerators
        baked['denominators'] = denominators
        baked['precalcs'] = precalcs
        baked['keys'] = keys
        return baked

class SyncScaleSet(ViaResourceSet):

    def __init__(self, resource_dir, slug):
        super().__init__(Sync3Scale, slug, resource_dir, resource_dir + 'scales/')
        self.output_dir = resource_dir + 'binaries/'            
        # self.scale_size = 32
        self.slug = slug

    def bake(self):
        for resource in self.resources:
            resource.bake()

    def pack_binary(self, write_dir=None):
        if not write_dir:
            write_dir = self.output_dir
        sz = self.scale_size
        packer = struct.Struct('<%dI%dI%dI%dII' % (sz, sz, sz, sz))
        compiled_structs = []
        for resource in self.resources:
            resource.bake()
            scale = resource.baked
            print(len(scale['numerators']))
            pack = []
            for number in scale['numerators']:
                pack.append(number)
            for number in scale['denominators']:
                pack.append(number)
            for number in scale['precalcs']:
                pack.append(number) 
            for number in scale['keys']:
                pack.append(number)
            pack.append(0)
            compiled_structs.append(packer.pack(*pack))

        resource_path = write_dir + self.slug + '.sync-scale'

        with open(resource_path, 'wb') as outfile:
            for chunk in compiled_structs:
                outfile.write(chunk)

        return resource_path


class Scale:

    scales = []

    scale_holder = []
    global_pitch_set = set([])

    def read_scale_set(self):

        # iterate through ViaScales.csv, get scale names and generation qualifiers

        with open("scale_resources/scale_set.csv", newline="\n") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                if row[0] != "":
                    self.scales.append([row[0], row[1]])

    def parse_scale_set(self):

        # initialize an array and a set to collect the scale data from the CSV per scale in ViaScales
        # the set keeps us from redundantly defining ratio structs

        # iterate through the scales and parse the CSV for each scale with the appropriate function
        # see fullspangenerator.py and onevoltoctgenerator.py for details on the parsing

        for pitch_class_set in self.scales:

            scale_name = pitch_class_set[0]

            parse_type = pitch_class_set[1]

            # not yet implemented
            # is_pitch_class_set = pitch_class_set[2]

            # not yet implemented
            # is_pretiled = pitch_class_set[3]

            # call the the CSV parsing function
            if parse_type == "1":
                scale_parser = self.generate_tiled(scale_name)
            elif parse_type == "2":
                scale_parser = self.generate_ascending_descending(scale_name)
            elif parse_type == "3":
                scale_parser = self.generate_inversion_walk(scale_name)
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

            print(scale_tags)

            # the "scale holder" array translates this data to the code generation routine below
            self.scale_holder.append([full_scale, scale_tags, num_scales, scale_parser[4]])

    def write_vcvrack_key(self):

        text_file = open("generated_code/sync_scale_rack_key.hpp", "w")
        text_file.truncate()

        stub = open("scale_resources/scale_header.txt", "r")

        for line in stub:
            text_file.write(line)

        stub.close()

        text_file.write("\n\n")

        num_bytes = 0
        word_size = 4

        # initialize an empty set to make sure we don't define any scale rows more than once

        scale_set = set([])

        for s in self.scales:

            full_scale = self.scale_holder[self.scales.index(s)][0]
            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]
            key = self.scale_holder[self.scales.index(s)][3]

            for pitch_class_set in range(0, num_scales):

                # see if the row has been defined yet

                if scale_tags[pitch_class_set] not in scale_set:

                    # if not, print the 128 value array of pointers to the ratio structs defined earlier

                    for grid_index in range(0, 128):

                        ratio_tag = str(key[pitch_class_set][grid_index])

                        num_bytes += word_size;

                        if grid_index == 0:
                            text_file.write(
                                "std::string " + scale_tags[pitch_class_set] + "[128] = {\"" + ratio_tag + "\", ")
                        elif grid_index != 127:
                            if grid_index % 12 != 0:
                                text_file.write("\"" + ratio_tag + "\", ")
                            else:
                                text_file.write("\"" + ratio_tag + "\", \n")
                        else:
                            text_file.write("\"" + ratio_tag + "\"}; \n\n")

                # add the scale we just printed to the set to avoid defining it again

                scale_set.add(scale_tags[pitch_class_set])

            text_file.write("\n\n")

        text_file.write("\n\n\n")

        # define the "grids" used by our scales by specifying a set of rows as defined above

        for s in self.scales:

            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]
            scale_name = s[0]

            for pitch_class_set in range(len(scale_tags)):

                num_bytes += word_size

                if pitch_class_set == 0:
                    text_file.write(
                        "std::string* " + scale_name + "Grid[" + str(num_scales) + "] = {" + scale_tags[
                            pitch_class_set] + ", ")
                elif pitch_class_set != (len(scale_tags) - 1):
                    text_file.write(scale_tags[pitch_class_set] + ", ")
                else:
                    text_file.write(scale_tags[pitch_class_set] + "}; \n\n")

        text_file.write("\n\n\n")

        # define the actual scale structs

        # for s in self.scales:
        #     scale_name = s[0]
        #     if s[1] == "1":
        #         one_v_oct_on = str(1)
        #     else:
        #         one_v_oct_on = str(0)
        #     num_scales = self.scale_holder[self.scales.index(s)][2]
        #     # calculate the size of the bitshift needed to scale the T2 control across full set of rows
        #     t2bitshift = str(int(math.log(4095 // num_scales, 2) + 1))
        #     text_file.write("static const Scale " + scale_name + " = {\n")
        #     text_file.write("   .grid = " + scale_name + "Grid,\n")
        #     text_file.write("   .t2Bitshift = " + t2bitshift + ",\n")
        #     text_file.write("   .oneVoltOct = " + one_v_oct_on + "};\n\n")

        text_file.write("#endif /* INC_SCALES_HPP_ */")

        print("These should take up ~ " + str(num_bytes) + " bytes")

        text_file.close()

    def write_scale_header(self):

        text_file = open("generated_code/sync_scale_defs.hpp", "w")
        text_file.truncate()

        stub = open("scale_resources/scale_header.txt", "r")

        for line in stub:
            text_file.write(line)

        stub.close()

        text_file.write("\n\n")

        num_bytes = 0
        word_size = 4

        # write all the ratios used throughout our scales

        for pitch_class_set in self.global_pitch_set:
            ratio_tag = pitch_class_set[0]
            integer_part = pitch_class_set[1]
            fractional_part = pitch_class_set[2]
            fundamental_divisor = pitch_class_set[3]
            num_bytes += word_size * 4
            text_file.write("static const ScaleNote " + ratio_tag + " = {" + str(integer_part) + ", " + str(
                fractional_part) + ", " + str(fundamental_divisor) + "};\n")

        text_file.write("\n\n\n")

        # initialize an empty set to make sure we don't define any scale rows more than once

        scale_set = set([])

        for s in self.scales:

            full_scale = self.scale_holder[self.scales.index(s)][0]
            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]

            for pitch_class_set in range(0, num_scales):

                # see if the row has been defined yet

                if scale_tags[pitch_class_set] not in scale_set:

                    # if not, print the 128 value array of pointers to the ratio structs defined earlier

                    for grid_index in range(0, 128):

                        ratio_tag = str(full_scale[pitch_class_set][grid_index][0])

                        num_bytes += word_size;

                        if grid_index == 0:
                            text_file.write(
                                "static const ScaleNote * const " + scale_tags[pitch_class_set] + "[128] = {&" + ratio_tag + ", ")
                        elif grid_index != 127:
                            if grid_index % 12 != 0:
                                text_file.write("&" + ratio_tag + ", ")
                            else:
                                text_file.write("&" + ratio_tag + ", \n")
                        else:
                            text_file.write("&" + ratio_tag + "}; \n\n")

                # add the scale we just printed to the set to avoid defining it again

                scale_set.add(scale_tags[pitch_class_set])

            text_file.write("\n\n")

        text_file.write("\n\n\n")

        # define the "grids" used by our scales by specifying a set of rows as defined above

        for s in self.scales:

            scale_tags = self.scale_holder[self.scales.index(s)][1]
            num_scales = self.scale_holder[self.scales.index(s)][2]
            scale_name = s[0]

            for pitch_class_set in range(len(scale_tags)):

                num_bytes += word_size

                if pitch_class_set == 0:
                    text_file.write(
                        "static const ScaleNote* const*" + scale_name + "Grid[" + str(num_scales) + "] = {" + scale_tags[
                            pitch_class_set] + ", ")
                elif pitch_class_set != (len(scale_tags) - 1):
                    text_file.write(scale_tags[pitch_class_set] + ", ")
                else:
                    text_file.write(scale_tags[pitch_class_set] + "}; \n\n")

        text_file.write("\n\n\n")

        # define the actual scale structs

        for s in self.scales:
            scale_name = s[0]
            if s[1] == "1":
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

        print("These should take up ~ " + str(num_bytes) + " bytes")

        text_file.close()

    def write_scale_code(self):

        text_file = open("generated_code/sync_scales.cpp", "w")
        text_file.truncate()

        text_file.write("\n#include \"sync.hpp\"\n\n")

        text_file.write("void ViaSync::initializeScales() {\n")
        for pitch_class_set in range(0, 16):
            scale_name = self.scales[pitch_class_set][0]
            text_file.write("   scaleArray[" + str(int(pitch_class_set/4)) + "][" + str(pitch_class_set % 4) + "] = &" + scale_name + ";\n")
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
            for file in sorted(files):
                with open("scale_resources/scale_defs/" + scale_name + "/" + file, newline="\n") as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:
                        if row[0] != "":
                            # the first column is the string identifier for the row
                            scale_tags.append(file[:-4])
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

        for pitch_class_set in interval_table:

            row_pointer = interval_table.index(pitch_class_set)

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

            for grid_index in interval_table[row_pointer]:
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

        for pitch_class_set in ratio_table:

            row_pointer = ratio_table.index(pitch_class_set)

            # figure out the octave relation to the fundamental that forms a lower bound

            lower_bound = 8

            while (min(interval_table[row_pointer])) < lower_bound:
                lower_bound = lower_bound - 1

            # use this to offset our indices to start at 0

            pad = -lower_bound * 12

            for grid_index in ratio_table[row_pointer]:

                interval_pointer = ratio_table[row_pointer].index(grid_index)

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

        raw_ratios = []

        for pitch_class_set in ratio_table:

            row_pointer = ratio_table.index(pitch_class_set)

            for grid_index in ratio_table[row_pointer]:

                interval_pointer = ratio_table[row_pointer].index(grid_index)

                starting_index = start_end_table[row_pointer][interval_pointer][0]

                last_index = start_end_table[row_pointer][interval_pointer][1]

                idx = starting_index

                while idx <= last_index:
                    subtile.append(tuple(ratio_table[row_pointer][interval_pointer][0:2]))
                    idx += 1

            tiles.append(subtile)

            subtile = []

        # print(tiles)

        # use those tiles to map out a 1vOct space across 128 indices (10 and 2/3 octaves)
        # precalculate the ratio to fix48
        # calculate the fundamental divisor if it was not specified in the scale CSV

        full_scale = []
        full_row = []
        pitch_set = set([])

        for pitch_class_set in tiles:

            raw_ratio_row = []

            row_pointer = tiles.index(pitch_class_set)

            grid_index = 0

            while grid_index < 64:

                octave = int(grid_index // len(pitch_class_set)) * octave_spans[row_pointer]

                numerator_int = int(tiles[row_pointer][grid_index % len(pitch_class_set)][0])

                denominator_int = int(tiles[row_pointer][grid_index % len(pitch_class_set)][1])

                temp_numerator = numerator_int * 2 ** octave

                raw_ratio_row.append(str(temp_numerator) + "/" + str(denominator_int))

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

                grid_index += 1

            grid_index = 63

            while grid_index >= 0:
                octave = abs((grid_index - 64) // len(pitch_class_set)) * octave_spans[row_pointer]

                numerator_int = int(tiles[row_pointer][(len(pitch_class_set) - (64 - grid_index)) % len(pitch_class_set)][0])

                denominator_int = int(tiles[row_pointer][(len(pitch_class_set) - (64 - grid_index)) % len(pitch_class_set)][1])

                temp_denominator = denominator_int * 2 ** octave

                raw_ratio_row.append(str(numerator_int) + "/" + str(temp_denominator))

                divisor = math.gcd(int(numerator_int), int(temp_denominator))

                fundamental_divisor = int(temp_denominator / divisor)

                ratio_tag = "ratio" + str(int(numerator_int / divisor)) + "_" + str(int(temp_denominator / divisor))

                fix32_calculation = int(numerator_int * 2 ** 48 / temp_denominator)

                integer_part = fix32_calculation >> 32

                fractional_part = fix32_calculation - (integer_part << 32)

                ratio_holder = (ratio_tag, integer_part, fractional_part, fundamental_divisor)

                full_row.insert(0, ratio_holder)

                grid_index -= 1

                if ratio_holder not in pitch_set:
                    pitch_set.add(ratio_holder)

            raw_ratio_row.reverse()

            raw_ratios.append(raw_ratio_row)

            full_scale.append(full_row)
            full_row = []

        return [full_scale, pitch_set, scale_tags, num_scales, raw_ratios]

    def generate_full_span(self, scale_name):

        # initialize lists to parse the csv
        ratio_subset = []
        ratio_table = []
        scale_tags = []

        # parse the csv for integer ratios
        # scale per row format
        for root, dirs, files in os.walk("scale_resources/scale_defs/" + scale_name):
            for file in sorted(files):
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

        # print(ratio_table)

        num_scales = len(scale_tags)
        pitch_set = set([])
        full_scale = []
        full_row = []

        # spread each row evenly across the full 128 index span

        # calculate the ratio in Q16.48

        # calcualte the PLL divisor if we didn't specify it in the CSV

        raw_ratios = []

        for pitch_class_set in ratio_table:

            raw_ratio_row = []

            row_pointer = ratio_table.index(pitch_class_set)

            grid_index = 0

            while grid_index < 128:

                numerator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][0])

                denominator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][1])

                raw_ratio_row.append(str(numerator_int) + "/" + str(denominator_int))

                divisor = math.gcd(int(numerator_int), int(denominator_int))

                if len(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)]) == 3:
                    fundamental_divisor = ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][2]
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

                grid_index += 1

            full_scale.append(full_row)
            full_row = []
            raw_ratios.append(raw_ratio_row)

        return [full_scale, pitch_set, scale_tags, num_scales, raw_ratios]

    def generate_ascending_descending(self, scale_name):

        # initialize lists to parse the csv
        ratio_subset = []
        ratio_table = []
        scale_tags = []

        row_counter = "skip"
        stored_row = []
        stored_tag = ""

        # parse the csv for integer ratios
        # scale per row format
        for root, dirs, files in os.walk("scale_resources/scale_defs/" + scale_name):
            for file in sorted(files):
                with open("scale_resources/scale_defs/" + scale_name + "/" + file, newline="\n") as csvfile:
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

                ratio_subset.sort(key=lambda x: x[0] / x[1])

                if row_counter == "skip":
                    row_counter = "use"
                    for ratio in ratio_subset:
                        stored_row.append(ratio)
                    stored_tag = file.rstrip(".csv")
                    ratio_subset = []
                else:
                    scale_tags.append(stored_tag + "_vs_" + file.rstrip(".csv"))
                    ratio_subset.reverse()
                    for ratio in ratio_subset:
                        stored_row.append(ratio)
                    ratio_table.append(stored_row)
                    ratio_subset = []
                    stored_row = []
                    row_counter = "skip"

        # print(ratio_table)

        num_scales = len(scale_tags)
        pitch_set = set([])
        full_scale = []
        full_row = []

        # spread each row evenly across the full 128 index span

        # calculate the ratio in Q16.48

        # calcualte the PLL divisor if we didn't specify it in the CSV

        raw_ratios = []

        for pitch_class_set in ratio_table:

            raw_ratio_row = []

            row_pointer = ratio_table.index(pitch_class_set)

            grid_index = 0

            while grid_index < 128:

                numerator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][0])

                denominator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][1])

                divisor = math.gcd(int(numerator_int), int(denominator_int))

                raw_ratio_row.append(str(numerator_int) + "/" + str(denominator_int))

                if len(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)]) == 3:
                    fundamental_divisor = ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][2]
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

                grid_index += 1

            full_scale.append(full_row)
            full_row = []
            raw_ratios.append(raw_ratio_row)

        # print(raw_ratios)

        return [full_scale, pitch_set, scale_tags, num_scales, raw_ratios]

    def generate_inversion_walk(self, scale_name):

        # initialize lists to parse the csv
        ratio_subset = []
        ratio_table = []
        scale_tags = []

        stored_row = []

        # parse the csv for integer ratios
        # scale per row format
        for root, dirs, files in os.walk("scale_resources/scale_defs/" + scale_name):
            for file in sorted(files):
                with open("scale_resources/scale_defs/" + scale_name + "/" + file, newline="\n") as csvfile:
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

                ratio_subset.sort(key=lambda x: x[0] / x[1])

                scale_tags.append(file.rstrip(".csv") + "inversion_walk")

                octave_span = int(math.log(ratio_subset[-1][0]/ratio_subset[-1][1], 2)) - int(math.log(ratio_subset[0][0]/ratio_subset[0][1], 2))
                octave_span += 1
                inversion = []

                for position, ratio in enumerate(ratio_subset):

                    for ratio in ratio_subset[position:]:
                        inversion.append(ratio)

                    if position > 0:
                        for ratio in ratio_subset[0:position]:
                            translated_ratio = []
                            translated_ratio.append(ratio[0])
                            translated_ratio.append(ratio[1])
                            translated_ratio[0] *= 2
                            inversion.append(translated_ratio)

                ratio_table.append(inversion)
                ratio_subset = []
                stored_row = []

        # print(ratio_table)

        num_scales = len(scale_tags)
        pitch_set = set([])
        full_scale = []
        full_row = []

        # spread each row evenly across the full 128 index span

        # calculate the ratio in Q16.48

        # calcualte the PLL divisor if we didn't specify it in the CSV

        raw_ratios = []

        for pitch_class_set in ratio_table:

            raw_ratio_row = []

            row_pointer = ratio_table.index(pitch_class_set)

            grid_index = 0

            while grid_index < 128:

                numerator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][0])

                denominator_int = int(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][1])

                raw_ratio_row.append(str(numerator_int) + "/" + str(denominator_int))

                divisor = math.gcd(int(numerator_int), int(denominator_int))

                if len(ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)]) == 3:
                    fundamental_divisor = ratio_table[row_pointer][int(grid_index * len(pitch_class_set) / 128)][2]
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

                grid_index += 1

            full_scale.append(full_row)
            full_row = []
            raw_ratios.append(raw_ratio_row)

        # print(raw_ratios)

        return [full_scale, pitch_set, scale_tags, num_scales, raw_ratios]
