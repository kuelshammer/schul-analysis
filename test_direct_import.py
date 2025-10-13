#!/usr/bin/env python3
"""
Direkter Test der Funktion aus dem Modul
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.struktur import _faktorisiere_exponential_summe
import sympy as sp


def test_direct_import():
    """Testet die direkt importierte Funktion"""

    print("=== Teste direkt importierte Funktion ===\n")

    x = sp.symbols("x")
    expr = sp.exp(x) + sp.exp(2 * x)
    print(f"Ausdruck: {expr}")

    # Rufe die Funktion direkt auf
    result = _faktorisiere_exponential_summe(expr, x)
    print(f"Ergebnis: {result}")

    # Teste mit verschiedenen Ausdrücken
    test_exprs = [
        sp.exp(x) + sp.exp(2 * x),
        sp.exp(2 * x) + sp.exp(x),
        sp.exp(3 * x) + sp.exp(5 * x),
        2 * sp.exp(x) + 3 * sp.exp(2 * x),
    ]

    for test_expr in test_exprs:
        print(f"\nTeste: {test_expr}")
        kann_faktorisiert, gemeinsamer_faktor, rest_faktor = (
            _faktorisiere_exponential_summe(test_expr, x)
        )
        print(f"  Kann faktorisiert: {kann_faktorisiert}")
        if kann_faktorisiert:
            print(f"  Gemeinsamer Faktor: {gemeinsamer_faktor}")
            print(f"  Rest-Faktor: {rest_faktor}")


if __name__ == "__main__":
    test_direct_import()
