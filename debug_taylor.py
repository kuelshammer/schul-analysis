#!/usr/bin/env python3
"""
Debug-Script für Taylorpolynom und Tangente
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp

from schul_mathematik.analysis.api import *
from schul_mathematik.analysis.funktion import Funktion
from schul_mathematik.analysis.taylor import tangente, taylorpolynom


def debug_taylor_tangente():
    """Debuggt die Taylorpolynom und Tangente Funktionen"""

    print("=== Debug: Taylorpolynom und Tangente ===\n")

    # Test 1: Direkte SymPy Berechnung
    print("1. Test: Direkte SymPy Berechnung")
    x = sp.symbols("x")
    f_expr = x**2

    # Taylorpolynom berechnen
    taylor_expr = sp.series(f_expr, x, 1, 3).removeO()
    print(f"SymPy Taylorpolynom: {taylor_expr}")
    print(f"Typ: {type(taylor_expr)}")

    # Tangente berechnen
    tangente_expr = sp.series(f_expr, x, 1, 2).removeO()
    print(f"SymPy Tangente: {tangente_expr}")
    print(f"Typ: {type(tangente_expr)}")

    print("\n" + "=" * 50 + "\n")

    # Test 2: Taylorpolynom Funktion direkt aufrufen
    print("2. Test: Taylorpolynom Funktion direkt")
    try:
        f = Funktion("x^2")
        print(f"Funktion f.term(): {f.term()}")
        print(f"Funktion f.term_sympy: {f.term_sympy}")

        # Direkter Aufruf der taylorpolynom Funktion
        result = taylorpolynom(f, grad=2, entwicklungspunkt=1)
        print(f"Taylorpolynom Ergebnis: {result}")
        print(f"Taylorpolynom.term(): {result.term()}")
        print(f"Taylorpolynom.term_sympy: {result.term_sympy}")

    except Exception as e:
        print(f"Fehler: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 50 + "\n")

    # Test 3: Tangente Funktion direkt aufrufen
    print("3. Test: Tangente Funktion direkt")
    try:
        f = Funktion("x^2")
        print(f"Funktion f.term(): {f.term()}")
        print(f"Funktion f.term_sympy: {f.term_sympy}")

        # Direkter Aufruf der tangente Funktion
        result = tangente(f, 1)
        print(f"Tangente Ergebnis: {result}")
        print(f"Tangente.term(): {result.term()}")
        print(f"Tangente.term_sympy: {result.term_sympy}")

    except Exception as e:
        print(f"Fehler: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 50 + "\n")

    # Test 4: GanzrationaleFunktion direkt testen
    print("4. Test: GanzrationaleFunktion direkt")
    try:
        from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion

        # Test mit verschiedenen Ausdrücken
        test_expr = sp.sympify("2*x - 1")
        print(f"Test-Ausdruck: {test_expr}")

        g = GanzrationaleFunktion(test_expr)
        print(f"GanzrationaleFunktion.term(): {g.term()}")
        print(f"GanzratigeFunktion(0): {g(0)}")
        print(f"GanzratigeFunktion(1): {g(1)}")

        # Mit Taylorpolynom Ausdruck
        taylor_test = sp.series(x**2, x, 1, 3).removeO()
        print(f"Taylor-Ausdruck: {taylor_test}")

        g2 = GanzrationaleFunktion(taylor_test)
        print(f"GanzrationaleFunktion(Taylor).term(): {g2.term()}")
        print(f"GanzratigeFunktion(Taylor)(0): {g2(0)}")
        print(f"GanzratigeFunktion(Taylor)(1): {g2(1)}")
        print(f"GanzratigeFunktion(Taylor)(2): {g2(2)}")

    except Exception as e:
        print(f"Fehler: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_taylor_tangente()
