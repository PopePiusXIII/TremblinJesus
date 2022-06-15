import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

dt = .1
t = 200
steps = int(t / dt)
m = 1000
f = 1000
r_vg = np.array([0, 0, 0])
rdot_vg = np.array([20, 0, 0])
r_va = np.array([0, 0, 0])
rdot_va = np.array([0, 0, 0])
theta = np.array([0, 0, 0])
w = np.array([0, 0, 0.05])
alpha = np.array([0, 0, 0])

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
           'odo_v': []
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
    r = np.array([[cos(theta), -sin(theta), 0], [sin(theta), cos(theta), 0], [0, 0, 1]])
    return np.matmul(r, vect)


def dsdt(s):
    rdotr_va = s[1]                                             # relative velocity
    w = s[3]
    r2dotr_va = np.array([0, f/m, 0]) - np.cross(w, rdotr_va)       # relative acceleration
    alpha = np.array([0, 0, 0])
    return [rdotr_va, r2dotr_va, w, alpha]


def write_result():
    results['r_vg'].append(r_vg)
    results['rdot_vg'].append(rdot_vg)
    results['r2dot_vg'].append(r2dot_vg)
    results['r_va'].append(r_va)
    results['rdot_va'].append(rdot_va)
    results['r2dot_va'].append(r2dot_va)
    results['theta'].append(theta)
    results['w'].append(w)
    results['alpha'].append(alpha)

    odo_v = rotate3d(-theta[2], rdot_vg)
    results['odo_v'].append(odo_v)


for t in np.linspace(0, t, steps):
    s = [r_va, rdot_va, theta, w]
    rdot_va, r2dot_va, w, alpha = dsdt(s)

    r2dot_vg = rotate3d(theta[2], r2dot_va)
    r_vg = r_vg + rdot_vg * dt   # global position
    rdot_vg = rdot_vg + r2dot_vg * dt                # relative velocity with respect to theta
    theta = normalize_angle(theta + w * dt)
    w = w + alpha * dt
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
plt.plot(odo_vx, 'g-', label='vx_odo')
plt.plot(odo_vy, 'g-', label='vx_odo')
plt.show()

plt.scatter(ax_vg, ay_vg)
plt.show()

plt.plot(theta3)
plt.show()