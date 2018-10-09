import csv

def get_table_lengths(family, familybank, slopefamilies, tables):

    familydef = ''
    example_slope = ''
    num_tables = 0
    num_samples = 0

    for idx in familybank:
        if idx[0] == family:
            familydef = idx[1]
    for jdx in slopefamilies:
        if jdx[0] == familydef:
            example_slope = jdx[1]
            num_tables = len(jdx) - 1
    for udx in tables:
        if udx[0] == example_slope:
            num_samples = len(udx) - 2

    return [num_tables, num_samples]

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

audio_families = []
env_families = []
seq_families = []

with open('meta_tables.csv', 'r') as csvfile:
    tablereader = csv.reader(csvfile, delimiter=',')
    for row in tablereader:
        if row[0] == "audio":
            audio_families.append([row[0], row[1], row[2]])
        elif row[0] == "env":
            env_families.append([row[0], row[1], row[2]])
        elif row[0] == "seq":
            seq_families.append([row[0], row[1], row[2]])

family_array = []
family_array.append(audio_families)
family_array.append(env_families)
family_array.append(seq_families)

families_used = set([])

for family in family_array:
    for i in family:
        families_used.add(i[2])

# print(families_used)

slopes_used = set([])

family_bank = []

with open('table_definitions.csv', 'r') as csvfile:
    tablereader = csv.reader(csvfile, delimiter=',')
    for row in tablereader:
        if row[0] in families_used:
            family_bank.append([row[0], row[1], row[2], row[3]])
            slopes_used.add(row[1])
            slopes_used.add(row[2])

# print(slopes_used)

slopefamilies = []
slopefamily = []
tables = []
table = []

for slope in slopes_used:
    with open('table_sample_defs/' + slope + '.csv', 'r') as csvfile:
        slopefamily = [slope]
        slopereader = csv.reader(csvfile, delimiter=',')
        rowcounter = 0
        for row in slopereader:
            if row[0] != '':
                slopefamily.append(slope+str(rowcounter))
                table.append(slope+str(rowcounter))
                j = 0
                while j < len(row) and row[j] != '':
                    if is_number(row[j]):
                        table.append(row[j])
                    j += 1
                    #print(row[j])
                tables.append(table)
                table = []
            rowcounter += 1

        slopefamilies.append(slopefamily)


print(slopefamilies)
print(tables)

# with open('rowdefinitions.csv', 'r') as csvfile:
#             tablereader = csv.reader(csvfile, delimiter=',')
#             for row in tablereader:
#                 if row[0] in slopes_used:
#                     for i in row:
#                         if str(i) != '':
#                             slopefamily.append(i)
#                             if row.index(i) != 0:
#                                 tables_used.add(i)
#                     slopefamilies.append(slopefamily)
#                     slopefamily = []
#
# print(slopefamilies)
#
# tables = []
# table = []
#
# with open('tabledefinitions.csv', 'r') as csvfile:
#             tablereader = csv.reader(csvfile, delimiter=',')
#             for row in tablereader:
#                 if row[0] != "" and row[0] in tables_used:
#                     for i in row:
#                         if str(i) != '':
#                             table.append(i)
#                     tables.append(table)
#                     table = []



#####################

text_file = open("tables.h", "w")
text_file.truncate()

header_stub = open('via_rev5_classic_header_stub.h', 'r')

for line in header_stub:
    text_file.write(line)

header_stub.close()

for table in tables:
    table_length = len(table) - 1
    text_file.write('static const uint16_t ' + table[0] + '[' + str(table_length) + '] = {\n\t')
    for i in table[1:(table_length)]:
        if (table.index(i) % 8) == 0:
            text_file.write(i + ',\n\t')
        else:
            text_file.write(i + ', ')
    text_file.write(table[table_length] +'};\n\n\n')


for table in slopefamilies:
    table_length = len(table) - 1
    text_file.write('static const uint16_t *' + table[0] + '[' + str(table_length) + '] = {\n\t')
    for i in table[1:(table_length)]:
        if (table.index(i) % 8) == 0:
            text_file.write(i + ',\n\t')
        else:
            text_file.write(i + ', ')
    text_file.write(table[table_length] + '};\n\n\n')

text_file.write('#endif')

text_file.close()


text_file = open("tables.c", "w")
text_file.truncate()

text_file.write('#include "tables.h"\n')
text_file.write('#include "main.h"\n')
text_file.write('#include "stm32f3xx_hal.h"\n')
text_file.write('#include "stm32f3xx.h"\n')
text_file.write('#include "stm32f3xx_it.h"\n')
text_file.write('#include "modes.h"\n')
text_file.write('\n\n\n')

for family in family_bank:
    text_file.write('const Family ' + family[0] + ' = {\n')
    text_file.write('\t.attackFamily = ' + family[1] + ',\n')
    text_file.write('\t.releaseFamily = ' + family[2] + ',\n')
    text_file.write('\t.tableLength = ' + str(get_table_lengths(family[0], family_bank, slopefamilies, tables)[1]) + ',\n')
    text_file.write('\t.familySize = ' + str(get_table_lengths(family[0], family_bank, slopefamilies, tables)[0]) + '};\n\n\n')

text_file.write('\n\n')

text_file.write('void fillFamilyArray(void) {\n\n')

for speed in family_array:
    for i in speed:
        text_file.write('\tfamilyArray[' + i[0] + '][' + i[1] + '] = &' + i[2] + ';\n')

text_file.write('\n\tcurrentFamily = *familyArray[0][0];\n')
text_file.write('\tswitchFamily();\n\n}')


text_file.close()