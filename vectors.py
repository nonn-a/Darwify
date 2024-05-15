# (c) First edit on: 01 November 2023 Nonna, "utils.py", library for utility functions.
# This code is licensed under MIT license (see LICENSE.txt for details)

def vectorialSum(self: tuple, other: tuple):
    if (len(self) - len(other)):
        raise ValueError("Expected tuples of the same length.")
    return tuple(self[iterator] + other[iterator] for iterator in range(len(self)))

def scaleVector(value: float, other: tuple):
    return tuple(value * iterator for iterator in other)

class vectorFunction():
    def __init__(self, func: "function"):
        self.func = func

    def __call__(self, vector: tuple) -> tuple:
        return tuple(self.func(item) for item in vector)

def dotProduct(A: tuple, B: tuple):
    return sum(A[i] * B[i] for i, _ in enumerate(A))

from math import sqrt
def module(A: tuple):
    return sqrt(sum(a ** 2 for a in A))

directions = {0: (0, 1), 1: (1,  0), 2: ( 0, -1), 3: (-1, 0),
              4: (1, 1), 5: (1, -1), 6: (-1, -1), 7: (-1, 1),
              8: (0, 0)}

creatureSprites = ("^", ">", "v", "<")

vectorAbs = vectorFunction(abs)