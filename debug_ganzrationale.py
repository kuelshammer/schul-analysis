#!/usr/bin/env python3
"""
Debug-Script für die GanzrationaleFunktion Konvertierung
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

import sympy as sp

from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion


def debug_ganzrationale_konvertierung():
    """Debuggt die GanzrationaleFunktion Konvertierung"""

    print("=== Debug: GanzrationaleFunktion Konvertierung ===\n")

    # Test 1: Einfache Ausdrücke
    print("1. Test: Einfache Ausdrücke")

    x = sp.symbols("x")

    # Test-Ausdrücke
    test_exprs = [
        x**2,
        2 * x - 1,
        sp.series(x**2, x, 1, 3).removeO(),  # Taylorpolynom
        sp.series(x**2, x, 1, 2).removeO(),  # Tangente
    ]

    for i, expr in enumerate(test_exprs):
        print(f"\nTest {i + 1}: {expr}")
        try:
            g = GanzrationaleFunktion(expr)
            print(f"  GanzrationaleFunktion.term(): {g.term()}")
            print(f"  GanzrationaleFunktion.term_sympy: {g.term_sympy}")
            print(f"  g(0): {g(0)}")
            print(f"  g(1): {g(1)}")
            print(f"  g(2): {g(2)}")
        except Exception as e:
            print(f"  Fehler: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 50 + "\n")

    # Test 2: Mit String-Eingabe vs. SymPy
    print("2. Test: String-Eingabe vs. SymPy")

    # String-Eingabe
    try:
        g1 = GanzrationaleFunktion("2*x - 1")
        print(f"String '2*x - 1': {g1.term()}")
        print(f"  g1(0): {g1(0)}")
        print(f"  g1(1): {g1(1)}")
    except Exception as e:
        print(f"Fehler bei String: {e}")

    # SymPy-Eingabe
    try:
        expr = 2 * x - 1
        g2 = GanzrationaleFunktion(expr)
        print(f"SymPy 2*x - 1: {g2.term()}")
        print(f"  g2(0): {g2(0)}")
        print(f"  g2(1): {g2(1)}")
    except Exception as e:
        print(f"Fehler bei SymPy: {e}")

    print("\n" + "=" * 50 + "\n")

    # Test 3: Vereinfachung prüfen
    print("3. Test: Vereinfachung prüfen")

    # Taylorpolynom-Ausdruck
    taylor_expr = sp.series(x**2, x, 1, 3).removeO()
    print(f"Taylor-Ausdruck: {taylor_expr}")
    print(f"Vereinfacht: {sp.simplify(taylor_expr)}")
    print(f"Expandiert: {sp.expand(taylor_expr)}")

    # Tangente-Ausdruck
    tangente_expr = sp.series(x**2, x, 1, 2).removeO()
    print(f"\nTangente-Ausdruck: {tangente_expr}")
    print(f"Vereinfacht: {sp.simplify(tangente_expr)}")
    print(f"Expandiert: {sp.expand(tangente_expr)}")

    # Erstelle GanzrationaleFunktion mit vereinfachtem Ausdruck
    try:
        taylor_simplified = sp.simplify(taylor_expr)
        g3 = GanzrationaleFunktion(taylor_simplified)
        print(f"\nVereinfachte GanzrationaleFunktion: {g3.term()}")
        print(f"  g3(0): {g3(0)}")
        print(f"  g3(1): {g3(1)}")
        print(f"  g3(2): {g3(2)}")
    except Exception as e:
        print(f"Fehler bei vereinfachtem Ausdruck: {e}")


if __name__ == "__main__":
    debug_ganzrationale_konvertierung()
