import colorsys

huegroup1 = [0.0, 0.05, 0.1, 0.15]
huegroup2 = [0.25, 0.30, 0.35, 0.40]
huegroup3 = [0.5, 0.55, 0.6, 0.65]
huegroup4 = [0.75, 0.8, 0.85, 0.90]


redLevel = 4095.0
blueLevel = 3000.0
greenLevel = 4095.0

rgb_list = []

for hue in huegroup1:
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    rgb_list.append([int(rgb[0] * redLevel), int(rgb[1] * greenLevel), int(rgb[2] * blueLevel)])

for hue in huegroup2:
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    rgb_list.append([int(rgb[0] * redLevel), int(rgb[1] * greenLevel), int(rgb[2] * blueLevel)])

for hue in huegroup3:
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    rgb_list.append([int(rgb[0] * redLevel), int(rgb[1] * greenLevel), int(rgb[2] * blueLevel)])

for hue in huegroup4:
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    rgb_list.append([int(rgb[0] * redLevel), int(rgb[1] * greenLevel), int(rgb[2] * blueLevel)])



print(rgb_list)