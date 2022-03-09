import matplotlib.pyplot as plt

import numpy as np


def sigmoid_calc(x, derivative=False):
  return x*(1-x) if derivative else 1/(1+np.exp(-x))

expo_domain = np.linspace(0, 4, 4097)
log_domain = np.linspace(1, 64, 4097)
logistic_domain = np.linspace(-4, 4, 4097)
lin = np.int32(np.linspace(0, 65535, 4097))
expo = np.zeros(4097)
log = np.zeros(4097)
sigmoid = np.zeros(4097)

np.exp(expo_domain, expo)
np.log(log_domain, log)
sigmoid = sigmoid_calc(logistic_domain)

print(np.max(expo))
expo -= 1
expo *= (65535/np.max(expo))
expo = np.int32(expo)
print(np.min(expo))
print(np.max(expo))

log *= (65535/np.max(log))
log = np.int32(log)

sigmoid -= np.min(sigmoid)
sigmoid *= (65535/np.max(sigmoid))
sigmoid = np.int32(sigmoid)

fig = plt.figure(0)
plt.axis("off")

ax = fig.add_subplot(221)
ax.set_facecolor((0, 0, 0))
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
plt.plot(expo, color=(240/256, 200/256, 50/256))
plt.axis('off')

ax = fig.add_subplot(222)
ax.set_facecolor((0, 0, 0))
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
plt.plot(lin, color=(240/256, 200/256, 50/256))
plt.axis('off')

ax = fig.add_subplot(223)
ax.set_facecolor((0, 0, 0))
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
plt.plot(log, color=(240/256, 200/256, 50/256))
plt.axis('off')

ax = fig.add_subplot(224)
ax.set_facecolor((0, 0, 0))
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
plt.plot(sigmoid, color=(240/256, 200/256, 50/256))
plt.axis('off')

fig.savefig('tiled.svg', transparent=True, bbox_inches='tight')


fig = plt.figure(1)
plt.axis("off")
plt.plot(lin, color=(240/256, 200/256, 50/256))
plt.plot(expo, color=(240/256, 200/256, 50/256))
plt.plot(log, color=(240/256, 200/256, 50/256))
plt.plot(sigmoid, color=(240/256, 200/256, 50/256))
fig.savefig('overlay.svg', transparent=True, bbox_inches='tight')



file = open("output/adsr_slopes.txt", "w")

file.truncate()

file.write("static constexpr int32_t expoSlope[4097] = {")

for number in expo:

    file.write(str(number) + ", ")

file.write("\n\n\n\n")

file.write("static constexpr int32_t logSlope[4097] = {")

for number in log:

    file.write(str(number) + ", ")

file.write("\n\n\n\n")

file.write("static constexpr int32_t linSlope[4097] = {")

for number in lin:
    file.write(str(number) + ", ")

file.write("\n\n\n\n")

file.write("static constexpr int32_t sigmoidSlope[4097] = {")

for number in sigmoid:
    file.write(str(number) + ", ")

file.close()

plt.show()
