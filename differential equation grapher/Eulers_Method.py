# Standard Library
from math import cos, sin

# Differential equation
def f(x: float, y: float) -> float:
    z = x+y
    return z

function = 'x+y'

# Euler approximation method
def eulers_method(x0: float, y0: float, x1: float, itercount: int) -> list:
    dx = (x1-x0)/itercount
    print('dx: {}'.format(dx))
    z = [(x0, y0)]
    for _ in range(0, itercount):
        #print(x0, y0)
        y0 += dx * f(x0, y0)
        x0 += dx
        z.append((x0, y0))
    return z

# Range
x0 = 1
x1 = 2

# Number of iterations
iter_count = 2

# Initial value
y0 = 2

# Print results
z = eulers_method(x0, y0, x1, iter_count)
for item in z:
    item = (round(item[0], 3), round(item[1], 3))
    #print(item)

print('Initial (x0, y0): ({:.3f}, {:.3f})'.format(*z[0]))
print('Final   (x1, y1): ({:.3f}, {:.3f})'.format(*z[-1]))
print('Function: dy/dx = {}'.format(function))
