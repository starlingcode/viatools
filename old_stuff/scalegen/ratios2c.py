# tool to generate scale code for the pll via

import csv

import math

from onevoltoctgenerator import makeScale1voct

from fullspangenerator import makeScaleFullSpan

# create an empty array to hold the scale struct definitions
scales = []

# iterate through ViaScales.csv, get scale names and generation qualifiers

with open("ViaScales.csv", newline="\n") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[0] != "":
            scales.append([row[0], row[1], row[2], row[3]])

# initialize an array and a set to collect the scale data from the CSV per scale in ViaScales
# the set keeps us from redundantly defining ratio structs

scale_holder = []
global_pitch_set = set([])

# iterate through the scales and parse the CSV for each scale with the appropriate function
# see fullspangenerator.py and onevoltoctgenerator.py for details on the parsing

for i in scales:
    scale_name = i[0]

    is_1voct = i[1]

    # not yet implemented
    is_pitch_class_set = i[2]

    # not yet implemented
    is_pretiled = i[3]

    # call the the CSV parsing function
    if is_1voct == "on":
        scaleParser = makeScale1voct(scale_name)
    else:
        scaleParser = makeScaleFullSpan(scale_name)

    # the parsing functions return an array with 4 complex entries in the first dimension
    # we assign legible variables to those

    # the actual ratios comprising the scale in a 2d array
    full_scale = scaleParser[0]

    # the ratio data, reduced to a set
    pitch_set = scaleParser[1]

    # the string names for each row in full_scale
    scale_tags = scaleParser[2]

    # the number of rows in this scale (a power of 2)
    num_scales = scaleParser[3]

    # add the pitch set to the global pitch set that we are collecting
    global_pitch_set = global_pitch_set | pitch_set

    # the "scale holder" array translates this data to the code generation routine below
    scale_holder.append([full_scale, scale_tags, num_scales])


text_file = open("scales.h", "w")
text_file.truncate()

#####################

text_file.write('#include "stm32f3xx_hal.h"\n')
text_file.write('#include "stm32f3xx.h"\n')
text_file.write('#include "stm32f3xx_it.h"\n')
text_file.write("\n\n\n")
text_file.write("typedef struct {\n")
text_file.write("	const uint32_t integerPart;\n")
text_file.write("	const uint32_t fractionalPart;\n")
text_file.write("	const uint32_t fundamentalDivision;\n")
text_file.write("} ScaleNote;\n")
text_file.write("\n\n\n")
text_file.write("typedef struct {\n")
text_file.write("	ScaleNote ***grid;\n")
text_file.write("	uint32_t t2Bitshift;\n")
text_file.write("	uint32_t oneVoltOct;\n")
text_file.write("} Scale;\n")
text_file.write("\n\n\n")
text_file.write("Scale scaleGroup[16];\n")
text_file.write("\n\n\n")

# declare global handles for the grid and scale structs

for i in scales:
    scale_name = i[0]
    num_scales = scale_holder[scales.index(i)][2]
    text_file.write("static const ScaleNote **" + scale_name + "Grid[" + str(num_scales) + "];\n")
    text_file.write("Scale " + scale_name + ";\n")


text_file.write("\n\n")

# write all the ratios used throughout our scales

for i in global_pitch_set:
    ratio_tag = i[0]
    integer_part = i[1]
    fractional_part = i[2]
    fundamental_divisor = i[3]
    text_file.write("static const ScaleNote " + ratio_tag + " = {" + str(integer_part) + ", " + str(fractional_part) + ", " + str(fundamental_divisor) + "};\n")

text_file.write("\n\n\n")

# initialize an empty set to make sure we don't define any scale rows more than once

scale_set = set([])

for s in scales:

    full_scale = scale_holder[scales.index(s)][0]
    scale_tags = scale_holder[scales.index(s)][1]
    num_scales = scale_holder[scales.index(s)][2]

    print(num_scales)

    for i in range(0, num_scales):

        # see if the row has been defined yet

        if scale_tags[i] not in scale_set:

            # if not, print the 128 value array of pointers to the ratio structs defined earlier

            for j in range(0, 128):

                ratio_tag = str(full_scale[i][j][0])

                if j == 0:
                    text_file.write("static const ScaleNote * const " + scale_tags[i] + "[128] = {&" + ratio_tag + ", ")
                elif j != 127:
                    if j%12 != 0:
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

for s in scales:

    scale_tags = scale_holder[scales.index(s)][1]
    num_scales = scale_holder[scales.index(s)][2]
    scale_name = s[0]

    for i in range(len(scale_tags)):

        if i == 0:
            text_file.write("static const ScaleNote **" + scale_name + "Grid["+str(num_scales)+"] = {" + scale_tags[i] + ", ")
        elif i != (len(scale_tags) - 1):
            text_file.write(scale_tags[i] + ", ")
        else:
            text_file.write(scale_tags[i] + "}; \n\n")

text_file.write("\n\n\n")

text_file.close()

text_file = open("scales.c", "w")
text_file.truncate()

text_file.write('#include "scales.h"\n')

text_file.write('#include "main.h"\n')

text_file.write('#include "stm32f3xx_hal.h"\n')
text_file.write('#include "stm32f3xx.h"\n')
text_file.write('#include "stm32f3xx_it.h"\n')

text_file.write("\n\n\n")


# define the actual scale structs

for s in scales:
    scale_name = s[0]
    if s[1] == "on":
        oneVoct_on = str(1)
    else:
        oneVoct_on = str(0)
    num_scales = scale_holder[scales.index(s)][2]
    # calculate the size of the bitshift needed to scale the T2 control across full set of rows
    t2bitshift = str(int(math.log(4095//num_scales, 2)))
    text_file.write("Scale " + scale_name + " = {\n")
    text_file.write("   .grid = " + scale_name + "Grid,\n")
    text_file.write("   .t2Bitshift = " + t2bitshift +",\n")
    text_file.write("   .oneVoltOct = " + oneVoct_on + "};\n\n")

# print the function that actually fills the scaleGroup array that is referenced in the frequency generation code

text_file.write("void initializeScales() {\n")
for i in range(0, 16):
    scale_name = scales[i % len(scales)][0]
    text_file.write("   scaleGroup[" + str(i) + "] = " + scale_name + ";\n")
text_file.write("}\n")

text_file.close()

    



