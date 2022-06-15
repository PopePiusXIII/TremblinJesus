import numpy as np
from Frame import Frame
from Axle import FrontAxle, RearAxle
from VectorMath import rotatez


class Car:
    def __init__(self):
        self.mass = 1000  # mass of car

        self.frame_a = Frame()  # local frame
        self.frame_ag = Frame()

        self.izz = 2000.0
        self.ics = np.array([self.frame_a.r, self.frame_a.v, self.frame_a.theta, self.frame_a.omega]).flatten()

        self.FrontAxle = FrontAxle()
        self.FrontAxle.d = np.array([[1], [0], [0]])
        self.RearAxle = RearAxle()
        self.RearAxle.d = np.array([[-1], [0], [0]])

    def set_ics(self, r, rdot, omega, alpha):
        self.ics = np.array([r, rdot, omega, alpha]).flatten()
        self.frame_a.v = rdot
        self.FrontAxle.frame_a.v = rdot
        self.RearAxle.frame_a.v = rdot
        self.frame_ag.v = rdot

        self.frame_a.omega = omega
        self.FrontAxle.frame_a.omega = omega
        self.RearAxle.frame_a.omega = omega
        self.frame_ag.omega = omega

    def mz(self, debug=False):
        fyf = self.FrontAxle.fy(debug)
        fyr = self.RearAxle.fy(debug)
        mzf = np.cross(self.FrontAxle.d, fyf, axis=0)
        mzr = np.cross(self.RearAxle.d, fyr, axis=0)
        if debug:
            print('mzf=', mzf[2, 0], '   fyf=', fyf[1, 0], '  d_f=', self.FrontAxle.d[0, 0])
            print('mzr=', mzr[2, 0], '   fyr=', fyr[1, 0], '    d_r=', self.RearAxle.d[0, 0], '\n\n')
        return mzf + mzr

    def alpha(self, debug=False):
        return self.mz(debug=debug) / self.izz

    def ay(self):
        ay = (self.FrontAxle.fy() + self.RearAxle.fy()) / self.mass
        ay_a = ay - np.cross(self.frame_a.omega, self.frame_a.v, axis=0)
        # like this for now cuz i dont want x accel
        return np.array([[0.0], ay_a[1],  [0.0]])

    def dsdt(self, t, s, result):
        s = s.flatten()
        self.frame_a.r = np.array([[s[0]], [s[1]], [s[2]]])
        self.frame_a.v = np.array([[s[3]], [s[4]], [s[5]]])
        self.frame_a.theta = np.array([[s[6]], [s[7]], [s[8]]])
        self.frame_a.omega = np.array([[s[9]], [s[10]], [s[11]]])

        self.FrontAxle.frame_a.v = self.frame_a.v
        self.RearAxle.frame_a.v = self.frame_a.v
        self.FrontAxle.frame_a.omega = self.frame_a.omega
        self.RearAxle.frame_a.omega = self.frame_a.omega

        self.frame_a.alpha = self.alpha(debug=False)
        self.frame_a.a = self.ay()

        self.frame_ag.r = self.frame_ag.r + self.frame_ag.v * (t - result.local['time'][-1])
        self.frame_ag.v = rotatez(self.frame_a.theta[2], self.frame_a.v)
        self.frame_ag.a = rotatez(self.frame_a.theta[2], self.frame_a.a + np.cross(self.frame_a.omega, self.frame_a.v,
                                  axis=0))
        result.write_local(t)
        result.write_world(t)
        return np.array([self.frame_a.v, self.frame_a.a, self.frame_a.omega, self.frame_a.alpha]).flatten()

