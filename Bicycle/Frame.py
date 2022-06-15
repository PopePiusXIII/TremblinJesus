import numpy as np
from VectorMath import rotatez


class Frame:
    def __init__(self):
        self.r = np.array([[0.0], [0.0], [0.0]])
        self.v = np.array([[0.0], [0.0], [0.0]])
        self.a = np.array([[0.0], [0.0], [0.0]])
        self.theta = np.array([[0.0], [0.0], [0.0]])
        self.omega = np.array([[0.0], [0.0], [0.0]])
        self.alpha = np.array([[0.0], [0.0], [0.0]])


if __name__ == "__main__":
    frame_a = Frame()
    frame_g = Frame()

    frame_a.v[1][0] = 10
