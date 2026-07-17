"""
Processes an audio file and uses FFT to manipulate frequency ranges.
Utilises a Hann window to smooth frame bondaries
"""

import wave
import cmath
import tempfile
from .fast_fourier_transform import iterative_fft, iterative_ifft

def generate_hann_window(frame_size):
    # premake Hann window to smooth frame boundaries (the clicks)
    hann_window = []
    for n in range(frame_size):
        hann_window.append(0.5 * (1.0 - cmath.cos(2.0 * cmath.pi * n / (frame_size - 1))).real)
    return hann_window

def apply_equalizer(transformed, frame_size, framerate, bass_gain, low_mid_gain, mid_gain, high_mid_gain, treble_gain):
    #filter by each of the 5 frequency ranges
    for k in range(frame_size):
        k_effective = k if k <= frame_size // 2 else frame_size - k
        frequency = k_effective * framerate / frame_size
        
        if frequency < 250: #bass (0-250 Hz)
            transformed[k] *= float(bass_gain)
        elif frequency < 1000: #low mid gain (250-1000 Hz)
            transformed[k] *= float(low_mid_gain)
        elif frequency < 4000: #mids (1000-4000 Hz)
            transformed[k] *= float(mid_gain)
        elif frequency < 8000: #high mids (4000-8000 Hz)
            transformed[k] *= float(high_mid_gain)
        else: #trebles >8000 Hz
            transformed[k] *= float(treble_gain)
    return transformed

def process_audio(audio_filepath, bass_gain, low_mid_gain, mid_gain, high_mid_gain, treble_gain, output=None):
    with wave.open(audio_filepath, 'rb') as wav_in:
        nchannels = wav_in.getnchannels()
        sampwidth = wav_in.getsampwidth()
        framerate = wav_in.getframerate()
        nframes = wav_in.getnframes()
        
        if nchannels != 1 or sampwidth != 2:
            raise ValueError("Audio must be formatted as 16 bit mono PCM WAV. Use `ffmpeg -i in.mp3 -acodec pcm_s16le -ac 1 -ar 44100 out.wav` to convert.")
            
        raw_data = wav_in.readframes(nframes)
        
    samples = []
    for i in range(0, len(raw_data), 2):
        sample = int.from_bytes(raw_data[i : i+2], byteorder='little', signed=True)
        samples.append(sample)
        
    frame_size = 1024  
    hop_size = frame_size // 2
    
    hann_window = generate_hann_window(frame_size)
    
    output_buffer = [0.0] * (len(samples) + frame_size) #accumulator buffer for overlapping frames OLA
    
    for i in range(0, len(samples), hop_size):
        frame = samples[i:i+frame_size]
        
        if len(frame) < frame_size:
            frame += [0] * (frame_size - len(frame))
            
        #apply hann window
        windowed_frame = []
        for f,w in zip(frame, hann_window):
            windowed_frame.append(f*w)
        
        #forward fast fourier
        transformed = iterative_fft(windowed_frame)
        
        transformed = apply_equalizer(
            transformed, frame_size, framerate, 
            bass_gain, low_mid_gain, mid_gain, high_mid_gain, treble_gain
        )
                
        #reconstruct -ifft
        new_frame = iterative_ifft(transformed)
        
        #readd to accumulator buffer
        for j in range(frame_size):
            output_buffer[i + j] += new_frame[j].real
            
    #repack to 16b integer + fix length
    output_samples = []
    for val in output_buffer[:len(samples)]:
        out_val = int(round(val))
        out_val = max(-32768, min(32767, out_val))
        output_samples.append(out_val)

    if output is None:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        output_path = temp_file.name
        temp_file.close()
    else:
        output_path = output
        
    with wave.open(output_path, 'wb') as wav_out:
        wav_out.setnchannels(1)
        wav_out.setsampwidth(2)
        wav_out.setframerate(framerate)
        for sample in output_samples:
            wav_out.writeframes(sample.to_bytes(2, byteorder='little', signed=True))
            
    return output_path