# helper functions to generate scale code for the pll via

import math

import csv


def makeScale1voct(scale_name):

    # initialize lists to parse the csv
    ratio_subset = []
    ratio_table = []
    interval_subset = []
    interval_table = []
    scale_tags = []

    # parse the csv for integer ratios and calculate an interval in terms of octaves

    with open(scale_name + ".csv", newline="\n") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] != "":
                # the first column is the string identifier for the row
                scale_tags.append(row[0])
                # each following column contains a ratio
                for cell in row[1:]:
                    # a required slash separates numerator from denominator
                    if "/" in cell:
                        delim1 = cell.index("/")
                        # an optional dash separates the ratio from the PLL divider
                        if "-" in cell:
                            delim2 = cell.index("-")
                            ratio = [int(cell[0:delim1]), int(cell[delim1 + 1:delim2]), int(cell[delim2+1:])]
                        else:
                            ratio = [int(cell[0:delim1]), int(cell[delim1+1:])]
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

            ratio_table[row_pointer][interval_pointer].append(int(12 * interval_table[row_pointer][interval_pointer]))
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

                start = 0;
                end = pad + int(
                    (ratio_table[row_pointer][interval_pointer][2] + ratio_table[row_pointer][interval_pointer + 1][2]) / 2)
                start_end_subset.append([start, end])

            elif interval_pointer != (len(ratio_table[row_pointer]) - 1):

                start = start_end_subset[interval_pointer - 1][1] + 1;
                end = pad + int(
                    (ratio_table[row_pointer][interval_pointer][2] + ratio_table[row_pointer][interval_pointer + 1][2]) / 2)
                start_end_subset.append([start, end])

            else:

                start = start_end_subset[interval_pointer - 1][1] + 1;
                end = octave_spans[row_pointer] * 12 - 1
                start_end_subset.append([start, end])

        start_end_table.append(start_end_subset)
        start_end_subset = []

    # generate the n octave sized tile for each row using the indices from above

    subtile = []
    tiles = []

    for i in ratio_table:

        row_pointer = ratio_table.index(i)

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


