
expo_table = []

for i in range(0, 4096):
    expo_scale = 2 ** (i/384.0)
    expo_scale = int(expo_scale * 65536)
    expo_table.append(expo_scale)

print(expo_table[4095] * 4096 / 2**32)

f = open("expo_table.txt", "w")

for number in expo_table:
    f.write((str(number) + ", "))

f.close

