import csv

inverted_tables = []

with open("newest_bounce_attack.csv", "r") as input_file:
    read_input = csv.reader(input_file)
    for row in read_input:
        inverted_table = []
        for sample in row:
            inverted_table.append(32767 - int(sample))
        inverted_tables.append(inverted_table)

with open("newest_bounce_attack.csv", "w") as output_file:
    write_output = csv.writer(output_file)
    for table in inverted_tables:
        write_output.writerow(table)
