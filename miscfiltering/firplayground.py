


lines = [line.rstrip('\n') for line in open('downloadedfiltercoeffs.txt')]
lines = [x.strip('\t') for x in lines]
lines = [x.strip('y[n] = (') for x in lines]
lines = [x.strip('+ (') for x in lines]
lines = [x.replace('*', '') for x in lines]


parsed_file = []

for line in lines:
    if line != '':
        parsed_file.append(line.split())

print(parsed_file)

coeffs = []

for line in parsed_file:
    coeffs.append(int(65536*float(line[0])))

print(coeffs)

text_file = open('filtercoeffs.h', "w")

for i in range(0,11):
    text_file.write("#define a" + str(i) + ' ' + str(coeffs[10 - i]) + '\n')
for i in range(0,10):
    text_file.write("#define b" + str(i) + ' ' + str(coeffs[20 - i]) + '\n')
