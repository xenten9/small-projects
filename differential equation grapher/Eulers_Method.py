# Standard Library
from inspect import getsource
from typing import Callable, List, Tuple


# Differential equation class
class DifferentialEquation:
    def __init__(self, f: Callable[[float, float], float]):
        self.f = f

    def __str__(self) -> str:
        string = getsource(self.f)
        split = string.split("\n")
        split.pop(0)
        for part in split:
            if "return " in part and "inf" not in part:
                part = part.replace("    ", "")
                part = part.removeprefix("return ")
                part = part.replace("**", "^")
                return part
        raise RuntimeError("Unable to parse f(x, y)")

    def eulers_method(
        self, x0: float, x1: float, y0: float, dx: float = None, iter: int = None
    ) -> List[Tuple[float, float]]:
        if isinstance(dx, float):
            iter = round((x1 - x0) / dx)
        if isinstance(iter, int):
            dx = (x1 - x0) / iter
        if dx is None or iter is None:
            raise ValueError("either iter or dx must be defined")

        # Go through iterations of Eulers method
        z = [(x0, y0)]
        for _ in range(0, iter):
            y0 += dx * self.f(x0, y0)
            x0 += dx
            z.append((x0, y0))
        return z


# Differential function
def func(x: float, y: float) -> float:
    from math import log as ln

    return y * (x * ln(x))


# Main
def main():
    # Inputs
    x0, y0 = 1, 4
    x1 = 2
    iter_count = 10000000

    # Solve
    de = DifferentialEquation(func)
    z = de.eulers_method(x0, x1, y0, iter=iter_count)

    # Print results
    print("Function dy/dx = {}\n".format(de))
    print("Initial  (x0, y0): ({:.3f}, {:.3f})".format(*z[0]))
    print("Final    (x1, y1): ({:.3f}, {:.3f})".format(*z[-1]))
    print(f"Final y value    : {z[-1][1]}")


if __name__ == "__main__":
    main()
