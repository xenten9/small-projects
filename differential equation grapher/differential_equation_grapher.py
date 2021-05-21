# Differential_Equation_Grapher.py
from PIL.Image import new as newimg
from math import sin, cos
from math import ceil, floor, atan, e, pi, inf
from numpy import linspace, sign
from matplotlib import pyplot as plot

func = "arctan(x + y) + sin(x) + cos(y)"
def f(x: float, y: float) -> float:
    try:
        return atan(x + y) + sin(x) + cos(y)
    except (ZeroDivisionError, ValueError):
        # Domain error
        return inf

def diff(x: float, y: float) -> float:
    # Find the value given (x, y)
    z = f(x, y)

    # Check if the value had a domain error
    if z == inf:
        return inf

    # Map from (-inf, inf) -> (-1, 1)
    z = (2 * atan(z)) / pi # faster
    #z = 2/(1+exp(-z)) - 1 # slower

    return z

def value_to_rgb(v: float, c_neg: tuple, c_pos: tuple, c_inf: tuple) -> tuple:
    if v == inf:
        return c_inf

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
        print('value: {}'.format(v))
        raise ValueError('value must be in range (-1, 1)')

def make_domain(domain: tuple, interval: float) -> list:
    # Make a list of x values
    z = list(range(floor(domain[0] / interval), ceil(domain[1] / interval), 1))
    z = [element * interval for element in z]
    q = []
    for element in z:
        if (domain[0] < element < domain[1]):
            q.append(element)
    return q

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

def spow(x: float, n: float) -> float:
    x = abs(x)**n * sign(x)
    return x

def convert_to_rgb(color: tuple) -> tuple:
    red = ceil(color[0] * 255)
    green = ceil(color[1] * 255)
    blue = ceil(color[2] * 255)
    return (red, green, blue)

def main():
    # Setup
    accuracy = 3
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
    cfactor = 1

    # Euler line
    pos = (1, 1)
    dx = 0.00001
    iterlimit = 40000000

    # Image
    de_image = newimg("RGB", size, "#ffffff")

    # iterate over image
    for y in range(0, size[1]):
        #print("y: " + str(y))
        for x in range(0, size[0]):
            v = diff(hpoints[x], vpoints[y])
            de_image.putpixel((x, -(y + 1)), value_to_rgb(v, c_neg, c_pos, c_inf))
    print("Image Created")

    # setup plot
    fig = plot.figure()
    ax = fig.add_subplot()

    # plot image
    ax.imshow(de_image, extent = (hbounds[0], hbounds[1], vbounds[0], vbounds[1]))

    # plot major ticks
    ax.set_xticks(hmajlines)
    ax.set_yticks(vmajlines)
    ax.grid(True, which = "major", c = c_major)

    # origin lines
    ax.axhline(0, c = (1, 1, 1))
    ax.axvline(0, c = (1, 1, 1))

    # labels
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_title("Slope Field of f(x, y) = " + func)
    euler_line = create_euler_line(pos, dx, hbounds, vbounds, iterlimit)

    print("Euler line created")
    ax.plot(euler_line['x'], euler_line['y'], color = c_euler,
            label = "Trends starting at: " + str(pos))

    plot.legend()

    # display graph
    plot.show()

if __name__ == '__main__':
    main()
