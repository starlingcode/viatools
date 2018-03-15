import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, butter, filtfilt, argrelextrema, resample
from scipy.io import wavfile





sampleRate, sampleData = wavfile.read("piano16bit.wav")

signal = sampleData[:-20000]



# duration = 1.0
# fs = 400.0
# samples = int(fs*duration)
t = range(np.size(signal))


# signal = chirp(t, 20.0, t[-1], 100.0)
# signal *= (1.0 + 0.5 * np.in(2.0*np.pi*3.0*t))

analytic_signal = hilbert(signal)
amplitude_envelope = np.abs(analytic_signal)

amplitude_average = np.zeros(np.size(signal))

runningSum = 0.0

for i in range(0, 1024):
    runningSum = runningSum + amplitude_average[i]

for i in range(np.size(signal)):
    if i <= 1024:
        runningSum = runningSum + amplitude_envelope[i + 1024]
        amplitude_average[i] = runningSum/(i + 1024)
    elif i < np.size(signal) - 1024:
        runningSum = runningSum + amplitude_envelope[i + 1024] - amplitude_envelope[i - 1024]
        amplitude_average[i] = runningSum/2048
    else:
        runningSum = runningSum - amplitude_envelope[i - 1024]
        amplitude_average[i] = runningSum/(1024 + (np.size(signal)))


hilbert_maxima_indices = argrelextrema(np.abs(amplitude_average), np.greater)
hilbert_maxima_values = np.abs(amplitude_average[hilbert_maxima_indices])
hilbert_peaks = resample(hilbert_maxima_values, np.size(signal))

signal_maxima_indices = argrelextrema(np.abs(signal), np.greater)
signal_maxima_values = np.abs(signal[signal_maxima_indices])
signal_peaks = resample(signal_maxima_values, np.size(signal))
instantaneous_phase = np.unwrap(np.angle(analytic_signal))
instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * 400.0)

fig = plt.figure()
ax0 = fig.add_subplot(211)
ax0.plot(t, signal, label='signal')
ax0.plot(t, amplitude_envelope, label='envelope')
ax0.plot(t, amplitude_average, label='envelopeAverage')
ax0.plot(t, signal_peaks, label='localPeaks')
# ax0.plot(t, hilbert_peaks, label='hilbertPeaks')
#ax0.plot(np.linspace(0, np.size(amplitude_envelope_maxValues), np.size(amplitude_envelope_maxValues)), amplitude_envelope_maxValues, label='envelopeSmooth')
ax0.set_xlabel("time in seconds")
ax0.legend()
ax1 = fig.add_subplot(212)
ax1.plot(t[1:], instantaneous_frequency)
ax1.set_xlabel("time in seconds")
ax1.set_ylim(0.0, 120.0)
plt.show()

