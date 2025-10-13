#!/usr/bin/env python3
"""
Debug script to understand why exp(x) + exp(2x) is not properly recognized
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.struktur import analysiere_funktionsstruktur
from schul_mathematik.analysis.funktion import Funktion
import sympy as sp


def test_exponential_structure():
    """Test the structure analysis for exp(x) + exp(2*x)"""

    print("=== Testing structure analysis for exp(x) + exp(2*x) ===")

    # Test with raw SymPy
    x = sp.symbols("x")
    expr = sp.exp(x) + sp.exp(2 * x)
    print(f"Raw SymPy expression: {expr}")
    print(f"Expression type: {type(expr)}")
    print(f"Expression func: {expr.func}")
    print(f"Expression args: {expr.args}")

    # Test with string input
    print(f"\n=== String input: 'exp(x) + exp(2*x)' ===")
    result = analysiere_funktionsstruktur("exp(x) + exp(2*x)")
    print(f"Structure: {result['struktur']}")
    print(f"Components: {[(k['term'], k['typ']) for k in result['komponenten']]}")

    # Test with Funktion input
    print(f"\n=== Funktion input ===")
    f = Funktion("exp(x) + exp(2*x)")
    print(f"Funktion type: {type(f)}")
    print(f"Term: {f.term()}")
    print(f"Struktur info available: {hasattr(f, '_struktur_info')}")
    if hasattr(f, "_struktur_info"):
        print(f"Structure: {f._struktur_info['struktur']}")
        print(
            f"Components: {[(k['term'], k['typ']) for k in f._struktur_info['komponenten']]}"
        )

    # Test with raw SymPy input
    print(f"\n=== Raw SymPy input ===")
    result_sympy = analysiere_funktionsstruktur(expr)
    print(f"Structure: {result_sympy['struktur']}")
    print(f"Components: {[(k['term'], k['typ']) for k in result_sympy['komponenten']]}")


if __name__ == "__main__":
    test_exponential_structure()
