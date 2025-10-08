#!/usr/bin/env python3
"""
Debug der wert() Methode in der Funktion-Klasse
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import Funktion


def debug_wert_methode():
    print("=== Debug: wert() Methode ===")

    f = Funktion("x^2")

    # Test verschiedene x-Werte
    test_werte = [0, 2, sp.Integer(2), sp.Rational(1, 2)]

    for x in test_werte:
        print(f"\nx = {x} (Typ: {type(x)})")
        y = f.wert(x)
        print(f"f.wert(x) = {y} (Typ: {type(y)})")
        print(f"y.is_number: {y.is_number}")
        print(f"y.is_real: {y.is_real}")
        print(f"y.is_finite: {y.is_finite}")

        if hasattr(y, "is_Float"):
            print(f"y.is_Float: {y.is_Float}")
        if isinstance(y, sp.Float):
            print(f"y ist sp.Float: {y}")
        if isinstance(y, float):
            print(f"y ist Python float: {y}")


if __name__ == "__main__":
    import sympy as sp

    debug_wert_methode()
