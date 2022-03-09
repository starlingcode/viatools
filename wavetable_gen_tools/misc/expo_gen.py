import numpy as np

target_sample_rate = 48000

expo_table = []

for i in range(0, 4095):
    expo_scale = 2**(i/384.0)
    expo_scale = int(expo_scale * 2**16)
    expo_table.append(expo_scale)

expo_table_stretch = []

for i in range(0, 4095):
    expo_scale = 2**(i/300.0)
    expo_scale = int(expo_scale * 2**16)
    expo_table_stretch.append(expo_scale)

offset = expo_table[2048] - expo_table_stretch[2048]

expo_table_work = np.asarray(expo_table_stretch)

expo_table_work += offset

print(expo_table[2048])
print(expo_table_stretch[2048])
print(expo_table_work[2048])

print("{", end="")

for number in expo_table_stretch[:-1]:
    print(number, end=", ")

print(expo_table_stretch[-1], end="}")




# audio_base_freq = 1/(2**5) * (expo_table[2048]/expo_table[0])/2**2
#
# audio_lowest_freq = audio_base_freq * (target_sample_rate/512)
#
# target_freq = 16.352
#
# audio_scaling_factor = target_freq/audio_lowest_freq
#
# print("Audio scaling factor is: " + str(audio_scaling_factor * 65536))
#
# drum_base_freq = (expo_table[1024]/expo_table[0])/(2**5) * (expo_table[2048]/expo_table[0])/2**5 * 1.5
#
# drum_lowest_freq = drum_base_freq * (target_sample_rate/512)
#
# target_freq = 32.703
#
# drum_scaling_factor = target_freq/drum_lowest_freq
#
# print("Drum scaling factor is: " + str(drum_scaling_factor * 65536))
#
# for i in range(0, 100):
#
#     print(str(i) + ": " + str(expo_table[2048 - i]/expo_table[2048]))

#VCVRack CV1 offsets are -23 for 48khz, -70 for 44.1

# f = open("expo_table.txt", "w")
#
# for number in expo_table:
#     f.write((str(number) + ", "))
#
# f.close

