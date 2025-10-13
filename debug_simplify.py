#!/usr/bin/env python3
"""
Debug des sp.simplify Problems
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp


def debug_simplify_issue():
    """Debuggt, ob sp.simplify das Problem verursacht"""

    print("=== Debug sp.simplify Problem ===\n")

    x = sp.symbols("x")
    expr = sp.exp(x) + sp.exp(2 * x)
    print(f"Ausdruck: {expr}")

    term1, term2 = expr.args
    print(f"Term1: {term1}")
    print(f"Term2: {term2}")

    # Exponential-Terme finden
    def ist_exponential_term(term):
        if isinstance(term, sp.Mul):
            for factor in term.args:
                if isinstance(factor, sp.exp):
                    return factor
        elif isinstance(term, sp.exp):
            return term
        return None

    exp1 = ist_exponential_term(term1)
    exp2 = ist_exponential_term(term2)

    print(f"Exponential-Term 1: {exp1}")
    print(f"Exponential-Term 2: {exp2}")

    # Teste mit und ohne simplify
    exp1_arg_raw = exp1.args[0]
    exp2_arg_raw = exp2.args[0]
    exp1_arg_simplified = sp.simplify(exp1.args[0])
    exp2_arg_simplified = sp.simplify(exp2.args[0])

    print(f"Exponent 1 (raw): {exp1_arg_raw}")
    print(f"Exponent 1 (simplified): {exp1_arg_simplified}")
    print(f"Exponent 2 (raw): {exp2_arg_raw}")
    print(f"Exponent 2 (simplified): {exp2_arg_simplified}")

    # Prüfe, ob sie polynomiell sind
    print(f"Exponent 1 raw is_polynomial: {exp1_arg_raw.is_polynomial(x)}")
    print(
        f"Exponent 1 simplified is_polynomial: {exp1_arg_simplified.is_polynomial(x)}"
    )
    print(f"Exponent 2 raw is_polynomial: {exp2_arg_raw.is_polynomial(x)}")
    print(
        f"Exponent 2 simplified is_polynomial: {exp2_arg_simplified.is_polynomial(x)}"
    )

    # Teste Polynom-Erstellung
    try:
        exp1_poly_raw = exp1_arg_raw.as_poly(x)
        exp1_poly_simplified = exp1_arg_simplified.as_poly(x)
        exp2_poly_raw = exp2_arg_raw.as_poly(x)
        exp2_poly_simplified = exp2_arg_simplified.as_poly(x)

        print(f"Exponent 1 raw als Polynom: {exp1_poly_raw}")
        print(f"Exponent 1 simplified als Polynom: {exp1_poly_simplified}")
        print(f"Exponent 2 raw als Polynom: {exp2_poly_raw}")
        print(f"Exponent 2 simplified als Polynom: {exp2_poly_simplified}")

        # Teste Koeffizienten
        print(f"Exponent 1 raw Koeffizienten: {exp1_poly_raw.coeffs()}")
        print(f"Exponent 1 simplified Koeffizienten: {exp1_poly_simplified.coeffs()}")
        print(f"Exponent 2 raw Koeffizienten: {exp2_poly_raw.coeffs()}")
        print(f"Exponent 2 simplified Koeffizienten: {exp2_poly_simplified.coeffs()}")

    except Exception as e:
        print(f"FEHLER bei Polynom-Erstellung: {e}")


if __name__ == "__main__":
    debug_simplify_issue()
