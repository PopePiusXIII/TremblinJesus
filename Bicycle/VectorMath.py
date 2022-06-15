import numpy as np
from math import cos, sin


def rotatez(theta, v):
    """
    :param theta: angle theta to rotate in rad
    :param vect: vector to rotate
    :return: rotated vector
    """
    r = np.array([[cos(theta), -sin(theta), 0.0], [sin(theta), cos(theta), 0.0], [0.0, 0.0, 1.0]])
    vrot = np.matmul(r, v)
    return vrot
