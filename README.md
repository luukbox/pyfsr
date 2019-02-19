# pyfsr

This module was developed in the course of a bachelor thesis and is in no way suitable for use in production. It enables a simple generation of pseudo random bit streams by providing linear and non-linear feedback shift register implementations.

# Installation

This package is currently not released on PyPI and must therefore be installed locally. To do that you have the following two options:

install with pip + github url

```bash
# install
$ pip install git+git://github.com/luukbox/pyfsr@master

# upgrade
$ pip install --upgrade git+git://github.com/luukbox/pyfsr@master
```

clone the repository and build it in your working directory

```bash
$ pip install setuptools
$ git clone https://github.com/luukbox/pyfsr.git
$ cd pyfsr
$ python setup.py sdist
$ pip install ./dist/pyfsr-VERSION_GOES_HERE.tar.gz
```

# Examples

## [LFSR](https://en.wikipedia.org/wiki/Linear-feedback_shift_register)

- [Fibonacci](https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Fibonacci_LFSRs) (external feedback)
- [Galois](https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Galois_LFSRs) (internal feedback)

```python
from pyfsr import LFSR, FSRFunction

# x^3 + x^2 + 1
l = LFSR(poly=[3,2], initstate=[0,1,0])
print(l.sequence(5))
# --> [0 1 0 1 1]

l = LFSR(poly=[3,2], initstate=[0,1,0], initcycles=3)
print(l.sequence(5))
# --> [1 1 1 0 0]

l = LFSR(poly=[3, 2], initstate=[0, 1, 0],
         initcycles=3, feedback='internal')
print(l.sequence(5))
# --> [1 0 1 0 0]

fsrfunc = FSRFunction([4, 3, '*', 0, '+'])
l = LFSR(poly=[5, 3], initstate=[0, 1, 0, 1, 1], outfunc=fsrfunc)
print(l.shift())
# --> 1 (l.state[4] and l.state[3] xor l.state[0])
```

## [NLFSR](https://en.wikipedia.org/wiki/Nonlinear-feedback_shift_register)

Use a non linear input function. Otherwise the resulting FSR would be a less efficient LFSR.

```python
from pyfsr import NLFSR, FSRFunction

infunc = FSRFunction([3, 2, 4, "*", "+"])
nl = NLFSR(initstate=[0, 1, 0, 0, 1], infunc=infunc)
print(nl.sequence(10))
# --> [1 0 0 1 0 0 0 1 0 0]

outfunc = FSRFunction([1, 2, 3, "+", "+"])
nl = NLFSR(initstate="ones", infunc=infunc,
           outfunc=outfunc, size=5, initcycles=13)
print(nl.sequence(10))
# --> [1 1 1 0 1 1 1 0 1 1]
```

## FSRFunction

Functions in [Reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation). Operands are indices of the solve methods parameter.

Operators:

- '\+' (xor)
- '\*' (and)

```python
fsrfunc = FSRFunction([4, 3, '+',  1, 2, '*', '+'])
print(fsrfunc.solve([0, 1, 0, 0, 1]))
# --> 1 [(0 xor 1) xor (0 and 1)]
```
