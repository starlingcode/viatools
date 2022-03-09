import sys
import json
import os

for root, dirs, files in os.walk('table_sample_defs'):
    for file in files:
        if not file.endswith('.py'):
            print(file)
            filename = file.replace('.csv', '')

            tables = []
            with open(root + '/' + file) as infile:
                for line in infile.readlines():
                    cells = line.split(',')
                    table = []
                    for cell in cells:  
                        try:
                            table.append(int(cell.replace('\n', '')))
                        except:
                            pass
                    while len(table) < 257:
                        last = table[-1]
                        table.append(last)                    
                    if len(table) > 257:
                        table = table[0:257]                    

                    tables.append(table)

            json_filename = filename + '.json'
            with open('table_sample_defs_json/' + json_filename, 'w') as jsonfile:
                json.dump(tables, jsonfile)
