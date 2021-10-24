class Polynomial:
    def __init__(self, terms: list[float]):
        self.terms: list[float] = terms
        self._terms_prime: list[float] = []
        self.get_derivative()

    def __str__(self) -> str:
        out: list[str] = []

        # Get each term
        for i in range(len(self.terms)):
            out.append(f"{self.terms[i]}*x^{i}")

        # Put the terms in order and join them
        out.reverse()
        return " + ".join(out)

    def get_derivative(self):
        terms: list[float] = []

        # Apply the power rule for each term
        for i in range(0, len(self.terms)):
            terms.append(self.terms[i] * i)

        # Set the derrivative
        self._terms_prime = terms[1:]
        print(self.terms)
        print(self._terms_prime)

    def f(self, x: float, derrivative: bool = False) -> float:
        # Decide polynomial
        terms = self.terms
        if derrivative:
            terms = self._terms_prime

        # Accumulator
        sum: float = 0

        # Add each term and multiply the coefficient
        for i in range(len(terms)):
            sum += terms[i] * pow(x, i)
        return sum


def main():
    # Get polynomial
    polynomial = get_polynomial()
    print(f"\nf(x) = {polynomial}\n")

    # Get x value
    x = get_x_value()

    # Get intercept
    intercept = newtons_method(polynomial, x)

    # Print intercept
    print(f"f({intercept:.8}) = {polynomial.f(round(intercept, 8)):.8}")


def get_polynomial() -> Polynomial:
    # Instructions
    print("Enter each term in order from largest to smallest degree.")
    print('Enter "finish"/"f" to finish the polynomial.')
    terms: list[float] = []

    # Enter loop
    while True:

        # Get input
        next_term: str = input("Enter term: ")

        # Check for exit code
        if next_term in ("finish", "f"):

            # Form final polynomial
            terms.reverse()
            polynomial = Polynomial(terms)
            break

        # Convert input
        try:

            terms.append(float(next_term))
        except ValueError:
            print("Improper input, try again.\n")
            continue

    # Return formed polynomial
    return polynomial


def get_x_value() -> float:
    # Enter loop
    while True:
        try:
            # Try to convert the input
            return float(input("Enter x coordinate: "))
        except ValueError:
            print("Invalid value, try again.")


def newtons_method(polynomial: Polynomial, x: float) -> float:
    for _ in range(10000):
        # Get value and slope
        y = polynomial.f(x)
        y_prime = polynomial.f(x, True)

        # Get next x value
        x -= y / y_prime

    # Return coords of the guessed intercept
    return x


if __name__ == "__main__":
    main()
