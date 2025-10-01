#!/usr/bin/env python3
"""Demonstrate precision improvement with exact arithmetic."""

from schul_analysis.ganzrationale import GanzrationaleFunktion
import sympy as sp


def demonstrate_precision():
    print("=== Demonstration der Präzisionsverbesserung ===")

    # Test mit 1/6 + 1/6 = 1/3 (exakt)
    print("\n1. Problem: 1/6 + 1/6 = 1/3")
    print(
        "Mit Float-Arithmetik: 0.16666666666666666 + 0.16666666666666666 =",
        0.16666666666666666 + 0.16666666666666666,
    )
    print("Exakt: 1/6 + 1/6 =", sp.Rational(1, 6) + sp.Rational(1, 6))

    f = GanzrationaleFunktion([sp.Rational(1, 6), sp.Rational(1, 6), 0])
    print(f"Unsere Implementation: f(1) = {f.wert(1)}")
    print(f"Koeffizienten sind exakt: {f.koeffizienten}")

    # Test mit komplexeren Berechnungen
    print("\n2. Komplexere Berechnung: (x²-2)(x+1/2)")
    f_complex = GanzrationaleFunktion("(x^2-2)(x+1/2)")
    print(f"f(x) = {f_complex.term()}")
    print(f"Koeffizienten: {f_complex.koeffizienten}")

    # Wert an irrationaler Stelle
    print(f"f(√2) = {f_complex.wert(sp.sqrt(2))}")
    print("(sollte exakt 0 sein, da √2 eine Nullstelle von x²-2 ist)")

    # Test mit Ableitungen
    print("\n3. Ableitungen mit exakten Koeffizienten:")
    f_poly = GanzrationaleFunktion(
        [sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(1, 5)]
    )
    print(f"f(x) = {f_poly.term()}")

    for i in range(1, 4):
        ableitung = f_poly.ableitung(i)
        print(f"f^{i}(x) = {ableitung.term()}")
        print(f"Koeffizienten: {ableitung.koeffizienten}")


if __name__ == "__main__":
    demonstrate_precision()
