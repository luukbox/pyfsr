"""
    File name: fsr_function.py
    Author: Lukas Müller
    Python Version: 3.6
"""

import numpy as np


class FSRFunction():
    """Function that can be used as input or output bit generator
    Args:
        expression (list[int or str]): list of state indices and operators 
            of the function in reverse polish notation
            supported operators: "+" (xor), "*" (and)
    """

    def __init__(self, expression):
        self.expression = []
        operands_count = 0
        operators_count = 0
        for token in expression:
            if isinstance(token, int):
                operands_count += 1
                self.expression.append(token)
            elif token == '+' or token == '*':
                operators_count += 1
                self.expression.append(token)
            else:
                raise Exception(
                    "Unknown Token in FSRFunction expression:", token)
        # check if we have enough indices and operands in the stack
        if operands_count - operators_count != 1:
            raise Exception("expression invalid:", expression)
        self.__checked = False

    def __check(self, fsr_size):
        for token in self.expression:
            if isinstance(token, int):
                if token > fsr_size - 1 or token < 0:
                    raise Exception("expression index out of bounds")
        self.__checked = True

    def __str__(self):
        out = []
        for e in self.expression:
            if e == "*":
                out.append("and")
            elif e == "+":
                out.append("xor")
            else:
                out.append(str(e))
        return "-".join(str(o) for o in out)

    def solve(self, fsr_state):
        """solves the function
        Args:
            fsr_state (list[int]): list of bits

        Returns:
            int: result of the operations
        """
        if not self.__checked:
            self.__check(len(fsr_state))

        stack = []
        for token in self.expression:
            if isinstance(token, int):
                # the token is an index of the state --> push the operand on the stack
                stack.append(fsr_state[token])
            else:
                # the token is an operator
                if len(stack) < 2:
                    raise Exception(
                        "function expression invalid: not enough values on the stack to perform operation")
                val1 = stack.pop()
                val2 = stack.pop()
                if token == '+':  # (xor)
                    stack.append(np.logical_xor(val1, val2) * 1)
                else:  # '*' (and) operator
                    stack.append(np.logical_and(val1, val2) * 1)

        if not len(stack) == 1:
            # this should actually never be the case, since we make sure that
            # the number of operators == number of operands - 1
            raise Exception(
                "output function expression invalid: too many values are left on the stack")
        return stack.pop()
