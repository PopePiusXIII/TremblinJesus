from VectorMath import rotatez
from math import atan2
from Frame import Frame
import numpy as np


class Axle:
    def __init__(self):
        self.ky = 50000.0  # N/rad
        self.d = np.array([[1], [0], [0]])  # meters from axle centerline to cg m
        self.tire_width = .33  # m
        self.tire_diameter = 1  # m
        self.delta = 0.0  # steering angle rad
        self.sa = 0.0  # slip angle

        self.frame_a = Frame()

    def sa_calc(self):
        return 69

    def fy(self):
        self.sa_calc()
        fy = -self.sa * self.ky
        return fy


class FrontAxle(Axle):
    def sa_calc(self, debug=False):
        vx, vy, vz = rotatez(-self.frame_a.theta[2], self.frame_a.v).flatten()
        w = self.frame_a.omega[2][0]
        vx, vy, vz = np.array([vx, vy + w * self.d[0][0], vz])
        self.sa = atan2(vy, vx) - self.delta
        if debug:
            print("Front", 'vy=', self.frame_a.v[1], '  vx=', self.frame_a.v[0], ' spin=',  w * self.d[0][0], '   sa=', self.sa)


class RearAxle(Axle):
    def sa_calc(self, debug=False):
        vx, vy, vz = rotatez(-self.frame_a.theta[2], self.frame_a.v).flatten()
        w = self.frame_a.omega[2][0]
        self.sa = atan2(vy + w * self.d[0][0], vx)
        if debug:
            print("Rear", 'vy=', self.frame_a.v[1], '  vx=', self.frame_a.v[0], ' spin=',  w * self.d[0][0], '   sa=', self.sa)
