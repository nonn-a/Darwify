# (c) Last edit on: 14 October 2023 Nonna Giuseppe, "DSP.py", "Discrete Space Provider"
# This code is licensed under MIT license (see LICENSE.txt for details)

from math import floor

def make_matrix(dimensions: tuple, recursion_object):
    if dimensions == tuple():
        return recursion_object
    return [make_matrix(dimensions[:-1], recursion_object) for _ in range(dimensions[-1])]

def isWithin(space: "Space", point: tuple[float]):
    return all([point[n] < space.dimensions[n] and point[n] >= 0 for n in range(len(space.dimensions))])

def point(space: "Space", point: tuple[int], object = None):
    if isWithin(space, point):
        point = point[::-1]
        temporary = space.matrix
        for i in point[:-1]:
            temporary = temporary[i]
        if object is not None:
            temporary[point[-1]] = object
        return temporary[point[-1]]
    return None

class Space():
    def __init__(self, dimensions: tuple, background: str = "·"):
        if not isinstance(dimensions, (tuple, list)) or not all(isinstance(dimension, (int, float)) for dimension in dimensions):
            raise TypeError("Expected int or float values for space dimension definitions.")
        
        self.dimensions = tuple(floor(dimension) for dimension in dimensions)
        self.background = background[0] if isinstance(background, (str, list, tuple)) else background
        self.matrix = make_matrix(self.dimensions, self.background)