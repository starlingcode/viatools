import numpy as np
from matplotlib import pyplot as plt

domain = np.linspace(0,2*np.pi,4097)

result = ((np.sin(domain)[:4096] + 1)/2 * 32767).astype(int)

print(result[0])
print(result[4095])

differences = np.roll(result, 1) - result

plt.plot(result)
plt.plot(differences)

packed_array = []

output_file = open("sine_write.txt", "w")

output_file.truncate()
output_file.write("static constexpr int big_sine[4095] = ")



for index, sample in enumerate(result):

    output_file.write(str(sample) + ", ")

output_file.write(str(result[0]) + "; ")

print(result)


plt.show()
