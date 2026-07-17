"""
Audio Equalisation Module using FFT, Hann windowing and Overlap-Add

This library is part of `audiergon`, built by Hamd Waseem (https://github.com/hamdivazim/Audiergon)

Available Methods:
    - generate_hann_window
    - apply_equaliser
    - process_audio

Dependencies:
    - wave, cmath, tempfile
    - audiergon.fast_fourier_transform
"""
import wave
import cmath
import tempfile
from .fast_fourier_transform import iterative_fft, iterative_ifft

def generate_hann_window(frame_size):
    """
    Generates a Hann Window to smooth frame boundaries for a given frame size.

    :param frame_size: The size of each frame
    :type frame_size: int

    :returns: A list containing the Hann window
    :rtype: list
    """
    
    # premake Hann window to smooth frame boundaries (the clicks)
    hann_window = []
    for n in range(frame_size):
        hann_window.append(0.5 * (1.0 - cmath.cos(2.0 * cmath.pi * n / (frame_size - 1))).real)
    return hann_window

def apply_equaliser(transformed, frame_size, framerate, bass_gain, low_mid_gain, mid_gain, high_mid_gain, treble_gain):
    """
    Applies equaliser gains on a Frequency Domain sound array.

    :param transformed: The frequency-domain representation of the audio frame.
    :type transformed: list or numpy.ndarray
    :param frame_size: The total size/length of the frame (number of bins).
    :type frame_size: int

    :param framerate: The sampling rate of the audio in Hz.
    :type framerate: int or float

    :param bass_gain: Gain multiplier for the bass band (0 - 249 Hz).
    :type bass_gain: float or int
    :param low_mid_gain: Gain multiplier for the low-mid band (250 - 999 Hz).
    :type low_mid_gain: float or int
    :param mid_gain: Gain multiplier for the mid band (1000 - 3999 Hz).
    :type mid_gain: float or int
    :param high_mid_gain: Gain multiplier for the high-mid band (4000 - 7999 Hz).
    :type high_mid_gain: float or int
    :param treble_gain: Gain multiplier for the treble band (8000 Hz and above).
    :type treble_gain: float or int

    :return: The modified frequency-domain array with gains applied.
    :rtype: list or numpy.ndarray

    """

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
    """
    Processes a mono 16-bit PCM WAV audio file through an equaliser.

    :param audio_filepath: Path to the input WAV audio file.
    :type audio_filepath: str

    :param bass_gain: Gain multiplier for frequencies under 250 Hz.
    :type bass_gain: float or int
    :param low_mid_gain: Gain multiplier for frequencies from 250 to 999 Hz.
    :type low_mid_gain: float or int
    :param mid_gain: Gain multiplier for frequencies from 1000 to 3999 Hz.
    :type mid_gain: float or int
    :param high_mid_gain: Gain multiplier for frequencies from 4000 to 7999 Hz.
    :type high_mid_gain: float or int
    :param treble_gain: Gain multiplier for frequencies 8000 Hz and above.
    :type treble_gain: float or int

    :param output: Optional explicit output file path. If None, a temporary file is created.
    :type output: str, optional

    :return: The file path where the processed WAV audio was saved.
    :rtype: str

    :raises ValueError: If the input file is not 16-bit mono PCM WAV format.
    """

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
        
        transformed = apply_equaliser(
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