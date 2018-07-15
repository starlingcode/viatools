import csv

table_defs = {}

with open("tabledefinitions.csv", 'r') as tablesheet:
    table_reader = csv.reader(tablesheet, delimiter = ',')
    for row in table_reader:
        if row[0] != '':
            table_defs[row[0]] = []
            j = 1
            while j < len(row) and row[j] != '':
                table_defs[row[0]].append(row[j])
                j += 1

row_defs = {}

with open("rowdefinitions.csv", 'r') as rowsheet:
    row_reader = csv.reader(rowsheet, delimiter = ',')
    for row in row_reader:
        if row[0] != '':
            row_defs[row[0]] = []
            j = 1
            while j < len(row) and row[j] != '':
                row_defs[row[0]].append(row[j])
                j += 1

for family in row_defs:
    with open(family + ".csv", 'w') as writefile:
        row_writer = csv.writer(writefile, delimiter=',')
        for row in row_defs[family]:
            row_writer.writerow(table_defs[row])


