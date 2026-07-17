"""
Contains three implementations of a bit reverse copy algorithm for the FFT.
"""

import numpy as np

"""
bit_reverse_lessefficient was my first attempt at doing a bit reverse
bit_reverse_standard is the same implementation but using bitwise operators. It's not a lot more efficient compared without them though, but an improvement is an improvement
bit_reverse is the implementation using numpy vectorisation so the rearrangement is a LOT more efficient :)

overall, all functions use O(N log N) time complexity and O(N) space complexity but each loop step is iteratively improved (and numpy uses compiled C so it will be a lot faster)
"""

def bit_reverse_lessefficient(arr):
    """ Bit reversal permutation on an array to make a more efficient FFT. Doesn't use bitwise operations or numpy vectorisation so it is less efficient """

    l = len(arr)
    permuted = [0] * l

    bitwidth = l.bit_length() - 1 # takes log base 2 of the length to get the bit width required

    for i in range(l):
        reversed = 0
        idx =i

        for _ in range(bitwidth):
            reversed = (reversed * 2) + (idx % 2) # shift the binary of reversed left once and replaces the new bit made at the end with the last bit of idx (given by whether it is odd or even)
            idx = idx // 2
            
        permuted[reversed] = arr[i]
    
    return permuted

def bit_reverse_standard(arr, convert_to_complex=False):
    """ Bit reversal permutation on an array to make a more efficient FFT. uses standard python lists """

    l = len(arr)
    permuted = [0] * l

    bitwidth = l.bit_length() - 1 # takes log base 2 of the length to get the bit width required

    for i in range(l):
        reversed = 0
        idx =i

        for _ in range(bitwidth):
            reversed = (reversed << 1) | (idx & 1) # more efficient because of use of bitwise operations
            idx = idx >> 1
            
        permuted[reversed] = complex(arr[i]) if convert_to_complex else arr[i]
    
    return permuted

def bit_reverse(arr, convert_to_complex=False):
    """ Bit reversal permutation to make a more efficient FFT using np vectors"""

    arr = np.asarray(arr)
    l = len(arr)
    bitwidth = l.bit_length() - 1  # takes log base 2 of the length to get the bit width required
    
    idx = np.arange(l)
    reversed_idx = np.zeros(l, dtype=int)
    
    for _ in range(bitwidth):
        reversed_idx = (reversed_idx << 1) | (idx & 1) # builds the order of reversed bitwise indices
        idx = idx >> 1
        
    if convert_to_complex:
        return arr[reversed_idx].astype(complex) # same as below but as complex numbers
    
    return arr[reversed_idx] # rearranges to match the order using numpy vectorisation in essentially one op