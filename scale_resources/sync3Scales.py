
ratios = []

for index in range(0, 8):
    ratio = 1/(8 - index)
    print(ratio)
    ratios.append(int(ratio * (2**32)))

for index in range(1, 9):
    ratios.append(int(index * (2**32)))

print(ratios)