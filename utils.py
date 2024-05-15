# (c) First edit on: 01 November 2023 Nonna, "utils.py", library for utility functions.
# This code is licensed under MIT license (see LICENSE.txt for details)

def check_type(object: object, types) -> bool:
    if not isinstance(object, types):
        acceptedTypes = tuple(types) if isinstance(types, (list, set, tuple)) else tuple((types, ))
        raise TypeError(f"Expected {' or '.join(type.__name__ for type in acceptedTypes)}, but got {type(object).__name__} instead.")
    return True

from math import sin
from math import pi as PI
def oscillator(t: float, halfPeriod: float, oscillatorFunction = sin):
    return round(oscillatorFunction(PI * t / halfPeriod) ** 2, 8)

def doNothing(any = None):
    return any

def getBit(value, lowerBound: int, upperBound: int = -1):
        value = "{0:b}".format(value)[::-1]
        if len(value) <= lowerBound:
            return 0
        if upperBound == -1: return int(value[lowerBound][::-1], 2)
        upperBound += 1
        return int(value[lowerBound : upperBound][::-1], 2)

flatten = lambda l: sum(map(flatten, l), []) if isinstance(l, list) else [l]

from math import acos as arccos