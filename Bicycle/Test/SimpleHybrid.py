import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos
from SimpleExamples.Attempt1000 import Car
from Frame import Frame

results = {'r_vg': [],
           'rdot_vg': [],
           'r2dot_vg': [],
           'r_va': [],
           'rdot_va': [],
           'r2dot_va': [],
           'theta': [],
           'w': [],
           'alpha': [],
           't': [],
           'odo_v': [],
           'delta': []
           }


def normalize_angle(angle):
    """
    Normalize an angle to [-pi, pi].
    :param angle: (float)
    :return: (float) Angle in radian in [-pi, pi]
    """
    norm_angle = angle
    for i in range(0, len(angle), 1):
        while norm_angle[i] > np.pi:
            norm_angle[i] -= 2.0 * np.pi

        while norm_angle[i] < -np.pi:
            norm_angle[i] += 2.0 * np.pi

    return norm_angle


def rotate3d(theta, vect):
    """
    :param theta: angle theta to rotate in rad
    :param vect: vector to rotate
    :return: rotated vector
    """
    r = np.array([[cos(theta), -sin(theta), 0.0], [sin(theta), cos(theta), 0.0], [0.0, 0.0, 1.0]])
    return np.matmul(r, vect)


def write_result():
    results['delta'].append(car.FrontAxle.delta)
    results['r_vg'].append(car.frame_a.r)
    results['rdot_vg'].append(car.frame_a.v)
    results['r2dot_vg'].append(car.frame_a.a)
    results['r_va'].append(r_va)
    results['rdot_va'].append(rdot_va)
    results['r2dot_va'].append(r2dot_va)
    results['theta'].append(car.frame_a.theta)
    results['w'].append(car.frame_a.omega)
    results['alpha'].append(car.frame_a.alpha)

    odo_v = rotate3d(-car.frame_a.theta[2], car.frame_a.v)
    results['odo_v'].append(odo_v)


dt = .001
t = 20
steps = int(t / dt)
frame_g = Frame()
car = Car(frame_g)
car.frame_a.v = np.array([20.0, 0.0, 0.0])
car.frame_a.omega = np.array([0.0, 0.0, 0.0])
r_va = np.array([0.0, 0.0, 0.0])
rdot_va = np.array([20.0, 0.0, 0.0])
r2dot_va = np.array([0.0, 0.0, 0.0])

for t in np.linspace(0, t, steps):
    car.FrontAxle.delta = .1 * sin(t/2.1)
    s = np.array([r_va, rdot_va, car.frame_a.theta, car.frame_a.omega])
    rdot_va, r2dot_va, car.frame_a.omega, car.frame_a.alpha = car.dsdt(t, s)
    rdot_va = rdot_va + r2dot_va * dt

    car.frame_a.a = rotate3d(car.frame_a.theta[2], r2dot_va + np.cross(car.frame_a.omega, rdot_va))
    car.frame_a.omega = car.frame_a.omega + car.frame_a.alpha * dt
    # car.frame_a.v = rotate3d(car.frame_a.theta[2], rdot_va)
    car.frame_a.v = car.frame_a.v + car.frame_a.a * dt
    car.frame_a.theta = normalize_angle(car.frame_a.theta + car.frame_a.omega * dt)
    car.frame_a.r = car.frame_a.r + car.frame_a.v * dt   # global position

    write_result()

x_vg, y_vg, z_vg = list(map(list, zip(*results['r_vg'])))
vx_vg, vy_vg, vz_vg = list(map(list, zip(*results['rdot_vg'])))
ax_vg, ay_vg, az_vg = list(map(list, zip(*results['r2dot_vg'])))

x_va, y_va, z_va = list(map(list, zip(*results['r_va'])))
vx_va, vy_va, vz_va = list(map(list, zip(*results['rdot_va'])))
ax_va, ay_va, az_va = list(map(list, zip(*results['r2dot_va'])))

theta1, theta2, theta3 = list(map(list, zip(*results['theta'])))

odo_vx, odo_vy, odo_vz = list(map(list, zip(*results['odo_v'])))

plt.scatter(x_vg, y_vg)
plt.show()

plt.plot(vx_va, 'r^', label='vx_va')
plt.plot(vy_va, 'r^', label='vx_va')
plt.plot(vx_vg, 'b.', label='vx_vg')
plt.plot(vy_vg, 'b.', label='vx_vg')
plt.plot(odo_vx, 'y-', label='vx_odo')
plt.plot(odo_vy, 'y-', label='vx_odo')
plt.legend()
plt.show()

# plt.scatter(ax_vg, ay_vg)
plt.scatter(ax_va, ay_va)
plt.show()

plt.plot(theta3)
plt.show()