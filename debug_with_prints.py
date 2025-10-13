#!/usr/bin/env python3
"""
Kopiert die Funktion mit echten Prints
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp


def _faktorisiere_exponential_summe_mit_prints(expr: sp.Basic, variable: sp.Symbol):
    """
    Kopie der Funktion mit Prints zum Debuggen
    """
    print(f"=== _faktorisiere_exponential_summe_mit_prints ===")
    print(f"Expr: {expr}")
    print(f"Variable: {variable}")

    if not isinstance(expr, sp.Add) or len(expr.args) != 2:
        print(
            f"  FEHLER: Keine Summe mit 2 Termen - ist {type(expr)} mit {len(expr.args) if hasattr(expr, 'args') else 'keine'} Argumenten"
        )
        return False, expr, sp.Integer(1)

    term1, term2 = expr.args
    print(f"  Term1: {term1} (Typ: {type(term1)})")
    print(f"  Term2: {term2} (Typ: {type(term2)})")

    # Prüfe, ob beide Terme Exponentialfunktionen sind
    def ist_exponential_term(term):
        print(f"    Prüfe Term: {term}")
        if isinstance(term, sp.Mul):
            print(f"    Ist Mul - Faktoren: {term.args}")
            for factor in term.args:
                if isinstance(factor, sp.exp):
                    print(f"      >>> Exponential-Faktor gefunden: {factor}")
                    return factor
        elif isinstance(term, sp.exp):
            print(f"    >>> Reiner Exponential-Term")
            return term
        print(f"    >>> Kein Exponential-Term")
        return None

    exp1 = ist_exponential_term(term1)
    exp2 = ist_exponential_term(term2)

    print(f"  Exponential-Term 1: {exp1}")
    print(f"  Exponential-Term 2: {exp2}")

    if exp1 is None or exp2 is None:
        print(f"  FEHLER: Nicht beide Terme sind Exponential-Terme")
        return False, expr, sp.Integer(1)

    # Extrahiere die Exponenten
    try:
        print(f"  Versuche Exponenten zu extrahieren...")
        exp1_arg = sp.simplify(exp1.args[0])
        exp2_arg = sp.simplify(exp2.args[0])

        print(f"  Exponent 1: {exp1_arg}")
        print(f"  Exponent 2: {exp2_arg}")

        # Prüfe, ob die Exponenten lineare Ausdrücke der Variable sind
        if not (exp1_arg.is_polynomial(variable) and exp2_arg.is_polynomial(variable)):
            print(f"  FEHLER: Nicht beide Exponenten sind polynomiell")
            return False, expr, sp.Integer(1)

        print(f"  Beide Exponenten sind polynomiell")

        # Extrahiere die Koeffizienten
        exp1_poly = exp1_arg.as_poly(variable)
        exp2_poly = exp2_arg.as_poly(variable)

        print(f"  Polynom 1: {exp1_poly}")
        print(f"  Polynom 2: {exp2_poly}")
        print(f"  Grad 1: {exp1_poly.degree()}")
        print(f"  Grad 2: {exp2_poly.degree()}")

        if exp1_poly.degree() != 1 or exp2_poly.degree() != 1:
            print(f"  FEHLER: Nicht beide sind linear")
            return False, expr, sp.Integer(1)

        print(f"  Beide sind linear")

        koeff1 = exp1_poly.coeffs()[0]  # Koeffizient von x
        koeff2 = exp2_poly.coeffs()[0]  # Koeffizient von x

        print(f"  Koeffizient 1: {koeff1}")
        print(f"  Koeffizient 2: {koeff2}")

        # Prüfe, ob die Konstante Terme 0 sind (keine Addition im Exponenten)
        const1 = exp1_poly.coeffs()[1] if len(exp1_poly.coeffs()) > 1 else 0
        const2 = exp2_poly.coeffs()[1] if len(exp2_poly.coeffs()) > 1 else 0

        print(f"  Konstante 1: {const1}")
        print(f"  Konstante 2: {const2}")

        if const1 != 0 or const2 != 0:
            print(f"  FEHLER: Konstante Terme sind nicht 0")
            return False, expr, sp.Integer(1)

        print(f"  Alle Konstanten sind 0")

        # Bestimme den gemeinsamen Faktor (kleinerer Koeffizient)
        if koeff1 == koeff2:
            print(f"  Gleiche Koeffizienten - keine Faktorisierung nötig")
            return False, expr, sp.Integer(1)

        print(f"  Koeffizienten sind unterschiedlich - kann faktorisieren!")

        # Finde den kleineren Koeffizienten für den gemeinsamen Faktor
        if abs(koeff1) < abs(koeff2):
            kleiner_koeff = koeff1
            diff_koeff = koeff2 - koeff1
            term_mit_kleinerem_koeff = term1
            term_mit_größerem_koeff = term2
        else:
            kleiner_koeff = koeff2
            diff_koeff = koeff1 - koeff2
            term_mit_kleinerem_koeff = term2
            term_mit_größerem_koeff = term1

        print(f"  Kleinerer Koeffizient: {kleiner_koeff}")
        print(f"  Differenz: {diff_koeff}")

        # Extrahiere die Vorfaktoren
        def extrahiere_vorfaktor(term, exp_factor):
            if isinstance(term, sp.Mul):
                # Baue einen neuen Term ohne den exp-Faktor
                other_factors = [f for f in term.args if f != exp_factor]
                if other_factors:
                    return sp.Mul(*other_factors)
                else:
                    return sp.Integer(1)
            else:
                return sp.Integer(1)

        vorfaktor1 = extrahiere_vorfaktor(
            term_mit_kleinerem_koeff, exp1 if koeff1 == kleiner_koeff else exp2
        )
        vorfaktor2 = extrahiere_vorfaktor(
            term_mit_größerem_koeff, exp2 if koeff2 > koeff1 else exp1
        )

        print(f"  Vorfaktor 1: {vorfaktor1}")
        print(f"  Vorfaktor 2: {vorfaktor2}")

        # Erstelle den gemeinsamen Exponential-Faktor
        gemeinsamer_exp = sp.exp(kleiner_koeff * variable)

        # Erstelle den Rest-Faktor
        if diff_koeff > 0:
            rest_exp = sp.exp(diff_koeff * variable)
        else:
            rest_exp = sp.exp(-diff_koeff * variable)

        rest_faktor = vorfaktor1 + vorfaktor2 * rest_exp

        print(f"  Gemeinsamer Exp-Faktor: {gemeinsamer_exp}")
        print(f"  Rest-Exp: {rest_exp}")
        print(f"  Rest-Faktor: {rest_faktor}")
        print(f"  Produkt: {gemeinsamer_exp * rest_faktor}")

        # Prüfe die Gleichheit
        diff = sp.simplify(gemeinsamer_exp * rest_faktor - expr)
        print(f"  Differenz: {diff}")
        print(f"  Ist gleich: {diff == 0}")

        return True, gemeinsamer_exp, rest_faktor

    except Exception as e:
        print(f"  FEHLER in der Berechnung: {e}")
        import traceback

        traceback.print_exc()
        return False, expr, sp.Integer(1)


def test_mit_prints():
    """Testet die Funktion mit Prints"""

    x = sp.symbols("x")
    expr = sp.exp(x) + sp.exp(2 * x)
    print(f"Test-Ausdruck: {expr}")

    result = _faktorisiere_exponential_summe_mit_prints(expr, x)
    print(f"\nEndergebnis: {result}")


if __name__ == "__main__":
    test_mit_prints()
