
chromatic = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
major = [0, 0, 2, 2, 4, 5, 5, 7, 7, 9, 9, 11]
minor = [0, 0, 2, 2, 3, 5, 5, 7, 7, 8, 8, 10]
spooky = [0, 1, 1, 4, 4, 5, 5, 7, 7, 10, 10, 10]

chromatic_out = []
major_out = []
minor_out = []
spooky_out = []


for index in range(0, 127):

    index_note = (index - 4) % 12
    index_octave = int(((index - 4) / 12)) * 12

    if index - 4 < 0:
        index_note = 0

    chromatic_out.append(index_octave + chromatic[index_note])
    major_out.append(index_octave + major[index_note])
    minor_out.append(index_octave + minor[index_note])
    spooky_out.append(index_octave + spooky[index_note])

print(chromatic_out)
print(major_out)
print(minor_out)
print(spooky_out)
