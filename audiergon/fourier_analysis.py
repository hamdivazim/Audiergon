"""
Shows the Frequency Domain and Time Domain for an input audio file
"""

import numpy as np
import matplotlib.pyplot as plt
import wave
import fast_fourier_transform
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s'
)

file_path = input("Enter the path to your mono PCM WAV file: ").strip()

logging.info("Reading audio file...")

with wave.open(file_path, 'rb') as wav_file:
    if wav_file.getnchannels() != 1:
        raise ValueError("Audio must be formatted as 16 bit mono PCM WAV. Use `ffmpeg -i in.mp3 -acodec pcm_s16le -ac 1 -ar 44100 out.wav` to convert.")
        
    sampling_rate = wav_file.getframerate()
    total_frames = wav_file.getnframes()
    
    raw_frames = wav_file.readframes(total_frames)

signal = np.frombuffer(raw_frames, dtype=np.int16).astype(float)

#need to trim the signal to a power of 2 for the FFT to work
original_len = len(signal)
p2_len = 1 << (original_len.bit_length() - 1) #largest power of 2 fitting inside the orig len

if p2_len > original_len:
    p2_len >>= 1

signal = signal[:p2_len]

duration = len(signal) / sampling_rate
t = np.linspace(0, duration, len(signal), endpoint=False)

logging.info("Performing FFT...")

fft_output = np.array(fast_fourier_transform.iterative_fft(signal))
frequencies = fast_fourier_transform.iterative_fftfreq(len(t), 1/sampling_rate)

positive_frequencies = frequencies[:len(frequencies)//2]
amplitudes = np.abs(fft_output)[:len(fft_output)//2] * (2.0 / len(t))

logging.info("Reconstructing with IFFT...")

reconstructed_output = np.array(fast_fourier_transform.iterative_ifft(fft_output))

logging.info("Plotting...")

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)

plt.plot(positive_frequencies, amplitudes, color='#e74c3c', linewidth=1, label="FFT Amplitude")
plt.fill_between(positive_frequencies, amplitudes, color='#e74c3c', alpha=0.15)

plt.title("Frequency Spectrum (FFT)", fontsize=12, fontweight='bold', pad=10)
plt.xlabel("Frequency (Hz)", fontsize=10)
plt.ylabel("Magnitude", fontsize=10)

plt.xlim(0, min(8000, sampling_rate // 2)) 
plt.ylim(bottom=0)

plt.grid(True, linestyle='--', alpha=0.6)

plt.subplot(1, 2, 2)
zoom_samples = min(500, len(signal)) 

plt.plot(t[:zoom_samples], signal[:zoom_samples], label="Original Signal", color='#2980b9', linewidth=1.5)
plt.plot(t[:zoom_samples], reconstructed_output.real[:zoom_samples], label="Reconstructed (IFFT)", linestyle='--', color='#27ae60', linewidth=1.5)

plt.title("Time Domain Waveform (Zoomed)", fontsize=12, fontweight='bold', pad=10)
plt.xlabel("Time (seconds)", fontsize=10)
plt.ylabel("Amplitude", fontsize=10)

plt.legend(frameon=True, facecolor='white', edgecolor='none')
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()