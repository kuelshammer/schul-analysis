#!/usr/bin/env python3
"""Test exact arithmetic implementation."""

from schul_analysis.ganzrationale import GanzrationaleFunktion
import sympy as sp


def test_exact_arithmetic():
    print("=== Test Exakte Arithmetik ===")

    # Test 1: Einfache rationale Zahlen
    print("\n1. Teste rationale Koeffizienten:")
    f1 = GanzrationaleFunktion([sp.Rational(1, 6), sp.Rational(1, 6), 0])
    print(f"f1(x) = {f1.term()}")
    print(f"f1.koeffizienten = {f1.koeffizienten}")
    print(f"f1.wert(1) = {f1.wert(1)} (sollte 1/6 + 1/6 = 1/3 sein)")

    # Test 2: Konstruktor mit Strings
    print("\n2. Teste String-Konstruktor:")
    f2 = GanzrationaleFunktion("1/6*x + 1/6")
    print(f"f2(x) = {f2.term()}")
    print(f"f2.koeffizienten = {f2.koeffizienten}")
    print(f"f2.wert(1) = {f2.wert(1)}")

    # Test 3: Linearfaktoren mit exakten Koeffizienten
    print("\n3. Teste Linearfaktoren:")
    f3 = GanzrationaleFunktion("(x-1/2)(x+1/3)")
    print(f"f3(x) = {f3.term()}")
    print(f"f3.koeffizienten = {f3.koeffizienten}")
    print(f"f3.wert(0) = {f3.wert(0)} (sollte -1/6 sein)")

    # Test 4: Berechnungen mit exakten Ergebnissen
    print("\n4. Teste exakte Berechnungen:")
    f4 = GanzrationaleFunktion(
        [sp.Rational(1, 3), 0, sp.Rational(-1, 3)]
    )  # (1/3)x² - 1/3
    print(f"f4(x) = {f4.term()}")
    nullstellen = f4.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 5: Ableitungen mit exakten Koeffizienten
    print("\n5. Teste Ableitungen:")
    f5 = GanzrationaleFunktion(
        [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)]
    )
    print(f"f5(x) = {f5.term()}")
    f5_abl = f5.ableitung()
    print(f"f5'(x) = {f5_abl.term()}")
    print(f"f5'.koeffizienten = {f5_abl.koeffizienten}")


if __name__ == "__main__":
    test_exact_arithmetic()
