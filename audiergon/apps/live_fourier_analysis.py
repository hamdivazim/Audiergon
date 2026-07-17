"""
Local Fourier analysis live through microphone input
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from audiergon.fast_fourier_transform import iterative_fft

FS = 44100
BLOCKSIZE = 1024

plt.ion()
fig, ax = plt.subplots()
x = np.linspace(0, FS/2, BLOCKSIZE//2)
line, = ax.plot(x, np.zeros(BLOCKSIZE//2))
ax.set_ylim(0, 100)
ax.set_xlim(0, 20000)
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Amplitude")

try:
    with sd.InputStream(channels=1, samplerate=FS, blocksize=BLOCKSIZE) as stream:
        print("Use your microphone :)")
        
        while plt.fignum_exists(fig.number):
            indata, overflowed = stream.read(BLOCKSIZE)
            signal = indata[:, 0]
            
            fft_output = iterative_fft(signal)
            
            magnitudes = np.abs(fft_output[:BLOCKSIZE//2])
            
            line.set_ydata(magnitudes)
            
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            
except KeyboardInterrupt:
    exit()