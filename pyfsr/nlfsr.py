"""
    File name: nlfsr.py
    Author: Lukas Müller
    Python Version: 3.6
"""

import numpy as np
from .fsr_function import FSRFunction


class NLFSR():
    """Non Linear Feedback Shift Register
    Args:
        `initstate` (list[int] or "ones" or "random"): the initial state
        `infunc` (FSRFunction): input function that generates the feedback_bit 
        `outfunc` (FSRFunction, optional): output function that generates 
            the outbit. defaults to FSRFuction([len(state)-1])
        `size` (int): size of the register
        `initcycles` (int, optional): number of cycles to run after initialization. 
    """

    def __init__(self, initstate, infunc, outfunc="default", size=-1, initcycles=-1):
        if isinstance(initstate, list):
            self.initstate = np.array(initstate)
            if size != -1:
                print(
                    "pyfsr Warning: The register size can be inferred from the initstate, thus setting the size is trivial and will be ignored.")
        elif isinstance(initstate, str):
            if not isinstance(size, int) or size < 1:
                raise Exception("size has to be an int > 0")
            if initstate == 'ones':
                self.initstate = np.ones(size)
            elif initstate == 'random':
                self.initstate = np.random.randint(0, 2, size)
            else:
                raise Exception("UNKNOWN INITSTATE STRING: ", initstate)
        else:
            raise Exception("UNKNOWN INITSTATE VALUE:", initstate)

        self.state = self.initstate.astype(int)

        if not isinstance(infunc, FSRFunction):
            raise Exception("infunc has to be an instance of FSRFunction")

        self.infunc = infunc

        if outfunc == "default":
            # set the output to the last index of the state
            self.outfunc = FSRFunction([len(self.state) - 1])
        else:
            if not isinstance(outfunc, FSRFunction):
                raise Exception(
                    "outfunc has to be an instance of FSRFunction")
            self.outfunc = outfunc

        self.cycles = 0
        # initialize the output and feedback bits
        self.outbit = -1
        self.feedback_bit = -1

        # if initcycles are set, we want to shift the register
        # n times in order to hide the initstate from the out sequence
        if initcycles > 0:
            self.sequence(initcycles)
            self.cycles = 0
            self.outbit = -1
            self.feedback_bit = -1
            self.initstate = self.state  # set the actual initstate

    def shift(self):
        """performs one cycle
        Returns:
            `int`: output bit
        """
        self.outbit = self.outfunc.solve(self.state)
        self.feedback_bit = self.infunc.solve(self.state)
        self.state = np.roll(self.state, 1)
        self.state[0] = self.feedback_bit
        self.cycles += 1
        return self.outbit

    def sequence(self, n):
        """generates a pseudo random sequence of length n
        Args:
            `n` (int): sequence length
        Returns:
            `np.array[int]`: binary sequence
        """
        seq = np.ones(n)
        for i in range(n):
            seq[i] = self.shift()
        return seq.astype(int)

    def reset(self):
        """resets the state
        """
        self.__init__(initstate=self.initstate.tolist(),
                      infunc=self.infunc, outfunc=self.outfunc)

    def __str__(self):
        return f'nlfsr_{len(self.state)}_in({self.infunc})_out({self.outfunc})'

    def print_info(self):
        print('------%d bit NLFSR with------' %
              (len(self.state)))
        print('Input function:', self.infunc)
        print('Output function:', self.outfunc)
        print('And Current:')
        print('     State:', self.state)
        print('     Cycles:', self.cycles)
        print('     Output bit:', self.outbit)
        print('     Feedback bit:', self.feedback_bit)
        print('----------------------------')
