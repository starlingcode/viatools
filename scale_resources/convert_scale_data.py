import os
import csv

for root, dirs, files in os.walk("scale_defs"):
    for file in files:
        with open("scale_defs/" + file, "r") as scale_read:
            reader = csv.reader(scale_read)
            for row in reader:
                if row[0] != "":
                    with open("translated_scales/" + file.rstrip(".csv") + "/" + row[0] + ".csv", "w") as scale_write:
                        writer = csv.writer(scale_write, delimiter=",")
                        scale = row[1:]
                        print(scale)
                        if scale:
                            try:
                                writer.writerow(row[1:].remove(""))
                            except ValueError:
                                writer.writerow(row[1:])
                            except csv.Error:
                                pass

