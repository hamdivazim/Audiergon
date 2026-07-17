"""
An implementation of a Fast Fourier Transform, Inverse Fast Fourier Transform, and a frequency calculator for the FFT.

This library is part of `audiergon`, built by Hamd Waseem (https://github.com/hamdivazim/Audiergon)

Available Methods:
    - iterative_fft
    - iterative_ifft
    - iterative_fftfreq

Dependencies:
    - cmath
    - audiergon.bit_reverse
"""

import cmath 
from .bit_reverse import bit_reverse

def iterative_fft(arr):
    """
    An iterative Fast Fourier Transform implementation within Python.

    Computes the one-dimensional discrete Fourier Transform (DFT) of an array using the Cooley-Tukey algorithm.

    :param arr: The time-domain samples to be transformed.
    :type arr: list or numpy.ndarray

    :return: A list of complex numbers representing the frequency spectrum.
    :rtype: list

    :raises ValueError: If the length of the array is not a power of two.
    """

    l = len(arr)

    #cooley-tukey fft needs l to be a power of 2
    if ( l&(l-1) ) != 0: #eg with 8 (1000): 1000-0111 should give us 0 since it is a power of 2.
        raise ValueError("l of frame must be a power of 2. Got "+str(l))
    
    A = bit_reverse(arr, True) # fft uses complex numbers to track amplitude And phase

    stage_count = l.bit_length() - 1 # takes log base 2 of the array length

    for s in range(1, stage_count+1):
        m = 1 << s # sub problem size for the current stage
        m_2 = m >> 1 # distance between the elements to be combined (half of m)

        w_m = cmath.exp(-2j * cmath.pi / m) # calculate the base twiddle factor rotation by mapping out a circle on complex plane. -ve i (or j) corresponds to clockwise rotation

        for k in range(0, l, m):
            w = 1.0+0.0j # j is the imaginary constant. starts at 1, which is the right edge on the circle

            for j in range(m_2): # only need to loop thru half because of the mirrored bins

                t= (w) * A[k+j+m_2] # rotate the element (via twiddle factor) using odd index
                u = A[k+j] # take the matching element for even index

                A[k+j] = u + t # constructive
                A[k + j + m_2] = u - t # destructive

                w *= w_m #rotate for the next frequency step (multiplying complex numbers adds angles together)
    
    return A

def iterative_ifft(arr):
    """
    An iterative Inverse Fast Fourier Transform implementation within Python.

    Computes the inverse discrete Fourier Transform (DFT) to convert a frequency-domain array back into the time-domain, utilising the Cooley-Tukey algorithm.

    :param arr: The complex frequency-domain coefficients.
    :type arr: list or numpy.ndarray

    :return: An array of numbers scaled down by the sequence length.
    :rtype: numpy.ndarray

    :raises ValueError: If the length of the array is not a power of two.
    """

    l = len(arr)

    if ( l&(l-1) ) != 0:
        raise ValueError("l of frame must be a power of 2. Got "+str(l))
    
    A = bit_reverse(arr, True)

    stage_count = l.bit_length() - 1

    for s in range(1, stage_count+1):
        m = 1 << s
        m_2 = m >> 1

        w_m = cmath.exp(2j * cmath.pi / m) # uses Positive imaginary constant to represent rotation anticlockwise

        for k in range(0, l, m):
            w = 1.0+0.0j

            for j in range(m_2):

                t= (w) * A[k+j+m_2]
                u = A[k+j]

                A[k+j] = u + t
                A[k + j + m_2] = u - t

                w *= w_m
    
    return A / l # divided the array by length (fast because of numpy vectorisation from `bit_reverse`)

def iterative_fftfreq(l, d=1.0):
    """
    An iterative calculation of the frequencies for the FFT output.

    Generates the sample frequencies for each bin location based on the total sequence window length and spacing interval.

    :param l: Window length (number of bins).
    :type l: int

    :param d: Sample spacing/interval (inverse of the sampling rate), defaults to 1.0.
    :type d: float, optional

    :return: A list containing the calculated frequency values for each bin.
    :rtype: list
    
    :raises ValueError: If the length of the frame is not a power of two.
    """

    if (l & (l - 1)) != 0:
        raise ValueError("l of frame must be a power of 2. Got " + str(l))

    val = 1.0 / (l * d) #spacing between frequency bins on complex plane
    
    results = [0.0] * l
    
    m_2 = l >> 1 #midpoint

    for j in range(m_2):
        results[j] = j * val

    for j in range(m_2, l):
        results[j] = (j - l) * val

    return results