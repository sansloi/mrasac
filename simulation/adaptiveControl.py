# Simulations for attitude control problem
# check requirements.txt

# Julio B. Figueroa
# December, 2019

##### Acknowledgements #####
# this code is heavily inspired by the work of Dhruv Laad
# via https://github.com/Thalaivar/control_practice

# import section
import matplotlib.pyplot as plt
from scipy.integrate import ode
import numpy as np
from numpy import sin

# adaptive gain
gamma = 2

#funciton
def model(t, X, params):

    y, ym, ar_cap, ay_cap = X

    # this is to run multiple systems with the same modelFunction()
    # just add another set of reference signals
    if params == 1:
        r = 4*sin(3*t)
    else:
        r = 4


    e = y - ym                  # signal error
    u = ar_cap*r + ay_cap*y     # control law

    ydot = y + 3*u
    ymdot = -4*ym +4*r

    ar_cap_dot = -gamma*e*r
    ay_cap_dot = -gamma*e*y

    return [ydot, ymdot, ar_cap_dot, ay_cap_dot]

def main(option):

    X0 = [0, 0, 0, 0]   # initial conditions
    t0 = 0              # time initial
    t1 = 6              # t final
    dt = 0.01       # steps

    r = ode(model).set_integrator('vode', method='bdf')
    r.set_initial_value(X0, t0).set_f_params(option)

    x = np.zeros((601, 4))
    t = []
    i = 0

    while r.successful() and r.t < t1:
        r.integrate(r.t + dt)
        x[i] = r.y
        t.append(r.t)
        i += 1

    return x, t


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == '__main__':
    x1, t1 = main(1)
    x2, t2 = main(0)

    y1 = np.reshape(x1[:,0], (601,))
    ym1 = np.reshape(x1[:,1], (601,))
    ar_cap1 = np.reshape(x1[:,2], (601,))
    ay_cap1 = np.reshape(x1[:,3], (601,))
    ar_ideal1 = (4/3)*np.ones((601,))
    ay_ideal1 = -(5/3)*np.ones((601,))

    y2 = np.reshape(x2[:,0], (601,))
    ym2 = np.reshape(x2[:,1], (601,))
    ar_cap2 = np.reshape(x2[:,2], (601,))
    ay_cap2 = np.reshape(x2[:,3], (601,))
    ar_ideal2 = (4/3)*np.ones((601,))
    ay_ideal2 = -(5/3)*np.ones((601,))

# Plotting section
    plt.subplot(211)
    plt.plot(t1 , y1, 'r', t1, ym1, 'k', t2, y2, 'b', t2, ym2, 'g')
    plt.ylabel('tracking performance')
    plt.grid()

    plt.subplot(212)
    plt.plot(t1, ar_cap1, 'b', t1, ay_cap1, 'k', t1, ar_ideal1, t1, ay_ideal1)
    plt.ylabel('parameter estimation')
    plt.grid()

    plt.show()
