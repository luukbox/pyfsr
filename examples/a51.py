'''
    File name: a51.py
    Author: Lukas Müller
    Python Version: 3.6
'''

import numpy as np
from pyfsr import LFSR

'''
Test Implementation of the A5/1 stream cipher used in GSM

'''

# 64 bit key
key = 0xFAECFB0FAFA0FABA

# convert the key to binary array
key_bin = [int(x) for x in bin(key)[2:]]

r1 = LFSR(poly=[19, 18, 17, 14], initstate=key_bin[:19], initcycles=2**7)
r1.print_info()
r2 = LFSR(poly=[23, 22, 21, 8], initstate=key_bin[19:19+23], initcycles=2**7)
r2.print_info()
r3 = LFSR(poly=[22, 21], initstate=key_bin[19+23:], initcycles=2**7)
r3.print_info()

seq_len = 2**7
sequence = np.ones(seq_len) * -1

for i in range(seq_len):
    '''advance the lfsr with the most popular clocking bit values
    eg. b1, b2 = 0, b3 = 1 => advance b1 & b2
    eg. b1, b2, b3 = 0 => advance b1, b2, b3 
    append xor result of the outbits'''
    (b1, b2, b3) = (r1.state[8], r2.state[10], r3.state[10])
    vote = np.argmax(np.bincount([b1, b2, b3]))
    if(b1 == vote):
        r1.shift()
    if(b2 == vote):
        r2.shift()
    if(b3 == vote):
        r3.shift()
    output_bit = np.logical_xor(
        np.logical_xor(r1.outbit, r2.outbit),
        r3.outbit) * 1
    sequence[i] = output_bit

print(sequence.astype(int))

r1.print_info()
r2.print_info()
r3.print_info()
