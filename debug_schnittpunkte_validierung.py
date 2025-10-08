#!/usr/bin/env python3
"""
Debug script to understand why Schnittpunkte validation is failing
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import Funktion


def debug_schnittpunkte():
    print("=== Debug: Schnittpunkte-Validierung ===")

    # Test: Einfache Funktionen
    f = Funktion("x^2")
    g = Funktion("2*x")

    print(f"f.term_sympy: {f.term_sympy}")
    print(f"g.term_sympy: {g.term_sympy}")
    print(f"f.term_sympy type: {type(f.term_sympy)}")
    print(f"g.term_sympy type: {type(g.term_sympy)}")

    # Manuelle Berechnung wie in der Methode
    import sympy as sp

    gleichung = sp.Eq(f.term_sympy, g.term_sympy)
    print(f"Gleichung: {gleichung}")

    x_loesungen = sp.solve(gleichung, f._variable_symbol)
    print(f"Lösungen: {x_loesungen}")
    print(f"Lösungen Typen: {[type(x) for x in x_loesungen]}")

    # Test y-Wert Berechnung
    for x_loesung in x_loesungen:
        print(f"\nFür x = {x_loesung} (Typ: {type(x_loesung)}):")
        y_wert = f.wert(x_loesung)
        print(f"y = {y_wert} (Typ: {type(y_wert)})")

        # Prüfe auf Float
        print(f"y.is_number: {y_wert.is_number}")
        print(f"y.is_real: {y_wert.is_real}")
        print(f"y.is_finite: {y_wert.is_finite}")

        # Prüfe auf Approximation
        if hasattr(y_wert, "is_Float") and y_wert.is_Float:
            print(f"y ist Float: {y_wert}")
        if isinstance(y_wert, sp.Float):
            print(f"y ist sp.Float: {y_wert}")


if __name__ == "__main__":
    debug_schnittpunkte()
