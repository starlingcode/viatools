
import csv

lines = [line.rstrip('\n') for line in open('tables.c')]
lines = [x.strip('\t') for x in lines]
lines = [x.strip('\t') for x in lines]
lines = [x.strip('//') for x in lines]
lines = [x.replace('};', '') for x in lines]
lines = [x.replace(',', ' ') for x in lines]
lines = [x.replace('=', '') for x in lines]
lines = [x.replace('{', ' ') for x in lines]

parsed_file = []

for line in lines:
    if line != '':
        parsed_file.append(line.split())

print(parsed_file)

families = []
family = []

for line in parsed_file:
    if line[0] == 'Family':
        families.append(family)
        family = []
        family.append(line[1])
    elif line[0] == '.attackFamily':
        family.append(line[1])
    elif line[0] == '.releaseFamily':
        family.append(line[1])

print(families)

with open('familytransfer.csv', 'w') as csvfile:
    tablewriter = csv.writer(csvfile, delimiter=',')
    for family in families:
        tablewriter.writerow(family)


