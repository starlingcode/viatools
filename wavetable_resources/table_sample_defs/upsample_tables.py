import numpy as np
from scipy import interpolate

import os
import csv

filenames = []

for fn in os.listdir('.'):
     if fn.endswith(".csv"):
         filenames.append(fn)

for filename in filenames:

    print(filename)
    samplearrays = []
    with open(filename, 'r') as samplefile:
        samplereader = csv.reader(samplefile, delimiter = ',')
        for row in samplereader:
            samplearrays.append(np.array(row))

    if samplearrays[0].size != 257:

        #print(samplearrays)

        upsampled_arrays = []

        for samplearray in samplearrays:
            basis = np.arange(0, samplearray.size, 1)
            #print(basis)
            samples = samplearray
            #print(samples)
            spline = interpolate.splrep(basis, samples)
            upsampled_basis = np.arange(0, samplearray.size - 1, (samplearray.size - 1)/256)
            upsampled_basis = np.append(upsampled_basis, samplearray.size - 1)
            #print(upsampled_basis)
            upsampled_spline = interpolate.splev(upsampled_basis, spline)
            upsampled_spline = np.clip(upsampled_spline, 0, 32767)
            print(upsampled_spline.size)
            upsampled_arrays.append(upsampled_spline.astype(int))

        with open(filename, 'w') as writefile:
            samplewriter = csv.writer(writefile, delimiter = ',')
            for row in upsampled_arrays:
                samplewriter.writerow(row)



