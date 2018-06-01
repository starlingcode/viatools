import numpy as np
import matplotlib.pyplot as plt

tableLength = (512 * (2**16)) - 1

storeLookup = np.zeros(65)
lookupTable = []

# iterate through 64 duty cycle values
# sample 64 points from the following equation
# for PWM in [0,1], phase in [0, tableLength]
# if phase < tableLength*PWM, phase = phase * (1/(2*PWM))
# else, phase = phase * (1/(2*(1 -PWM)))

PWMValues = np.linspace(0.2, .8, 33)
phaseValues = np.linspace(0, tableLength, 65)

for PWM in PWMValues:
    for phaseIndex, phase in np.ndenumerate(phaseValues):
        if phase < tableLength * PWM:
            coefficient = (.5/PWM)
            storeLookup[phaseIndex] = int(phase * coefficient)
        else:
            coefficient = (.5/(1-PWM))
            storeLookup[phaseIndex] = int(phase * coefficient + tableLength * (1 - coefficient))
    lookupTable.append(storeLookup)
    plt.plot(phaseValues, storeLookup)
    storeLookup = np.zeros(65)

############

text_file = open("pwm_tables.h", "w")
text_file.truncate()

text_file.write('#ifndef PWM_TABLES"\n')
text_file.write('#define PWM_TABLES"\n')

text_file.write('#include "stm33f3xx_hal.h"\n')
text_file.write('#include "stm33f3xx.h"\n')
text_file.write('#include "stm33f3xx_it.h"\n')
text_file.write('#include "dsp.h"\n')
text_file.write("\n\n\n")

tableIndex = 0
while tableIndex < 33:
    text_file.write("#define phaseModPWM_" + str(tableIndex) + " {" + str(int(lookupTable[tableIndex][0])))
    sampleIndex = 1
    while sampleIndex < 65:
        text_file.write(", " + str(int(lookupTable[tableIndex][sampleIndex])))
        sampleIndex += 1
    text_file.write("}\n\n")
    tableIndex += 1

text_file.write("q31_t phaseModPWMTables[64][64] = {phaseModPWM_0")
tableIndex = 1
while tableIndex < 33:
    text_file.write(", phaseModPWM_" + str(tableIndex))
    tableIndex += 1;
text_file.write("};\n\n")

text_file.write('#endif\n')



text_file.close()

print(lookupTable)
plt.show()
