
import csv

lines = [line.rstrip('\n') for line in open('tables.h')]
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

table = []
tables = []
collect_values = 0

for line in parsed_file:
    if line[0] == 'static':
        tables.append(table)
        table = []
        table.append(line[3])
        for i in line[4:]:
            table.append(i)
        collect_values = 1
    else:
        for i in line:
            table.append(i)

print(tables)

with open('tabletransfer.csv', 'w') as csvfile:
    tablewriter = csv.writer(csvfile, delimiter=',')
    for table in tables:
        tablewriter.writerow(table)


