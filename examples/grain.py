'''
File name: grain.py
Author: Lukas Müller
Python Version: 3.6
'''

import numpy as np
from pyfsr import LFSR, NLFSR, FSRFunction

'''
Test Implementation of the Grain v0 cipher:
source: https: //cr.yp.to/streamciphers/grain/desc.pdf
'''

# 80 bit key
key = 0xB5EC3B0FC1A0F8B17A5B
# 64 bit IV
iv = 0xFAECFB0FAFA0FABA

# convert to binary list
key_bin = [int(x) for x in bin(key)[2:]]
iv_bin = [int(x) for x in bin(iv)[2:]]

# pad IV with ones as described in the paper
for i in range(len(iv_bin), 80):
    iv_bin.append(1)

# the nfsrs feedback function
gx = FSRFunction([
    16, 19, 27, 34, 42, 46, 51, 58, 64, 70, 79, "+", "+", "+", "+", "+", "+", "+", "+", "+", "+",
    16, 19, "*", "+", 42, 46, "*", "+", 64, 70, "*", "+", 19, 27, 34, "*", "*", "+", 46, 51, 58,
    "*", "*", "+", 16, 34, 51, 70, "*", "*", "*", "+", 19, 27, 42, 46, "*", "*", "*", "+", 16, 19,
    58, 64, "*", "*", "*", "+", 16, 19, 27, 34, 42, "*", "*", "*", "*", "+", 46, 51, 58, 64, 70,
    "*", "*", "*", "*", "+", 27, 34, 42, 46, 51, 58, "*", "*", "*", "*", "*", "+"
])

# init the nfsr with the key and feedback function
nfsr = NLFSR(initstate=key_bin, infunc=gx)

# the lfsrs feedback polynom
fx = [80, 67, 57, 42, 29, 18]

# init lfsr with the padded iv and the specified feedback polynom
lfsr = LFSR(poly=fx, initstate=iv_bin)

# the filter function
hx = FSRFunction([
    1, 4, "+", 0, 3, "*", "+", 2, 3, "*", "+", 3, 4, "*", "+", 0, 1, 2,
    "*", "*", "+", 0, 2, 3, "*", "*", "+", 0, 2, 4, "*", "*", "+", 1, 2,
    4, "*", "*", "+", 2, 3, 4, "*", "*", "+"
])

# key initialization phase
for i in range(0, 160):
    lfsr.shift()
    nfsr.shift()
    # for bi we'll choose 63, so bi+63 would result in (63+63) % 80 = 46
    outtaps = [lfsr.state[3], lfsr.state[25],
               lfsr.state[46], lfsr.state[64], nfsr.state[46]]
    filter_out = hx.solve(outtaps)
    # mask the output of the filter function with bi
    outbit = np.logical_xor(filter_out, nfsr.state[63])
    # feed it back to the fsrs
    lfsr.state[0] = np.logical_xor(outbit, lfsr.feedback_bit)
    nfsr.state[0] = np.logical_xor(
        outbit, np.logical_xor(lfsr.outbit, nfsr.feedback_bit))

# generate the actual sequence
length = 2000
sequence = np.ones(length) * -1
for i in range(0, 2000):
    lfsr.shift()
    nfsr.shift()
    nfsr.state[0] = np.logical_xor(lfsr.outbit, nfsr.state[0])
    # for bi we'll choose 63, so bi+63 would result in (63+63) % 80 = 46
    outtaps = [lfsr.state[3], lfsr.state[25],
               lfsr.state[46], lfsr.state[64], nfsr.state[46]]
    # mask the output of the filter function with bi
    sequence[i] = np.logical_xor(nfsr.state[63], hx.solve(outtaps))

print("".join(str(s) for s in sequence.astype(int)))
