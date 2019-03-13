'''
    File name: a51.py
    Author: Lukas Müller
    Python Version: 3.6
'''

import numpy as np
from pyfsr import LFSR, FSRFunction

'''
Test Implementation of the A5/1 stream cipher used in GSM

'''

# 64 bit key
key = 0xFAECFB0FAFA0FABA

# convert the key to binary array
key_bin = [int(x) for x in bin(key)[2:]]

r1 = LFSR(poly=[19, 18, 17, 14], initstate=key_bin[:19])
r2 = LFSR(poly=[23, 22, 21, 8], initstate=key_bin[19:19+23])
r3 = LFSR(poly=[22, 21], initstate=key_bin[19+23:])

seq_len = 2**7
sequence = np.ones(seq_len) * -1

outfunc = FSRFunction([0, 1, 2, "+", "+"])

for i in range(seq_len):
    '''advance the lfsrs with the most popular clocking bit values
    eg. b1, b2 = 0, b3 = 1 => advance r1 & r2
    eg. b1, b2, b3 = 0 => advance r1, r2, r3 
    then xor the outbits of all lfsrs'''
    (b1, b2, b3) = (r1.state[8], r2.state[10], r3.state[10])
    vote = np.argmax(np.bincount([b1, b2, b3]))
    if b1 == vote:
        r1.shift()
    if b2 == vote:
        r2.shift()
    if b3 == vote:
        r3.shift()
    output_bit = outfunc.solve([r1.outbit, r2.outbit, r3.outbit])
    # could also be written as:
    # output_bit = np.logical_xor(np.logical_xor(r1.outbit, r2.outbit), r3.outbit)
    sequence[i] = output_bit

print(sequence.astype(int))
