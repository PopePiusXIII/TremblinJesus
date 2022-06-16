import numpy as np
from math import atan2
from Frame import Frame
from Axle import FrontAxle, RearAxle
from VectorMath import rotatez


class Car:
    def __init__(self, frame_g):
        self.mass = 1000  # mass of car

        self.frame_a = Frame()  # local frame
        self.frame_g = Frame()

        self.izz = 2000.0

        self.ics = np.array([self.frame_a.r, self.frame_a.v, self.frame_a.theta, self.frame_a.omega])

        self.FrontAxle = FrontAxle()
        self.FrontAxle.frame_a = self.frame_a
        self.RearAxle = RearAxle()
        self.RearAxle.frame_a = self.frame_a
        self.RearAxle.d = np.array([[-1], [0], [0]])

    def set_ics(self, x, y, vx, vy, w, alpha):
        self.ics = np.array([x, y, vx, vy, w, alpha])

    def alpha_z(self):
        """
        angular acceleration of vehicle ccw +
        """
        mzf = self.FrontAxle.fy() * self.FrontAxle.d[0][0]
        mzr = self.RearAxle.fy() * self.RearAxle.d[0][0]
        mz = mzf + mzr
        return np.array([[0.0], [0.0], [mz/ self.izz]])

    def ay(self):
        """
        lateral acceleration of vehicle left is positive
        """
        return (self.FrontAxle.fy() + self.RearAxle.fy()) / self.mass

    def dsdt(self, t, s):

        v_va = s[1]
        w_va = s[3]

        alpha = self.alpha_z()
        r2dot_va = np.array([[0.0], [self.ay()], [0.0]]) + np.cross(w_va, v_va, axis=0)
        r2dot_va = np.array([[0], r2dot_va[1], [0]])
        return [v_va, r2dot_va, w_va, alpha]

