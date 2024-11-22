class EternityCalculator:
    def manual_sum(self, *args):
        total = 0
        for num in args:
            if not isinstance(num, (int, float)):
                raise TypeError(f"Invalid input: {num}. Expected an integer or float.")
            total += num
        return total

    # Helper function to calculate absolute value manually
    def manual_abs(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid input: {value}. Expected an integer or float.")
        if value < 0:
            return -value
        return value

    def calculate_standard_deviation(self, *args):
        if not args:
            raise ValueError("At least one number is required to calculate standard deviation.")

        # Calculate the mean manually
        total = 0
        count = 0
        for x in args:
            if not isinstance(x, (int, float)):
                raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
            total += x
            count += 1
        mean = total / count

        # Calculate the variance manually
        variance_sum = 0
        for x in args:
            variance_sum += (x - mean) ** 2
        variance = variance_sum / count

        # Calculate square root using a manual method (Newton's method), without abs()
        def sqrt(n):
            if n < 0:
                raise ValueError("Cannot calculate the square root of a negative number.")
            approx = n / 2.0
            better_approx = (approx + n / approx) / 2.0
            while (approx - better_approx) > 0.00001 or (
                    better_approx - approx) > 0.00001:  # Manual check instead of abs()
                approx = better_approx
                better_approx = (approx + n / approx) / 2.0
            return approx

        return sqrt(variance)

    # Gamma function using Lanczos approximation without built-in math functions
    def calculate_gamma(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        if x <= 0 and x == int(x):
            raise ValueError("Gamma function is undefined for non-positive integers.")

        g = 7
        p = [
            0.99999999999980993,
            676.5203681218851,
            -1259.1392167224028,
            771.32342877765313,
            -176.61502916214059,
            12.507343278686905,
            -0.13857109526572012,
            9.9843695780195716e-6,
            1.5056327351493116e-7
        ]

        if x < 0.5:
            return self.custom_pi() / (self.custom_sin(self.custom_pi() * x) * self.calculate_gamma(1 - x))
        else:
            x -= 1
            y = p[0]
            for i in range(1, len(p)):
                y += p[i] / (x + i)
            t = x + g + 0.5
            return self.custom_sqrt(2 * self.custom_pi()) * (t ** (x + 0.5)) * self.custom_exp(-t) * y

    # Mean Absolute Deviation (MAD) function
    def calculate_mad(self, *args):
        if not args:
            raise ValueError("At least one number is required to calculate MAD.")
        mean = self.manual_sum(*args) / len(args)
        absolute_sum = self.manual_sum(*(self.manual_abs(x - mean) for x in args))
        mad = absolute_sum / len(args)
        return mad

    # Logarithm function using the Newton-Raphson method for natural log
    def calculate_logarithm(self, value, base=None):
        if not isinstance(value, (int, float)) or (base is not None and not isinstance(base, (int, float))):
            raise TypeError("Invalid input: Expected integers or floats for value and base.")
        if value <= 0:
            raise ValueError("Logarithm is undefined for non-positive values.")
        if base is not None and (base <= 0 or base == 1):
            raise ValueError("Logarithm base must be positive and not equal to 1.")

        if base is None:
            base = self.custom_e()

        # Calculate the natural logarithm using the Newton-Raphson method
        def natural_logarithm(x):
            if x <= 0:
                raise ValueError("Cannot compute natural logarithm of non-positive values.")
            tolerance = 1e-10
            n = 0
            result = x - 1

            while n < 100:
                exp_result = self.custom_exp(result)
                result -= (exp_result - x) / exp_result
                if self.manual_abs(exp_result - x) < tolerance:
                    break
                n += 1
            return result

        # Calculate logarithm with any base using the change of base formula
        return natural_logarithm(value) / natural_logarithm(base)

    # Exponential function for a * b^x without using built-in power
    def calculate_exponential(self, a, b, x):
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)) or not isinstance(x, (int, float)):
            raise TypeError("Invalid input: Expected integers or floats for a, b, and x.")
        result = a * self.PowerOf(b, x)
        return result

    # Arccos function approximation using Taylor series expansion
    def calculate_arccos(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        if x < -1 or x > 1:
            raise ValueError("Input for arccos must be in the range [-1, 1].")

        # Taylor series approximation of arccos(x) around 0
        result = 0
        term = x
        factor = 1
        n = 0
        while self.manual_abs(term) > 1e-10:
            result += term / (2 * n + 1)
            factor *= (2 * n + 1) / (2 * n + 2)
            term *= (x * x) * factor
            n += 1

        return self.custom_pi() / 2 - result

    # Hyperbolic sine function using approximation of e
    def calculate_hyperbolic_sine(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        e = 2.718281828459045235360287471352
        result = ((e ** x) - e ** (-x)) / 2
        return result

    # Power function without using built-in functions
    def PowerOf(self, base, power):
        if not isinstance(base, (int, float)) or not isinstance(power, (int, float)):
            raise TypeError("Invalid input: Expected integers or floats for base and power.")
        # Handle zero base cases
        if base == 0:
            if power > 0:
                return 0
            else:
                raise ValueError("0 cannot be raised to a non-positive power.")

        # If power is zero, result is 1
        if power == 0:
            return 1

        # If power is an integer
        result = 1
        if power == int(power):
            for _ in range(self.manual_abs(int(power))):
                result *= base
            if power < 0:
                result = 1 / result
        else:
            # For non-integer power, use the exponential and logarithm method
            result = self.custom_exp(power * self.calculate_logarithm(base))
        return result

    # Custom implementations of necessary math functions
    def custom_pi(self):
        return 3.141592653589793

    def custom_e(self):
        return 2.718281828459045

    def custom_sin(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        # Taylor series expansion for sin(x)
        sine = 0
        term = x
        n = 1
        sign = 1
        while self.manual_abs(term) > 1e-10:
            sine += term
            term = -term * x * x / ((2 * n) * (2 * n + 1))
            n += 1
        return sine

    def custom_exp(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        # Taylor series expansion for exp(x)
        result = 1
        term = 1
        n = 1
        while self.manual_abs(term) > 1e-10:
            term *= x / n
            result += term
            n += 1
        return result

    def custom_sqrt(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Invalid input: {x}. Expected an integer or float.")
        # Newton's method for square root
        if x < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        guess = x
        epsilon = 1e-10
        while self.manual_abs(guess * guess - x) > epsilon:
            guess = (guess + x / guess) / 2
        return guess
