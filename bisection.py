import math


def eval_poly(coeffs, x):
    # Supports cubic [a, b, c, d],
    # quadratic [a, b, c], or linear [a, b]
    if len(coeffs) == 4:
        a, b, c, d = coeffs
        return a * (x ** 3) + b * (x ** 2) + c * x + d
    elif len(coeffs) == 3:
        a, b, c = coeffs
        return a * (x ** 2) + b * x + c
    elif len(coeffs) == 2:
        a, b = coeffs
        return a * x + b
    else:
        raise ValueError("Unsupported number of coefficients.")


def turning_points(coeffs):
    # Repeated roots can occur wheare the derivative is zero.
    if len(coeffs) == 3:
        a, b, c = coeffs
        return [-b / (2 * a)]
    elif len(coeffs) == 4:
        a, b, c, d = coeffs
        # Solve f'(x) = 3ax^2 + 2bx + c = 0.
        discriminant = b ** 2 - 3 * a * c
        if discriminant < 0:
            return []
        return [(-b - math.sqrt(discriminant)) / (3 * a),
                (-b + math.sqrt(discriminant)) / (3 * a)]
    return []


def bisection_method(coeffs, lower, upper, tol, max_iter):
    f_low = eval_poly(coeffs, lower)
    f_high = eval_poly(coeffs, upper)

    # Check if an endpoint is already a root
    if abs(f_low) == 0:
        return {
            "success": True,
            "root": lower,
            "residual": abs(f_low),
            "iterations": 0,
            "reason": "Lower bound is already a root",
            "history": []
        }

    if abs(f_high) == 0:
        return {
            "success": True,
            "root": upper,
            "residual": abs(f_high),
            "iterations": 0,
            "reason": "Upper bound is already a root",
            "history": []
        }

    # Additional root pre-check for same-sign endpoints.
    # This is NOT a standard Bisection iteration: a repeated root
    # may touch the x-axis without changing the sign of f(x).
    if f_low * f_high > 0:
        mid = (lower + upper) / 2.0
        if eval_poly(coeffs, mid) == 0:
            return {
                "success": True,
                "root": mid,
                "residual": 0.0,
                "iterations": 0,
                "reason": "Exact midpoint root found during pre-check",
                "history": []
            }

        for point in turning_points(coeffs):
            if lower < point < upper and eval_poly(coeffs, point) == 0:
                return {
                    "success": True,
                    "root": point,
                    "residual": 0.0,
                    "iterations": 0,
                    "reason": "Exact stationary-point root found during pre-check",
                    "history": []
                }

        # Do not accept an interval just because an extremum is near zero.
        # Keep the standard sign-change requirement if no exact root is found.
        return {
            "success": False,
            "root": None,
            "residual": None,
            "iterations": 0,
            "reason": (
                "Invalid bracket: f(lower) and f(upper) must have opposite signs "
                "unless an exact root is detected. Try different bounds or "
                "Newton-Raphson. This does not prove that no real root exists."
            ),
            "history": []
        }

    low = float(lower)
    high = float(upper)
    history = []
    mid = low
    f_mid = eval_poly(coeffs, mid)
    reason = "Maximum iterations reached"

    for i in range(1, max_iter + 1):
        mid = (low + high) / 2.0
        f_mid = eval_poly(coeffs, mid)
        f_low = eval_poly(coeffs, low)

        row = {
            "iter": i,
            "lower": low,
            "upper": high,
            "mid": mid,
            "f_mid": f_mid
        }
        history.append(row)

        # Stop if exact root or within tolerance
        if (
            f_mid == 0
            or abs(f_mid) <= tol
            or (high - low) / 2.0 <= tol
        ):
            if f_mid == 0:
                reason = "Exact root found"
            elif abs(f_mid) <= tol:
                reason = "Tolerance met (|f(mid)| <= tol)"
            else:
                reason = "Tolerance met (half-interval <= tol)"
            break

        # Update bracket half
        if f_low * f_mid < 0:
            high = mid
        else:
            low = mid

    return {
        "success": reason != "Maximum iterations reached",
        "root": mid,
        "residual": abs(f_mid),
        "iterations": len(history),
        "reason": reason,
        "history": history
    }


def print_bisection_report(result):
    if not result["success"] and result["root"] is None:
        print("\nCould not run Bisection Method:", result["reason"])
        return

    print("\n--- ITERATION TABLE ---")
    print("Iter | Lower      | Upper      | Midpoint   | f(Midpoint)")
    print("-" * 58)

    for step in result["history"]:
        print(
            f"{step['iter']:<4} | "
            f"{step['lower']:<10.6f} | "
            f"{step['upper']:<10.6f} | "
            f"{step['mid']:<10.6f} | "
            f"{step['f_mid']:<11.6f}"
        )

    print("\n--- BISECTION RESULT ---")
    print("Approximate root:", result["root"])
    print("Residual |f(x)|:", result["residual"])
    print("Iterations:", result["iterations"])
    print("Stopped by:", result["reason"])
    print("Status:", "Successful" if result["success"] else "Unsuccessful")
