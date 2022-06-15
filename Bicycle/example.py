import numpy as np
import math
import matplotlib.pyplot as plt

max_steer = np.radians(30.0)  # [rad] max steering angle
L = 2  # [m] Wheel base of vehicle
dt = 0.01
Lr = L / 2.0  # [m]
Lf = L - Lr
Cf = 50000  # N/rad
Cr = 50000  # N/rad
Iz = 2000.0  # kg/m2
m = 1000.0  # kg


# non-linear lateral bicycle model
class NonLinearBicycleModel():
    def __init__(self, x=0.0, y=0.0, yaw=0.0, vx=20, vy=0, omega=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.vx = vx
        self.vy = vy
        self.omega = omega
        # Aerodynamic and friction coefficients
        self.c_a = 0
        self.c_r1 = 0
        self.saf = 0
        self.sar = 0
        self.ay = 0

    def update(self, throttle, delta):
        delta = np.clip(delta, -max_steer, max_steer)
        self.x = self.x + self.vx * math.cos(self.yaw) * dt - self.vy * math.sin(self.yaw) * dt
        self.y = self.y + self.vx * math.sin(self.yaw) * dt + self.vy * math.cos(self.yaw) * dt
        self.yaw = self.yaw + self.omega * dt
        self.yaw = normalize_angle(self.yaw)
        self.saf = math.atan2((self.vy + Lf * self.omega) / self.vx - delta, 1.0)
        self.sar = math.atan2(((self.vy - Lr * self.omega) / self.vx), 1.0)
        Ffy = -Cf * math.atan2(((self.vy + Lf * self.omega) / self.vx - delta), 1.0)
        Fry = -Cr * math.atan2((self.vy - Lr * self.omega) / self.vx, 1.0)
        self.vx = self.vx
        self.vy = self.vy + (Fry / m + Ffy / m - self.vx * self.omega) * dt
        self.omega = self.omega + (Ffy * Lf - Fry * Lr) / Iz * dt


def normalize_angle(angle):
    """
    Normalize an angle to [-pi, pi].
    :param angle: (float)
    :return: (float) Angle in radian in [-pi, pi]
    """
    while angle > np.pi:
        angle -= 2.0 * np.pi

    while angle < -np.pi:
        angle += 2.0 * np.pi

    return angle


bike = NonLinearBicycleModel()
x = []
y = []
vx = []
vy = []
t=[]
saf=[]
sar=[]
ay = []
w = []
for i in np.linspace(0, 100, 2000):
    print(i)
    bike.update(0, .1)
    t.append(i)
    ay.append(bike.ay)
    x.append(bike.x)
    y.append(bike.y)
    saf.append(bike.saf)
    sar.append(bike.sar)
    vx.append(bike.vx)
    vy.append(bike.vy)
    w.append(bike.omega)
plt.scatter(x, y)
plt.axis('equal')
plt.show()

plt.scatter(t, vx)
plt.scatter(t, vy)
plt.scatter(t, (np.array(vx)**2 + np.array(vy)**2)**.5)
plt.show()

plt.title('slip angles')
plt.scatter(t, saf)
plt.scatter(t, sar)
plt.show()

plt.scatter(t, w)
plt.show()

plt.scatter(t, ay)
plt.show()