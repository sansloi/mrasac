# test run
import matplotlib.pyplot as plt
from scipy.integrate import ode
import numpy as np
from numpy import sin

# adaptive gain
gamma = 2


def model(t, X, params):
    y, ym, ar_hat, ay_hat = X

    if params == 1:
        r = 4*sin(3*t)
    else:
        r = 4
    e = y - ym
    u = ar_hat*r + ay_hat*y

    ydot = y + 3*u
    ymdot = -4*ym + 4*r

    ar_hat_dot = -gamma*e*r
    ay_hat_dot = -gamma*e*y

    return [ydot, ymdot, ar_hat_dot, ay_hat_dot]


def main(option):
    # start with initital conditions
    X0 = [0, 0, 0, 0]
    t0 = 0
    t1 = 8                    # change this freely now!
    dt = 0.01                 # this too..
    steps = int(t1 / dt) + 1  # keep this

    r = ode(model).set_integrator('vode', method='bdf')
    r.set_initial_value(X0, t0).set_f_params(option)

    x = np.zeros((steps, 4))
    t = []
    i = 0
    while r.successful() and r.t < t1:  # checks if integration was successful
        r.integrate(r.t + dt)           # returns the integrated value at input
        x[i] = r.y
        t.append(r.t)
        i += 1
    return x, t


# really, this is the plotting section
# we're plotting the same model with two different inputs
# then we can compare them side by side, or top by down... top by bottom...
if __name__ == '__main__':

    # main(1) has the in control input, main(0) was the constant control input
    x1, t1 = main(1)            # rich
    x2, t2 = main(0)            # less rich

    steps = len(t1)             # "should" be 501
    # we're hoping len(t1) = len(t2) for now, if it changes then add a steps2
    # steps = int(t1 / dt) + 1  # +1 because python, see main(option)
    # basically, I just don't want to hardcode it

    # data for the first plot
    y1 = np.reshape(x1[:, 0], (steps,))
    ym1 = np.reshape(x1[:, 1], (steps,))
    ar_hat1 = np.reshape(x1[:, 2], (steps,))
    ay_hat1 = np.reshape(x1[:, 3], (steps,))

    # to compare against the reference, so... this is for adaptive regulation?
    ar_ideal1 = (4/3)*np.ones((steps,))
    ay_ideal1 = -(5/3)*np.ones((steps,))

    # data for the second plot
    y2 = np.reshape(x2[:, 0], (steps,))
    ym2 = np.reshape(x2[:, 1], (steps,))
    ar_hat2 = np.reshape(x2[:, 2], (steps,))
    ay_hat2 = np.reshape(x2[:, 3], (steps,))

    # now draw
    plt.subplot(211)
    plt.plot(t1, y1, 'r', t1, ym1, 'k', t2, y2, 'b', t2, ym2, 'g')
    plt.ylabel('tracking performance')
    plt.grid()

    plt.subplot(212)
    plt.plot(t1, ar_hat1, 'b', t1, ay_hat1, 'k', t1, ar_ideal1, t1, ay_ideal1)
    plt.ylabel('parameter estimation')
    plt.grid()

    plt.show()
