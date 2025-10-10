#!/usr/bin/env python3
"""
Test für die optimierte solveset-Integration in SummenFunktion.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion
import sympy as sp


def test_solveset_integration():
    """Testet ob solveset wirklich alle Lösungen findet."""
    print("=== Test solveset-Integration ===\n")

    # Test: sin(x) + cos(x) sollte mehrere Lösungen haben
    print("1. sin(x) + cos(x) - Erwartet: -π/4, 3π/4, 7π/4, etc.")
    f1 = Funktion("sin(x) + cos(x)")
    print(f"Funktionstyp: {f1.funktionstyp}")

    nullstellen = f1.nullstellen()
    print(f"Gefundene Nullstellen: {nullstellen}")

    # Erwartete Lösungen im Intervall [-2π, 2π]
    print("\nErwartete Lösungen im Intervall [-2π, 2π]:")
    from sympy import pi

    erwartete = [-7 * pi / 4, -3 * pi / 4, pi / 4, 5 * pi / 4]  # Korrigierte Werte
    for lösung in erwartete:
        print(f"  x = {lösung} ≈ {float(lösung.evalf()):.3f}")

    # Überprüfe ob unsere gefundene Lösung darin enthalten ist
    if nullstellen:
        gefundene_werte = [float(ns.x.evalf()) for ns in nullstellen]
        print(f"\nGefundene Werte: {gefundene_werte}")

        for lösung in erwartete:
            wert = float(lösung.evalf())
            if any(abs(wert - g) < 0.001 for g in gefundene_werte):
                print(f"  ✅ {lösung} gefunden")
            else:
                print(f"  ❌ {lösung} NICHT gefunden")


if __name__ == "__main__":
    test_solveset_integration()
