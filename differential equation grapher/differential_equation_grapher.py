# Standard Library
from inspect import getsource
from math import atan, ceil, cos, e, floor, inf, nan, pi, sin
from typing import Tuple

# External Libraries
from matplotlib import pyplot as plot
from numpy import linspace, sign
from PIL.Image import new as newimg


# Differential Equation
def f(x: float, y: float) -> float:
    try:
        #out = atan(x + y) + sin(x) + cos(y)
        out = (x-y**2) / y
    except (ZeroDivisionError, ValueError, RuntimeWarning):
        # Domain error
        out = inf
    return out


# Converters
def compress(v: float) -> float:
    # Map from (-inf, inf) -> (-1, 1)
    if v == inf:
        return inf
    return (2 * atan(v)) / pi # faster
    #return 2/(1+exp(-v)) - 1 # slower

def value_to_rgb(v: float, c_neg: tuple, c_pos: tuple, c_inf: tuple) -> tuple:
    if -1 <= v <= 1:
        # Map from (-1, 1) to [0, 255]
        new_v = int(abs(255 * v))

        if v < 0:
            # negative
            red = floor(c_neg[0] * new_v)
            green = floor(c_neg[1] * new_v)
            blue = floor(c_neg[2] * new_v)
        else:
            # positive
            red = floor(c_pos[0] * new_v)
            green = floor(c_pos[1] * new_v)
            blue = floor(c_pos[2] * new_v)
        return (red, green, blue)
    else:
        return c_inf

def convert_to_rgb(color: Tuple[float, float, float]) -> tuple:
    red = ceil(color[0] * 255)
    green = ceil(color[1] * 255)
    blue = ceil(color[2] * 255)
    return (red, green, blue)


# Euler methods
def eulers_method(pos: tuple, dx: float) -> tuple:
    # Approximate new position given an initial position and dx
    pos = (pos[0] + dx, pos[1] + dx * f(pos[0], pos[1]))
    return pos

def create_euler_line(pos: tuple, dx: float, h_bounds: tuple,
                      v_bounds: tuple, iterlimit: int) -> dict:
    # create euler line throuhg the graph
    px = [pos[0]]
    py = [pos[1]]
    npos = pos

    # iterate the point through the slope field
    for step in range(0, iterlimit):
        # if within domain and range
        if ((h_bounds[0] <= npos[0] <= h_bounds[1])
            and (v_bounds[0] <= npos[1] <= v_bounds[1])):
            npos = eulers_method(npos, dx)

            # add position to domain and range
            px.append(npos[0])
            py.append(npos[1])
        else:
            print("iter: (" + str(step) + " / " + str(iterlimit) + ")")
            break
    px = px[:-1]
    py = py[:-1]
    px.reverse()
    py.reverse()

    npos = pos
    for step in range(0, iterlimit):
        # if within domain and range
        if ((h_bounds[0] <= npos[0] <= h_bounds[1])
            and (v_bounds[0] <= npos[1] <= v_bounds[1])):
            npos = eulers_method(npos, -dx)

            # add position to domain and range
            px.append(npos[0])
            py.append(npos[1])
        else:
            print("iter: (" + str(step) + " / " + str(iterlimit) + ")")
            break
    px = px[:-1]
    py = py[:-1]
    px.reverse()
    py.reverse()
    output = {"x": px, "y": py}

    return output


# Helper functions
def make_domain(domain: tuple, interval: float) -> list:
    # Make a list of x values
    z = list(range(floor(domain[0] / interval), ceil(domain[1] / interval), 1))
    z = [element * interval for element in z]
    q = []
    for element in z:
        if (domain[0] < element < domain[1]):
            q.append(element)
    return q

def spow(x: float, n: float) -> float:
    x = abs(x)**n * sign(x)
    return x


# Main
def main():
    # Setup
    accuracy = 2
    size = (ceil((8 * pi) * e**accuracy), ceil((8 * pi) * e**accuracy))
    majspacing = pi
    hbounds = (-8 * pi, 8 * pi)
    vbounds = (-8 * pi, 8 * pi)

    # Lines
    hpoints = linspace(hbounds[0], hbounds[1], size[0])
    vpoints = linspace(vbounds[0], vbounds[1], size[1])
    hmajlines = make_domain(hbounds, majspacing)
    vmajlines = make_domain(vbounds, majspacing)

    # Colors
    c_major = (0.8, 0.8, 0.8)
    c_pos = (0.5, 1, 0)
    c_neg = (1, 0.1, 0.1)
    c_inf = convert_to_rgb((1, 0.2, 1))
    c_euler = (0.25, 0.25, 1)

    # Euler line
    pos = (1, 1)
    dx = 0.00001
    iterlimit = 40000000

    # Image
    de_image = newimg("RGB", size, "#ffffff")

    # Iterate over image
    for y in range(0, size[1]):
        #print("y: " + str(y))
        for x in range(0, size[0]):
            v = compress(f(hpoints[x], vpoints[y]))
            de_image.putpixel((x, -(y + 1)), value_to_rgb(v, c_neg, c_pos, c_inf))
    print("Image Created")

    # Setup plot
    fig = plot.figure()
    ax = fig.add_subplot()

    # Plot image
    ax.imshow(de_image, extent = (hbounds[0], hbounds[1], vbounds[0], vbounds[1]))

    # Plot major ticks
    ax.set_xticks(hmajlines)
    ax.set_yticks(vmajlines)
    ax.grid(True, which = "major", c = c_major)

    # Origin lines
    ax.axhline(0, c = (1, 1, 1))
    ax.axvline(0, c = (1, 1, 1))

    # Get function definition
    func_string = getsource(f)
    split = func_string.split('\n')
    for part in split:
        if 'return ' in part and 'inf' not in part:
            part = part.replace('    ', '')
            part = part.removeprefix('return ')
            part = part.replace('**', '^')
            func_string = part

    # Labels
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_title("Slope Field of f(x, y) = " + func_string)

    # Creat euler line
    euler_line = create_euler_line(pos, dx, hbounds, vbounds, iterlimit)
    print("Euler line created")
    ax.plot(euler_line['x'], euler_line['y'], color = c_euler,
            label = "Trends starting at: " + str(pos))

    # Finish plotting
    plot.legend()
    plot.show()

if __name__ == '__main__':
    main()
