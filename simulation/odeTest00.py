import numpy as np
from scipy.integrate import simps

def f1(x):
    return x**2

def f2(x):
    return x**3

x = np.array([1,3,4])
y1 = f1(x)

I1 = simps(y1, x)
print(I1)

y2 = f2(x)
I2 =  simps(y2,x)
print(I2)
