# Audiergon Local
A suite of audio-related tools built with Python and AWS to demonstrate the use of the Fourier Transform!

## Features

### Cooley-Tukey Fast Fourier Transform
An implementation of the Cooley-Tukey FFT in Python, in `fast_fourier_transform.py`. It contains the following three methods:
* `iterative_fft()` performs a forward FFT
* `iterative_ifft()` performs a backward FFT
* `iterative_fftfreq()` calculates the frequencies outputted by an FFT

### Local EQ Filter
A local Gradio client that uses the FFT to modify frequency bins in inputted audio files to analyse them.
* Requires the `gradio` library
* Uses `process.py` (Hann Window and Overlap-Add) for processing and `local_gradio.py` for the UI

### Fourier Analysis
A local analysis tool to visually graph the Frequency Domain and Time Domain of a sound file.
* Requires inputted audio files to be formatted as `.wav` files using a Mono PCM codec.
    * Use `ffmpeg -i in.mp3 -acodec pcm_s16le -ac 1 -ar 44100 out.wav` in a command line to convert
* Uses the `fourier_analysis.py` file

### Live Fourier Analysis
A local analysis tool that uses your microphone to graphically show the Frequency Domain of the ambient sound around you!
* Requires the `sounddevice` library
* Uses the `live_fourier_analysis.py` file

## Upcoming Features

### Audio Compression Tool
Utilises the concept that high frequency sound gets masked when lower frequencies are louder.

### AWS Cloud Implementation and UI
A streamlined version of the FFT designed to process audio as fast as possible entirely within the cloud.
* Planning to use S3 Event Triggers combined with Lambda and a simple Vercel/Next.js frontend.

## Devlog
Check out [Audiergon Devlog Part 1](https://youtu.be/Kwgaz00gUXw) on YouTube for a detailed run-through of the theory behind the Fourier Transform!

<kbd>
<a href="https://youtu.be/Kwgaz00gUXw"><img src="https://img.youtube.com/vi/Kwgaz00gUXw/maxresdefault.jpg" alt="Watch the video!"></a>
</kbd>

## License
Audiergon is licensed under the [MIT License](LICENSE)