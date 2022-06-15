from Vehicle import Car
from scipy.integrate import solve_ivp
from ResultsHandler import Result
import matplotlib.pyplot as plt
from VectorMath import rotatez
import numpy as np

t0 = 0
t1 = 10
car = Car()
results = Result(car)
car.set_ics(np.array([[0.0], [0.0], [0.0]]), np.array([[20.0], [0.0], [0.0]]), np.array([[0.0], [0.0], [0.0]]),
            np.array([[0.0], [0.0], [0.0]]))


car.FrontAxle.delta = .1
results.write_local(0)
results.write_world(0)
sol = solve_ivp(car.dsdt, [t0, t1], car.ics, args=[results], max_step=.01)

plt.title('global position')
plt.scatter(results.local['x'], results.local['y'], s=1)
plt.scatter(results.world['x'], results.world['y'], s=1)
plt.axis('equal')
plt.show()

plt.title("velocities")
plt.plot(results.local['vx'], label='localx')
plt.plot(results.local['vy'], label='localy')

plt.plot(results.world['vx'], label='worldx')
plt.plot(results.world['vy'], label='worldy')
plt.legend()
plt.show()

plt.title("local acceleration")
plt.plot(results.local['ax'])
plt.plot(results.local['ay'])
plt.show()
plt.title('world accel')
plt.plot(results.world['ax'])
plt.plot(results.world['ay'])
plt.show()

plt.title('slip angles')
plt.scatter(results.local['time'], results.local['saf'], s=1, c='r')
plt.scatter(results.local['time'], results.local['sar'], s=1, c='b')
plt.show()

plt.title('forces')
plt.scatter(results.local['time'], results.local['fyf'], s=1)
plt.scatter(results.local['time'], results.local['fyr'], s=1)
plt.show()

plt.title('angles')
plt.scatter(results.local['time'], results.local['omega'], s=1, label='omega')
plt.scatter(results.local['time'], results.local['theta'], s=1, label='theta')
plt.legend()
plt.show()
