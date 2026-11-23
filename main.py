import math
from newton_raphson import newton_raphson
from bisection import bisection_method, print_bisection_report


def get_number(message):
    while True:
        try:
            number = float(input(message))

            if math.isfinite(number):
                return number

            print("Please enter a finite number.")

        except ValueError:
            print("Please enter a valid number.")



def get_integer(message):
    while True:
        try:
            number = int(input(message))
            if number > 0:
                return number
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a valid whole number.")


def main():
    while True:
        print("\n==============================")
        print("     NUMERICAL ROOT FINDER")
        print("==============================")
        print("1. Bisection Method")
        print("2. Newton-Raphson Method")
        print("3. Exit")

        method = input("\nChoose a method: ")

        if method == "3":
            print("Thank you for using Numerical Root Finder!")
            break

        if method not in ["1", "2"]:
            print("Invalid choice. Please try again.")
            continue

        print("\nChoose Equation Degree")
        print("1. Linear")
        print("2. Quadratic")
        print("3. Cubic")

        degree_choice = input("Choose degree: ")

        if degree_choice not in ["1", "2", "3"]:
            print("Invalid equation degree.")
            continue

        degree = int(degree_choice)

        if degree == 1:
            labels = ["a", "b"]
        elif degree == 2:
            labels = ["a", "b", "c"]
        else:
            labels = ["a", "b", "c", "d"]

        coefficients = []

        print("\nEnter the polynomial coefficients:")

        for label in labels:
            value = get_number("Enter " + label + ": ")
            coefficients.append(value)

        print("\nEnter calculation settings:")

        tolerance = get_number("Enter tolerance: ")
        max_iterations = get_integer("Maximum iterations: ")

        if tolerance <= 0:
            print("Tolerance must be greater than zero.")
            continue

        if method == "1":
            print("\nBisection Method selected.")
            lower = get_number("Enter lower bound: ")
            upper = get_number("Enter upper bound: ")

            if lower >= upper:
                print("Upper bound must be greater than lower bound.")
                continue

        elif method == "2":
            print("\nNewton-Raphson Method selected.")
            initial_guess = get_number("Enter initial guess: ")

        print("\n========== INPUT SUMMARY ==========")
        print("Equation degree:", degree)
        print("Coefficients:", coefficients)
        print("Tolerance:", tolerance)
        print("Maximum iterations:", max_iterations)

        if method == "1":
            print("Lower bound:", lower)
            print("Upper bound:", upper)

            result = bisection_method(
                coefficients,
                lower,
                upper,
                tolerance,
                max_iterations
            )

            print_bisection_report(result)

        elif method == "2":
            print("Initial guess:", initial_guess)

            root, iterations, converged = newton_raphson(
                coefficients,
                initial_guess,
                tolerance,
                max_iterations
            )

            print("\n========== NEWTON-RAPHSON RESULT ==========")
            print("Estimated Root:", root)
            print("Iterations:", iterations)

            if converged:
                print("Status: Converged")
            else:
                print("Status: Did not converge")


if __name__ == "__main__":
    main()
