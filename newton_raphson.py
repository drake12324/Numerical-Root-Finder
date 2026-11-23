from polynomial import calculate_polynomial, calculate_derivative


def newton_raphson(coefficients, initial_guess, tolerance, max_iterations):
    x = initial_guess

    for iteration in range(1, max_iterations + 1):
        
        fx = calculate_polynomial(coefficients, x)

        if abs(fx) <= tolerance:
            return x, iteration, True

        derivative = calculate_derivative(coefficients, x)


        if derivative == 0:
            return x, iteration, False

        new_x = x - (fx / derivative)

        if abs(calculate_polynomial(coefficients, new_x)) <= tolerance:
            return new_x, iteration, True


        x = new_x

    return x, max_iterations, False
