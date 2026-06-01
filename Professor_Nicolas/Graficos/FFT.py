import numpy as np
import matplotlib.pyplot as plt

fs = 1000  # Sampling frequency
t = np.arange(0, 1, 1/fs)  # Time vector of 1 second
f1 = 50  # Frequency of the first sine wave
f2 = 120  # Frequency of the second sine wave
signal = np.sin(2 * np.pi * f1 * t) + 0.5* np.sin(2 * np.pi * f2 * t)  # Composite signal
fft_result = np.fft.fft(signal)  # Compute the FFT
frequencies = np.fft.fftfreq(len(signal), 1/fs)  #              
# Plotting the FFT result
plt.figure(figsize=(10, 6))
plt.plot(frequencies[:len(frequencies)//2], np.abs(fft_result)[:len(fft_result)//2]) 
plt.xlim(25,200)  # Limit x-axis to 25 to 200 Hz
plt.title('FFT of the Composite Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid()
plt.show()  