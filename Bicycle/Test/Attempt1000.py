import numpy as np
from math import atan2
from Bicycle.Frame import Frame
from Bicycle.Axle import Axle
from Bicycle.VectorMath import rotatez


class Car:
    def __init__(self, frame_g):
        self.mass = 1000  # mass of car

        self.frame_a = Frame()  # local frame
        self.frame_g = Frame()

        self.izz = 2000.0

        self.ics = np.array([self.frame_a.r, self.frame_a.v, self.frame_a.theta, self.frame_a.omega])

        self.FrontAxle = Axle()
        self.RearAxle = Axle()

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

    def sa(self, axle):
        delta, vx, vy, kyf, kyr, w, a, b = self.get_states()
        vx, vy, vz = rotatez(-self.frame_a.theta[2], self.frame_a.v).flatten()
        w = w[2][0]
        if axle == 'f':
            v = np.array([vx, vy + w * a[0][0], vz])
            vfx, vfy, vfz = rotatez(-delta, v).flatten()
            return atan2(vfy, vfx)
        elif axle == 'r':
            return atan2(vy + w * -b[0][0], vx)
        else:
            print("not valid choice")

    def fyf(self):
        delta, vx, vy, kyf, kyr, w, a, b = self.get_states()
        saf = self.sa('f')
        self.FrontAxle.sa = saf
        fyf = -kyf * saf
        return fyf

    def fyr(self):
        delta, vx, vy, kyf, kyr, w, a, b = self.get_states()
        sar = self.sa('r')
        self.RearAxle.sa = sar
        fyr = -kyr * sar
        return fyr

    def mz(self):
        delta, vx, vy, kyf, kyr, w, a, b = self.get_states()
        saf = self.sa('f')
        sar = self.sa('r')
        mzf = -kyf * saf * a[0][0]
        mzr = -kyr * sar * -b[0][0]
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

