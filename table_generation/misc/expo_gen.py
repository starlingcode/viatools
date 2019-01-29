
expo_table = []

for i in range(0, 4095):
    expo_scale = 2**(i/384.0)
    expo_scale = int(expo_scale * 2**16)
    expo_table.append(expo_scale)

audio_base_freq = 1/(2**5) * (expo_table[2048]/expo_table[0])/2**2

audio_lowest_freq = audio_base_freq * (50000/512)

target_freq = 16.35

audio_scaling_factor = target_freq/audio_lowest_freq

print("Audio scaling factor is: " + str(audio_scaling_factor * 65536))

drum_base_freq = (expo_table[1024]/expo_table[0])/(2**5) * (expo_table[2048]/expo_table[0])/2**6

drum_lowest_freq = drum_base_freq * (50000/512)

target_freq = 16.35

drum_scaling_factor = target_freq/drum_lowest_freq

print("Drum scaling factor is: " + str(drum_scaling_factor * 65536))

for i in range(0, 100):

    print(str(i) + ": " + str(expo_table[2048 - i]/expo_table[2048]))

#VCVRack CV1 offsets are -23 for 48khz, -70 for 44.1

# f = open("expo_table.txt", "w")
#
# for number in expo_table:
#     f.write((str(number) + ", "))
#
# f.close

