import csv

file_name = input("which file cap'n: ")

tables = []

with open(file_name + ".csv", "r") as input_file:
    read_file = csv.reader(input_file)
    for row in read_file:
        table = []
        for cell in row:
            table.append(cell)
        table.reverse()
        tables.append(table)

with open(file_name + "_reversed.csv", "w") as output_file:
    writer_bot = csv.writer(output_file)
    for table in tables:
        writer_bot.writerow(table)

print(tables)

