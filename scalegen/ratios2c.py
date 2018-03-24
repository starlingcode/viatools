# tool to generate scale code for the pll via

import csv

import math

from onevoltoctgenerator import makeScale1voct

from fullspangenerator import makeScaleFullSpan

scales = []

with open("ViaScales.csv", newline="\n") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if row[0] != "":
            scales.append([row[0], row[1], row[2], row[3]])

scale_holder = []
global_pitch_set = set([])

for i in scales:
    scale_name = i[0]

    is_1voct = i[1]

    is_pitch_class_set = i[2]

    is_pretiled = i[3]

    if is_1voct == "on":
        scaleParser = makeScale1voct(scale_name)
    else:
        scaleParser = makeScaleFullSpan(scale_name)

    full_scale = scaleParser[0]
    pitch_set = scaleParser[1]
    scale_tags = scaleParser[2]
    num_scales = scaleParser[3]
    
    global_pitch_set = global_pitch_set|pitch_set

    scale_holder.append([full_scale, scale_tags, num_scales])


text_file = open("ViaScales.txt", "w")
text_file.truncate()

#####################

for i in scales:
    scale_name = i[0]
    num_scales = scale_holder[scales.index(i)][2]
    text_file.write("const ScaleNote *" + scale_name + "Grid[" + str(num_scales) + "];\n")

text_file.write("\n\n")

for i in global_pitch_set:
    ratio_tag = i[0]
    integer_part = i[1]
    fractional_part = i[2]
    fundamental_divisor = i[3]
    text_file.write("#define " + ratio_tag + " {" + str(integer_part) + ", " + str(fractional_part) + ", " + str(fundamental_divisor) + "}\n")

text_file.write("\n\n\n")


for s in scales:

    full_scale = scale_holder[scales.index(s)][0]
    scale_tags = scale_holder[scales.index(s)][1]

    for i in range(0,num_scales):

        for j in range(0, 128):

            ratio_tag = str(full_scale[i][j][0])

            if j == 0:
                text_file.write("const ScaleNote " + scale_tags[i] + "[128] = {" + ratio_tag + ", ")
            elif j != 127:
                if j%12 != 0:
                    text_file.write(ratio_tag + ", ")
                else:
                    text_file.write(ratio_tag + ", \n")
            else:
                text_file.write(ratio_tag + "}; \n\n")

    text_file.write("\n\n")

text_file.write("\n\n\n")

for s in scales:

    scale_tags = scale_holder[scales.index(s)][1]
    num_scales = scale_holder[scales.index(s)][2]
    scale_name = s[0]

    for i in range(len(scale_tags)):

        if i == 0:
            text_file.write("const ScaleNote *" + scale_name + "Grid["+str(num_scales)+"] = {" + scale_tags[i] + ", ")
        elif i != (len(scale_tags) - 1):
            text_file.write(scale_tags[i] + ", ")
        else:
            text_file.write(scale_tags[i] + "}; \n\n")

text_file.write("\n\n\n")

for s in scales:
    scale_name = s[0]
    if s[1] == "on":
        oneVoct_on = str(1)
    else:
        oneVoct_on = str(0)
    num_scales = scale_holder[scales.index(s)][2]
    t2bitshift = str(int(math.log(4099//num_scales, 2)))
    text_file.write("Scale " + scale_name + " = {\n")
    text_file.write("   .grid = " + scale_name + "Grid,\n")
    text_file.write("   .t2Bitshift = " + t2bitshift +",\n")
    text_file.write("   .oneVoltOct = " + oneVoct_on + "};\n\n")

text_file.write("void initializeScales() {\n")
for s in scales:
    scale_name = s[0]
    scale_index = str(scales.index(s))
    text_file.write("   scaleGroup[" + scale_index + "] = " + scale_name + ";\n")
text_file.write("}\n")

text_file.close()

    



