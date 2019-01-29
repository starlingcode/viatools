
#define SH_MODE button1Mode
#define TABLE button2Mode
#define FREQ_MODE button3Mode
#define TRIG_MODE button4Mode
#define LOOP_MODE button6Mode
#define DRUM_AUX_MODE aux1Mode
#define LOGIC_A_MODE aux2Mode
#define DRUM_MODE aux3Mode
#define DAC_3_MODE aux4Mode

# button1Mode = 0
# button2Mode = 0
# button3Mode = 0
# button4Mode = 0
# button5Mode = 0
# button6Mode = 0
# aux1Mode = 2
# aux2Mode = 0
# aux3Mode = 0
# aux4Mode = 0

button1Mode = 2
button2Mode = 4
button3Mode = 0
button4Mode = 4
button5Mode = 0
button6Mode = 1
aux1Mode = 0
aux2Mode = 1
aux3Mode = 0
aux4Mode = 0

test = 0
test |= button1Mode
test |= button2Mode << 3
test |= button3Mode << 6
test |= button4Mode << 9
test |= button5Mode << 12
test |= button6Mode << 15
test |= aux1Mode << 18
test |= aux2Mode << 21
test |= aux3Mode << 24
test |= aux4Mode << 27

print(bin(test))
print(hex(test))
print(test)