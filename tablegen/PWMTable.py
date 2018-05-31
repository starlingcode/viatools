import numpy as np
import matplotlib.pyplot as plt

tableLength = 512 * (2**16)

storeLookup = np.zeros(64)
lookupTable = []

# iterate through 64 duty cycle values
# sample 64 points from the following equation
# for PWM in [0,1], phase in [0, tableLength]
# if phase < tableLength*PWM, phase = phase * (1/(2*PWM))
# else, phase = phase * (1/(2*(1 -PWM)))

PWMValues = np.linspace(0, 1, 64)
phaseValues = np.linspace(0, tableLength, 64)

for PWM in PWMValues:
    for phaseIndex, phase in np.ndenumerate(phaseValues):
        if phase < tableLength * PWM:
            coefficient = (.5/PWM)
            storeLookup[phaseIndex] = phase * coefficient
        else:
            coefficient = (.5/(1-PWM))
            storeLookup[phaseIndex] = phase * coefficient + tableLength * (1 - coefficient)
    lookupTable.append(storeLookup)
    plt.plot(PWMValues, storeLookup)
    storeLookup = np.zeros(64)

print(lookupTable)
plt.show()
