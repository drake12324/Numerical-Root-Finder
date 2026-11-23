def calculate_polynomial(coefficients, x):
    result = 0

    for coefficient in coefficients:
        result = result * x + coefficient

    return result

def calculate_derivative(coefficients, x):
    degree = len(coefficients) - 1
    derivative_coefficients = []

    for i in range(degree):
        derivative_coefficients.append(coefficients[i] * (degree - i))

    result = 0

    for coefficient in derivative_coefficients:
        result = result * x + coefficient

    return result