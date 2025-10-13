#!/usr/bin/env python3
"""
Debug-Skript für die Exponential-Faktorisierung
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.struktur import _faktorisiere_exponential_summe
import sympy as sp


def debug_exponential_faktorisierung():
    """Debuggt die Exponential-Faktorisierungslogik"""

    print("=== Debug Exponential-Faktorisierung ===\n")

    x = sp.symbols("x")

    test_cases = [
        sp.exp(x) + sp.exp(2 * x),
        sp.exp(2 * x) + sp.exp(x),
        2 * sp.exp(x) + 3 * sp.exp(2 * x),
        sp.exp(x) + sp.exp(x),
        sp.exp(x) + x**2,
    ]

    for expr in test_cases:
        print(f"Teste: {expr}")
        print(f"  Typ: {type(expr)}")
        print(f"  Funktion: {expr.func}")
        print(f"  Args: {expr.args}")

        kann_faktorisiert, gemeinsamer_faktor, rest_faktor = (
            _faktorisiere_exponential_summe(expr, x)
        )
        print(f"  Kann faktorisiert: {kann_faktorisiert}")
        if kann_faktorisiert:
            print(f"  Gemeinsamer Faktor: {gemeinsamer_faktor}")
            print(f"  Rest-Faktor: {rest_faktor}")
            print(f"  Produkt: {gemeinsamer_faktor * rest_faktor}")
            print(
                f"  Gleiches Ergebnis: {sp.simplify(gemeinsamer_faktor * rest_faktor - expr) == 0}"
            )
        print()


if __name__ == "__main__":
    debug_exponential_faktorisierung()
