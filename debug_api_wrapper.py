#!/usr/bin/env python3
"""
Debug-Script für die API Wrapper
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.api import *
from schul_mathematik.analysis.funktion import Funktion


def debug_api_wrapper():
    """Debuggt die API Wrapper Funktionen"""

    print("=== Debug: API Wrapper ===\n")

    # Test 1: API Tangente vs. direkt
    print("1. Test: API Tangente vs. direkt")
    f = ErstellePolynom([1, 0, 0])  # x²

    # API Wrapper
    try:
        api_tangente = Tangente(f, 1)
        print(f"API Tangente: {api_tangente}")
        print(f"API Tangente.term(): {api_tangente.term()}")
        print(f"API Tangente.term_sympy: {api_tangente.term_sympy}")
        print(f"API Tangente(0): {api_tangente(0)}")
        print(f"API Tangente(1): {api_tangente(1)}")
        print(f"Typ: {type(api_tangente)}")
    except Exception as e:
        print(f"API Tangente Fehler: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "-" * 30 + "\n")

    # Direkter Aufruf
    try:
        from schul_mathematik.analysis.taylor import tangente

        direct_tangente = tangente(f, 1)
        print(f"Direkte Tangente: {direct_tangente}")
        print(f"Direkte Tangente.term(): {direct_tangente.term()}")
        print(f"Direkte Tangente.term_sympy: {direct_tangente.term_sympy}")
        print(f"Direkte Tangente(0): {direct_tangente(0)}")
        print(f"Direkte Tangente(1): {direct_tangente(1)}")
        print(f"Typ: {type(direct_tangente)}")
    except Exception as e:
        print(f"Direkte Tangente Fehler: {e}")

    print("\n" + "=" * 50 + "\n")

    # Test 2: API Taylorpolynom vs. direkt
    print("2. Test: API Taylorpolynom vs. direkt")
    g = Funktion("sin(x)")

    # API Wrapper
    try:
        api_taylor = Taylorpolynom(g, grad=3)
        print(f"API Taylorpolynom: {api_taylor}")
        print(f"API Taylorpolynom.term(): {api_taylor.term()}")
        print(f"API Taylorpolynom.term_sympy: {api_taylor.term_sympy}")
        print(f"API Taylorpolynom(0): {api_taylor(0)}")
        print(f"API Taylorpolynom(1): {api_taylor(1)}")
        print(f"Typ: {type(api_taylor)}")
    except Exception as e:
        print(f"API Taylorpolynom Fehler: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "-" * 30 + "\n")

    # Direkter Aufruf
    try:
        from schul_mathematik.analysis.taylor import taylorpolynom

        direct_taylor = taylorpolynom(g, grad=3)
        print(f"Direktes Taylorpolynom: {direct_taylor}")
        print(f"Direktes Taylorpolynom.term(): {direct_taylor.term()}")
        print(f"Direktes Taylorpolynom.term_sympy: {direct_taylor.term_sympy}")
        print(f"Direktes Taylorpolynom(0): {direct_taylor(0)}")
        print(f"Direktes Taylorpolynom(1): {direct_taylor(1)}")
        print(f"Typ: {type(direct_taylor)}")
    except Exception as e:
        print(f"Direktes Taylorpolynom Fehler: {e}")

    print("\n" + "=" * 50 + "\n")

    # Test 3: Funktionstypen vergleichen
    print("3. Test: Funktionstypen vergleichen")
    try:
        f_test = ErstellePolynom([1, 0, 0])
        t_test = Tangente(f_test, 1)

        print(f"f_test Typ: {type(f_test)}")
        print(f"t_test Typ: {type(t_test)}")
        print(
            f"Ist t_test Unterklasse von f_test Typ: {isinstance(t_test, type(f_test))}"
        )

        # Methoden vergleichen
        print(f"f_test hat term(): {hasattr(f_test, 'term')}")
        print(f"t_test hat term(): {hasattr(t_test, 'term')}")
        print(f"f_test hat __call__: {hasattr(f_test, '__call__')}")
        print(f"t_test hat __call__: {hasattr(t_test, '__call__')}")

    except Exception as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    debug_api_wrapper()
