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

    def get_states(self):
        delta = self.FrontAxle.delta
        vx, vy, vz = self.frame_a.v
        kyf = self.FrontAxle.ky
        kyr = self.RearAxle.ky
        w = self.frame_a.omega
        a = self.FrontAxle.d
        b = self.RearAxle.d
        return delta, vx, vy, kyf, kyr, w, a, b

    def fyf(self):
        return self.FrontAxle.fy()

    def fyr(self):
        return self.RearAxle.fy()

    def mz(self):
        delta, vx, vy, kyf, kyr, w, a, b = self.get_states()
        mzf = self.fyf() * a[0][0]
        mzr = self.fyr() * b[0][0]
        return mzf + mzr

    def alpha_z(self):
        return np.array([[0.0], [0.0], [self.mz() / self.izz]])

    def ay(self):
        return (self.fyf() + self.fyr()) / self.mass

    def dsdt(self, t, s):

        v_va = s[1]
        w_va = s[3]

        alpha = self.alpha_z()
        r2dot_va = np.array([[0.0], [self.ay()], [0.0]]) + np.cross(w_va, v_va, axis=0)
        r2dot_va = np.array([[0], r2dot_va[1], [0]])
        return [v_va, r2dot_va, w_va, alpha]

