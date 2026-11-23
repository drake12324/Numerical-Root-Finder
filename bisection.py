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

    # Check if signs are opposite (Bolzano / bracket check)
    if f_low * f_high > 0:
        return {
            "success": False,
            "root": None,
            "residual": None,
            "iterations": 0,
            "reason": "Invalid bracket: f(lower) and f(upper) must have opposite signs",
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
