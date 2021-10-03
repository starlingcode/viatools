import os
import json
import csv

for root, dirs, files in os.walk('pattern_resources'):
    print(files)
    for file in [_file for _file in files if 'csv' in _file]:
        json_out = []
        with open(root + '/' + file) as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row in reader:
                json_out.append(row)
        new_file = file.replace('.csv', '.json')  
        with open(root + '/' + new_file, 'w') as out_file:
            json.dump(json_out, out_file)         

