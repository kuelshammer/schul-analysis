#!/usr/bin/env python3
"""
Debug des spezifischen Problems mit len(expr.args)
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp


def debug_len_args():
    """Debuggt das Problem mit len(expr.args)"""

    print("=== Debug len(expr.args) Problem ===\n")

    x = sp.symbols("x")
    expr = sp.exp(x) + sp.exp(2 * x)

    print(f"Ausdruck: {expr}")
    print(f"Typ: {type(expr)}")
    print(f"Funktion: {expr.func}")
    print(f"Args: {expr.args}")
    print(f"Len(args): {len(expr.args)}")
    print(f"Type von args: {type(expr.args)}")

    # Teste die Bedingung
    bedingung1 = isinstance(expr, sp.Add)
    bedingung2 = len(expr.args) != 2

    print(f"ist isinstance(expr, sp.Add): {bedingung1}")
    print(f"ist len(expr.args) != 2: {bedingung2}")
    print(f"Komplette Bedingung: {not bedingung1 or bedingung2}")

    # Teste mit manuell erstelltem Ausdruck
    print(f"\n=== Test mit manuell erstelltem Ausdruck ===")
    manual_expr = sp.Add(sp.exp(x), sp.exp(2 * x))
    print(f"Manueller Ausdruck: {manual_expr}")
    print(f"Typ: {type(manual_expr)}")
    print(f"Args: {manual_expr.args}")
    print(f"Len(args): {len(manual_expr.args)}")

    # Teste den direkten Import
    print(f"\n=== Test mit importierter Funktion ===")
    from schul_mathematik.analysis.struktur import _faktorisiere_exponential_summe

    result = _faktorisiere_exponential_summe(expr, x)
    print(f"Ergebnis: {result}")


if __name__ == "__main__":
    debug_len_args()
