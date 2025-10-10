#!/usr/bin/env python3
"""
Test der korrigierten Implementierung für sin(x) + cos(x) = 0
"""

from src.schul_mathematik.analysis.strukturiert import SummeFunktion
from src.schul_mathematik.analysis.funktion import Funktion
import sympy as sp


def test_sin_cos_korrigiert():
    """Testet die korrigierte Nullstellen-Berechnung für sin(x) + cos(x) = 0"""
    print("=== Test: sin(x) + cos(x) = 0 mit korrigierter Implementation ===\n")

    # Erstelle die Summenfunktion
    f1 = Funktion("sin(x)")
    f2 = Funktion("cos(x)")
    summe = SummeFunktion([f1, f2])

    print(f"Funktion: {summe}")
    print(f"Term: {summe.term()}")

    # Berechne Nullstellen
    nullstellen = summe.nullstellen()

    print(f"\nGefundene Nullstellen: {len(nullstellen)}")

    if nullstellen:
        print("Konkrete Lösungen:")
        for i, ns in enumerate(nullstellen, 1):
            if hasattr(ns, "x"):
                x_wert = ns.x
                x_num = float(x_wert.evalf())
                print(f"  {i}. {x_wert} ≈ {x_num:.3f}")
            else:
                print(f"  {i}. {ns}")

    # Vergleiche mit dem, was wir erwarten
    print("\nErwartete Lösungen für sin(x) + cos(x) = 0:")
    print("In [-2π, 2π]: -5π/4, -π/4, 3π/4, 7π/4")

    # Teste auch direkt mit solve
    x = sp.Symbol("x")
    direkt_lösungen = sp.solve(sp.sin(x) + sp.cos(x), x)
    print(f"\nsolve() Ergebnis: {direkt_lösungen}")

    # Teste mit solveset
    solveset_lösungen = sp.solveset(sp.sin(x) + sp.cos(x), x, domain=sp.S.Reals)
    print(f"solveset() Ergebnis: {solveset_lösungen}")

    return nullstellen


if __name__ == "__main__":
    test_sin_cos_korrigiert()
