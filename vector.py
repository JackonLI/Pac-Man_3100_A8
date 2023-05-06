"""
Project: Pac-Man A8 in CSCI3100, CUHK
Program: Maze generator and object classes for classic mode game
Main Contributor: Haoyuan YUE
Created: March 28, 2023
Last Modified: May 5, 2023
Github Access: https://github.com/JackonLI/Pac-Man_3100_A8

Description: 
This class is used to calculate the distance

Classes: 
- Vector2-Generate a vector between two points

Dependencies:
- NA

How to use it:
#

Known issues:
None.

Acknowledgement and References: 
Bandai Namco Entertainment America Inc: https://www.bandainamcoent.com/games/pac-man
Github project: https://github.com/greyblue9/pacman-python
Github project: https://github.com/lylant/PacMan-Pygame
"""
import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    def copy(self):
        return Vector2(self.x, self.y)

    def asTuple(self):
        return self.x, self.y

    def asInt(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
