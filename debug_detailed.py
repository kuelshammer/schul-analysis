#!/usr/bin/env python3
"""
Detailliertes Debug-Skript für die Exponential-Faktorisierung
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp


def debug_faktorisierung_step_by_step():
    """Debuggt die Faktorisierung Schritt für Schritt"""

    print("=== Debug Faktorisierung Schritt für Schritt ===\n")

    x = sp.symbols("x")

    # Testfall: exp(x) + exp(2*x)
    expr = sp.exp(x) + sp.exp(2 * x)
    print(f"Original Ausdruck: {expr}")

    # Schritt 1: Prüfe, ob es eine Summe mit 2 Termen ist
    if not isinstance(expr, sp.Add) or len(expr.args) != 2:
        print(f"  Keine Summe mit 2 Termen")
        return

    term1, term2 = expr.args
    print(f"  Term1: {term1}")
    print(f"  Term2: {term2}")

    # Schritt 2: Prüfe auf Exponential-Terme
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

    print(f"  Exponential-Term 1: {exp1}")
    print(f"  Exponential-Term 2: {exp2}")

    if exp1 is None or exp2 is None:
        print(f"  Nicht beide Terme sind Exponential-Terme")
        return

    # Schritt 3: Extrahiere Exponenten
    exp1_arg = exp1.args[0]
    exp2_arg = exp2.args[0]

    print(f"  Exponent 1: {exp1_arg}")
    print(f"  Exponent 2: {exp2_arg}")

    # Schritt 4: Prüfe, ob Exponenten polynomiell sind
    if not (exp1_arg.is_polynomial(x) and exp2_arg.is_polynomial(x)):
        print(f"  Nicht beide Exponenten sind polynomiell")
        return

    print(f"  Beide Exponenten sind polynomiell")

    # Schritt 5: Extrahiere Koeffizienten
    exp1_poly = exp1_arg.as_poly(x)
    exp2_poly = exp2_arg.as_poly(x)

    print(f"  Polynom 1: {exp1_poly}")
    print(f"  Polynom 2: {exp2_poly}")
    print(f"  Grad 1: {exp1_poly.degree()}")
    print(f"  Grad 2: {exp2_poly.degree()}")

    if exp1_poly.degree() != 1 or exp2_poly.degree() != 1:
        print(f"  Nicht beide sind linear")
        return

    koeff1 = exp1_poly.coeffs()[0]
    koeff2 = exp2_poly.coeffs()[0]

    print(f"  Koeffizient 1: {koeff1}")
    print(f"  Koeffizient 2: {koeff2}")

    # Schritt 6: Prüfe konstante Terme
    const1 = exp1_poly.coeffs()[1] if len(exp1_poly.coeffs()) > 1 else 0
    const2 = exp2_poly.coeffs()[1] if len(exp2_poly.coeffs()) > 1 else 0

    print(f"  Konstante 1: {const1}")
    print(f"  Konstante 2: {const2}")

    if const1 != 0 or const2 != 0:
        print(f"  Konstante Terme sind nicht 0")
        return

    print(f"  Alle Prüfungen bestanden - kann faktorisiert werden!")

    # Schritt 7: Faktorisierung
    if koeff1 == koeff2:
        print(f"  Gleiche Koeffizienten - keine Faktorisierung nötig")
        return

    if abs(koeff1) < abs(koeff2):
        kleiner_koeff = koeff1
        diff_koeff = koeff2 - koeff1
        print(f"  Kleinerer Koeffizient: {kleiner_koeff}")
        print(f"  Differenz: {diff_koeff}")
    else:
        kleiner_koeff = koeff2
        diff_koeff = koeff1 - koeff2
        print(f"  Kleinerer Koeffizient: {kleiner_koeff}")
        print(f"  Differenz: {diff_koeff}")

    # Extrahiere Vorfaktoren
    def extrahiere_vorfaktor(term, exp_factor):
        if isinstance(term, sp.Mul):
            other_factors = [f for f in term.args if f != exp_factor]
            if other_factors:
                return sp.Mul(*other_factors)
            else:
                return sp.Integer(1)
        else:
            return sp.Integer(1)

    vorfaktor1 = extrahiere_vorfaktor(term1, exp1)
    vorfaktor2 = extrahiere_vorfaktor(term2, exp2)

    print(f"  Vorfaktor 1: {vorfaktor1}")
    print(f"  Vorfaktor 2: {vorfaktor2}")

    # Erstelle Faktoren
    gemeinsamer_exp = sp.exp(kleiner_koeff * x)
    rest_exp = sp.exp(diff_koeff * x) if diff_koeff > 0 else sp.exp(-diff_koeff * x)
    rest_faktor = vorfaktor1 + vorfaktor2 * rest_exp

    print(f"  Gemeinsamer Exp-Faktor: {gemeinsamer_exp}")
    print(f"  Rest-Exp: {rest_exp}")
    print(f"  Rest-Faktor: {rest_faktor}")
    print(f"  Produkt: {gemeinsamer_exp * rest_faktor}")
    print(f"  Gleichheit: {sp.simplify(gemeinsamer_exp * rest_faktor - expr) == 0}")


if __name__ == "__main__":
    debug_faktorisierung_step_by_step()
