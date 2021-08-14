import os
import json
for root, dirs, files in os.walk('sync3scales'):
    print(files)
    for file in files:
            with open('sync3scales/' + file) as jsonfile:
                    print(file)
                    data = json.load(jsonfile)
                    print(data)
            if 'method' in data:
                    with open('sync3scales/' + file, 'w') as jsonfile:
                            data['method'] = data['method'].replace('doubled','fill')
                            data['method'] = data['method'].replace('full set','fill')
                            print(data['method'])
                            json.dump(data, jsonfile)
