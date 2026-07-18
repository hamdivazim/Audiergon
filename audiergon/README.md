
<div align="center">
  <img src="https://raw.githubusercontent.com/hamdivazim/Audiergon/main/logo.png" width="80%">

  <h1>Audiergon</h1>

  <p>A Python Digital Signal Processing (DSP) processor powered by a custom Cooley-Tukey Fast Fourier Transform implementation.</p>

  <h5> 
    <a href="https://github.com/hamdivazim/Audiergon">💻 GitHub Repo</a> | 
    <a href="https://pypi.org/project/audiergon/">🐍 PyPI Page</a> | 
    <a href="https://audiergon.readthedocs.io/en/latest/">📝 Docs</a>
  </h5>
</div>

## Key Features

* **Cooley-Tukey FFT**
    * Pure Python iterative implementations of 1D Forward and Inverse Fast Fourier Transforms.
* **Optimised Bit Reversal Permutations**
    * Fast bit-reversal indexing using native compiled C-speed NumPy indexing.
* **Overlap-Add Audio EQ Pipeline**
    * Complete pipeline for applying Hann windowing, processing frames through an equaliser, and rebuilding raw 16-bit PCM `.wav` streams without clicking or imaginary artifacts.

## Installation

Install the library using `pip`:

```bash
pip install audiergon
```

### Dependencies

* `numpy`

## Quick Start & API Examples

### 1 - Basic FFT & Frequency Analysis

Compute the Fourier Transform of a simple signal array and generate its matching frequency bins.

```python
from audiergon import iterative_fft, iterative_fftfreq

# Input array must have a length that is a power of 2
signal = [1.0, 0.5, -0.2, 0.1, 0.8, -0.4, 0.3, -0.1]
sampling_interval = 1.0 / 44100  # 44.1 kHz Sample Rate

# 1. Perform Forward FFT
frequency_coefficients = iterative_fft(signal)

# 2. Compute matching frequencies for the spectrum bins
frequencies = iterative_fftfreq(len(signal), d=sampling_interval)

print("Frequency spectrum coefficients:", frequency_coefficients)
print("Calculated bin frequencies (Hz):", frequencies)
```

### 2 - Equalising an Audio File

Process an audio track using the built-in Overlap-Add (OLA) processing pipeline.

```python
from audiergon import process_audio

# Modify the frequency bands using multipliers
output_path = process_audio(
    audio_filepath="in.wav",
    bass_gain=1.5,
    low_mid_gain=1.2,
    mid_gain=1.0,
    high_mid_gain=0.8,
    treble_gain=0.5,
    output="out.wav"
)
```

The `process_audio` pipeline requires 16-bit Mono PCM WAV files. You can  convert standard formats using `ffmpeg`:
```bash
ffmpeg -i in.mp3 -acodec pcm_s16le -ac 1 -ar 44100 out.wav
```

## API Overview

### `audiergon.fast_fourier_transform`

* `iterative_fft(arr)`
    * Computes the 1D Discrete Fourier Transform (DFT).
    * *Input:* `list` or `numpy.ndarray` (length must be a power of 2).
    * *Returns:* `list` of complex numbers tracking amplitude and phase.

* `iterative_ifft(arr)`
    * Computes the Inverse DFT converting frequencies back to the time domain.
    * *Returns:* `numpy.ndarray` scaled by the sequence length.

* `iterative_fftfreq(l, d=1.0)`
    * Generates frequency values for each bin location.

### `audiergon.process`

* `process_audio(audio_filepath, bass_gain, low_mid_gain, mid_gain, high_mid_gain, treble_gain, output=None)`
    * Applies windowed equalisation filters over an absolute file path.
* `generate_hann_window(frame_size)`
    * Generates a list containing real Hann coefficients to smooth frame boundary edges.
* `apply_equaliser(transformed, frame_size, framerate, ...)`
    * Sirectly apply scale gains on an existing complex frequency domain segment.

### `audiergon.bit_reverse`

* `bit_reverse(arr, convert_to_complex=False)`
    * Applies bit-reversal array permutations optimized with high-performance NumPy vector operations.

## License

Audiergon is open-source software licensed under the [MIT License](https://github.com/hamdivazim/Audiergon/raw/main/LICENSE).