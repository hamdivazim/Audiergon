"""
My implementation of a fast fourier transform.


"""

import numpy as np
import cmath 
from bit_reverse import bit_reverse

def iterative_fft(arr):
    """
    An iterative Fast Fourier Transform implementation within Python.
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