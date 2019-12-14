import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.pylab import *
from scipy.integrate import ode

def tank(t, y):
    """
    Dynamic balance for a CSTR
    """
    F = 20.1        # L/main
    CA_in = 2.5
    v = 100
    K = 0.15

    CA = y[0]

    n = len(y)
    dydt = np.zeros((n,1))
    dydt[0] = F/v*(CA_in - CA) - k*CA**2
    return dydt

# this is the same integrator we use in the AdaptiveControl.py file
if __name__ == '__main__':
    # Start by specifying the set_integrator
    # use 'vode' with 'backward differentiation formula'
    r = ode(tank).set_integrator('vode', method='bdf')

    t_start = 0.0
    t_final = 10.0
    delta_t = 0.1
    # force this to be an int
    num_steps = int(np.floor((t_final - t_start)/delta_t) + 1)

    CA_t_zero = 0.5
    r.set_initial_value([CA_t_zero], t_start)

    # print(int(num_steps), 1)
    # numpy 1.11.0 will support float indices like 1.0
    # if this is the case then perhaps you're using old code
    t = np.zeros((num_steps,1))
    CA = np.zeros((num_steps,1))
    t[0] = t_start
    CA[0] = CA_t_zero

    k = 1
    while r.successful() and k < num_steps:
        r.integrate(r.t + delta_t)

        # store results to plot later
        t[k] = r.t
        CA[k] = r.y[0]
        k += 1

    # plot trajectories
    # switched to plt, seeing issues.. Seems that sciPy has it's own
    # version of matplotlib and i'm running into trouble here
    # so go all the way sciPy or go all the way plt, pick one.
    plt.plot(t, CA)
    # don't use 'on' or 'True' for thi sanymore, this really is old code
    # just True without quotes will do
    #grid(True)
    plt.xlabel('Time [Minutes]')
    plt.ylabel('Concentration [mol/L]')
    plt.show()
