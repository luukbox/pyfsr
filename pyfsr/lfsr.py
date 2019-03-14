"""
    File name: lfsr.py
    Author: Lukas Müller
    Python Version: 3.6
"""

import numpy as np
from tqdm import tqdm
from .fsr_function import FSRFunction


class LFSR():
    """Linear Feedback Shift Register
    Args:
        `poly` (list[int]): the feedback polynom
        `initstate` (list[int] or "ones" or "random"): the initial state
        `initcycles` (int, optional): number of cycles to run after initialization. 
            useful to obfuscate the state
        `feedback` ('external' or 'internal', optional): feedback type.
            defaults to external
        `outfunc` (FSRFunction, optional): output function that generates 
            the outbit. defaults to FSRFuction([np.max(poly)-1])
    """

    def __init__(self, poly, initstate, initcycles=-1, feedback="external", outfunc="default"):
        if isinstance(initstate, list):
            self.initstate = np.array(initstate)
        elif isinstance(initstate, str):
            if initstate == 'ones':
                self.initstate = np.ones(np.max(poly))
            elif initstate == 'random':
                self.initstate = np.random.randint(0, 2, np.max(poly))
            else:
                raise Exception("UNKNOWN INITSTATE STRING: ", initstate)
        else:
            raise Exception("UNKNOWN INITSTATE VALUE:", initstate)

        if feedback == "internal":
            self.__internal_feedback = True
        elif feedback == "external":
            self.__internal_feedback = False
        else:
            raise Exception("unknown feedback type:", feedback)

        # make sure that the poly is in the right order
        # irrelevant for the lfsr itself, just looks better when printed
        poly.sort(reverse=True)
        self.poly = poly

        # set the current state to the initstate
        self.state = self.initstate.astype(int)

        # initialize the output and feedback bits
        self.outbit = -1
        self.feedback_bit = -1

        # set the other stuff
        self.feedback = feedback
        self.cycles = 0

        # check the poly and initstate
        self.__check()

        # set the output function
        if outfunc == "default":
            # set the output to the last index of the state
            self.outfunc = FSRFunction([len(self.state) - 1])
        else:
            if not isinstance(outfunc, FSRFunction):
                raise Exception(
                    "out_func has to be an instance of FSRFunction")
            self.outfunc = outfunc

        # if initcycles are set, we want to shift the register
        # n times in order to hide the initstate from the out sequence
        if initcycles > 0:
            self.sequence(initcycles, show_progress=False)
            self.cycles = 0
            self.outbit = -1
            self.feedback_bit = -1
            self.initstate = self.state  # set the actual initstate

    def __check(self):
        if len(self.poly) < 2:
            raise Exception('Feedback polynomial too short')
        if np.min(self.poly) < 1:
            raise Exception('Use positive values in feedback polynomial')
        if np.max(self.poly) != len(self.initstate):
            raise Exception(
                "initstate length has to equal the polynomials degree")

    def __internal_feedback_shift(self):
        self.feedback_bit = self.state[-1]
        self.state = np.roll(self.state, 1)
        for i in range(1, len(self.poly)):
            self.state[self.poly[i]] = np.logical_xor(
                self.feedback_bit, self.state[self.poly[i]]) * 1

    def __external_feedback_shift(self):
        # compute feedback bit from state and polynomial
        self.feedback_bit = self.state[self.poly[0]-1]
        for i in range(1, len(self.poly)):
            self.feedback_bit = np.logical_xor(
                self.feedback_bit, self.state[self.poly[i]-1]) * 1  # * 1 casts bool to int

        # shift the register once -> roll pushes the last bit (the outBit) to the beginning
        self.state = np.roll(self.state, 1)

        # replace the outbit (now at index 0) with the feebackBit
        self.state[0] = self.feedback_bit

    def shift(self):
        """performs one cycle
        Returns:
            `int`: output bit
        """
        self.outbit = self.outfunc.solve(self.state)
        if self.__internal_feedback:
            self.__internal_feedback_shift()
        else:
            self.__external_feedback_shift()

        self.cycles += 1
        return self.outbit

    def sequence(self, n, show_progress=True):
        """generates a pseudo random sequence of length n
        Args:
            `n` (int): sequence length
        Returns:
           `np.array[int]`: binary sequence
        """
        seq = np.ones(n)
        if show_progress:
            for i in tqdm(range(n), ascii=True, desc=f'Generating {n} bit sequence'):
                seq[i] = self.shift()
        else:
            for i in range(n):
                seq[i] = self.shift()
        return seq.astype(int)

    def reset(self):
        """resets the state
        """
        feedback = "external"
        if self.__internal_feedback:
            feedback = "internal"
        self.__init__(poly=self.poly,
                      initstate=self.initstate.tolist(), feedback=feedback)

    def change_poly(self, poly):
        """changes the feedback polynom without changing the state or the output function
        Args:
            `poly` (list[int]): new polynom. the degree has to equal the size of the state
        """
        if np.max(poly) != np.max(self.poly):
            raise Exception(
                "degree of new poly has to equal the size of the state")
        poly.sort(reverse=True)
        self.poly = poly
        self.__check()

    def __str__(self):
        feedback = "ext"
        if self.__internal_feedback:
            feedback = "int"
        poly = "-".join(str(p) for p in self.poly)
        output = f'lfsr_({poly})_{feedback}'
        if len(self.outfunc.expression) == 1:
            # it's the primitive outfunction, so we ignore it
            return output
        return f'{output}_out({self.outfunc})'

    def print_info(self):
        feedback = "External"
        if self.__internal_feedback:
            feedback = "Internal"
        print('------%d bit LFSR with------' %
              (np.max(self.poly)))
        print('Feedback poly:', self.poly)
        print(f'Feedback type: {feedback}')
        print('Expected period (if primitive poly):', 2**np.max(self.poly)-1)
        print('Output function:', self.outfunc)
        print('And Current:')
        print('     State:', self.state)
        print('     Cycles:', self.cycles)
        print('     Output bit:', self.outbit)
        print('     Feedback bit:', self.feedback_bit)
        print('----------------------------')
