"""
    File name: tools.py
    Author: Lukas Müller
    Python Version: 3.6
"""


def roll(l):
    """rolls a list to the right
        e.g.: roll([0,1,1]) => [1,0,1]
    """
    tmp1, tmp2 = l[:-1], l[-1]
    l[1:] = tmp1
    l[0] = tmp2
    return l


def logical_xor(a, b, unsafe=False):
    """logical xor without the bloat of numpy.logical_xor
        could be substituted with numpy.logical_xor
        !important: if unsafe is set to True, a and b are not checked. This improves speed but is risky.
        expects integers [0,1] or bools
    """

    if not unsafe:
        sum = a*1+b*1
        if sum > 2 or sum < 0:
            raise Exception(
                "The parameters for logical_xor have to be booleans or integers in range [0,1]. got a: " + str(a) + ", b: " + str(b))
    return a ^ b


def logical_and(a, b, unsafe=False):
    """logical and without the bloat of numpy.logical_and
        could be substituted with numpy.logical_and
        !important: if unsafe is set to True, a and b are not checked. This improves speed but is risky.
        expects integers [0,1] or bools
    """
    if not unsafe:
        sum = a*1+b*1
        if sum > 2 or sum < 0:
            raise Exception(
                "The parameters for logical_and have to be boolean or integer in range [0,1]. got a: " + str(a) + ", b: " + str(b))
    return a & b
