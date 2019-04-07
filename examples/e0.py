'''
File name: e0.py
Author: Lukas Müller
Python Version: 3.6
'''

import numpy as np
from pyfsr import LFSR

'''
Test Implementation of the E0 cipher:
source: https://www.esat.kuleuven.be/cosic/publications/article-22.pdf
'''


class FSM():
    def __init__(self):
        self.ct_1 = [1, 0]
        self.ct = [1, 0]
        self.ct1 = [1, 0]

    def __T2(self):
        as_bin = [int(b) for b in bin(self.ct_1)[2:]]
        if len(as_bin) == 1:
            as_bin.append(0)
        return [as_bin[1], np.logical_xor(as_bin[0], as_bin[1])]

    def blend(self, x1, x2, x3, x4):
        # calc int from bit arr
        self.ct = self.ct[0]+2*self.ct[1]
        yt = x1 + x2 + x3 + x4
        st1 = int((yt + self.ct) / 2)
        self.ct_1 = self.ct
        self.ct = self.ct1
        self.ct1 = np.logical_xor(st1, self.ct)
        self.ct1 = np.logical_xor(self.ct1, self.__T2())
        return self.ct


if __name__ == "__main__":
    # 128 bit key
    key = 0xB5EC3B0FC1A0F8B17A5BFAEC08FBE30A

    # convert to binary list
    key_bin = [int(x) for x in bin(key)[2:]]

    l1 = LFSR([25, 20, 12, 8], key_bin[:25])
    l2 = LFSR([31, 24, 16, 12], key_bin[25:25+31])
    l3 = LFSR([33, 28, 24, 4], key_bin[25+31:25+31+33])
    l4 = LFSR([39, 36, 28, 4], key_bin[25+31+33:])

    # generate the actual sequence
    length = 2000
    sequence = np.ones(length) * -1

    fsm = FSM()

    for i in range(length):
        l1.shift()
        l2.shift()
        l3.shift()
        l4.shift()

        ct_blend = fsm.blend(l1.outbit, l2.outbit, l3.outbit, l4.outbit)
        cipherbit = np.logical_xor(l1.outbit, np.logical_xor(
            l2.outbit, np.logical_xor(l3.outbit, np.logical_xor(l4.outbit, ct_blend))))
        sequence[i] = cipherbit[0]

    print("".join(str(s) for s in sequence.astype(int)))
