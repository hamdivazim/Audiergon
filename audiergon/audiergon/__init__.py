"""
Audiergon: A suite of DSP tools to perform Fourier analysis

Built by Hamd Waseem - https://github.com/hamdivazim

Available methods:
    - bit_reverse
    - iterative_fft
    - iterative_ifft
    - iterative_fftfreq
    - process_audio
    - generate_hann_window
    - apply_equaliser
"""

from .bit_reverse import bit_reverse
from .fast_fourier_transform import iterative_fft, iterative_ifft, iterative_fftfreq
from .process import process_audio, generate_hann_window, apply_equaliser

__all__ = [
    "bit_reverse",
    "iterative_fft",
    "iterative_ifft",
    "iterative_fftfreq",
    "process_audio",
    "generate_hann_window",
    "apply_equaliser",
]

__version__ = "0.1.2"
__author__ = "Hamd Waseem"