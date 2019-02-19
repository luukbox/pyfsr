'''
    File name: misc.py
    Author: Lukas Müller
    Python Version: 3.6
'''

import numpy as np
from pyfsr import LFSR, NLFSR, FSRFunction

r = LFSR(poly=[11, 9], initstate="random")
r.print_info()

print("\nS1:", r.sequence(10))
print()

r.change_poly(poly=[11, 6, 3])
r.print_info()

print("\nS2:", r.sequence(10))
print()

l = LFSR(poly=[9, 5], initstate=[1, 0, 1, 1, 0, 0, 1, 0, 1],
         initcycles=2**7, feedback="internal")
l.print_info()

print("\nS3:", l.sequence(10))
print()

l.reset()
l.print_info()
print()

l = LFSR(poly=[9, 5, 2, 1], initstate="random")
l.print_info()

sequence = np.append([], l.shift())
while not np.array_equal(l.state, l.initstate):
    sequence = np.append(sequence, l.shift())
print("Actual period:", l.cycles)
print("\nS4:", sequence.astype(int))


initstate = [0, 1, 0, 1, 1]

# reverse polish notation. stateindices start from 0
fsrfunc = FSRFunction([4, 3, '+',  0, 1, '+', '+'])

print(fsrfunc.solve(initstate))
# --> (1 xor 1) xor (0 xor 1) = 1

l = LFSR(poly=[5, 3], initstate=initstate, outfunc=fsrfunc)
l.print_info()
print()

print("\nS5:", l.sequence(25))

infunc = FSRFunction([3, 2, 4, "*", "+"])
nl = NLFSR(initstate=[0, 1, 0, 0, 1], infunc=infunc)
print(nl.sequence(10))

outfunc = FSRFunction([1, 2, 3, "+", "+"])
nl = NLFSR(initstate="ones", infunc=infunc,
           outfunc=outfunc, size=5, initcycles=15)
print(nl.sequence(10))
print("\nS6:", nl.sequence(10))
nl.print_info()
