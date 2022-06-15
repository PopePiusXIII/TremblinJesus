from VectorMath import rotatez
from math import atan2
from Frame import Frame
import numpy as np


class Axle:
    def __init__(self):
        self.ky = 50000.0  # N/rad
        self.d = np.array([[1], [0], [0]])  # feet from axle centerline to cg m
        self.tire_width = .33  # m
        self.tire_diameter = 1  # m
        self.delta = 0.0  # steering angle rad
        self.sa = 0.0  # slip angle

        self.frame_a = Frame()

    def sa_calc(self):
        return 69

    def fy(self, debug=False):
        self.sa_calc(debug)
        fy = -self.sa * self.ky
        return np.array([[0], [fy], [0]])


class FrontAxle(Axle):
    def sa_calc(self, debug=False):
        spin = np.cross(self.frame_a.omega, self.d, axis=0)
        v = self.frame_a.v + spin
        vfx, vfy, vfz = rotatez(-self.delta, v)
        self.sa = atan2(vfy / vfx, 1.0)
        if debug:
            print("Front", 'vy=', self.frame_a.v[1], '  vx=', self.frame_a.v[0], ' spin=', spin[1], '   sa=', self.sa)


class RearAxle(Axle):
    def sa_calc(self, debug=False):
        spin = np.cross(self.frame_a.omega, self.d, axis=0)
        vx, vy, vz = self.frame_a.v + spin
        self.sa = atan2(vy / vx, 1.0)
        if debug:
            print("Rear", 'vy=', self.frame_a.v[1], '  vx=', self.frame_a.v[0], ' spin=', spin[1], '   sa=', self.sa)
