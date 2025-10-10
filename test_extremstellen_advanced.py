#!/usr/bin/env python3
"""
Test-Skript für die erweiterten parametrischen Extremstellen-Strategien.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion
import logging

# Logging für Debug-Informationen aktivieren
logging.basicConfig(level=logging.DEBUG)


def test_extremstellen_parametrisch():
    """Testet die fortgeschrittenen parametrischen Extremstellen-Strategien."""

    print("=== Test Erweiterte Parametrische Extremstellen-Strategien ===\n")

    # Test 1: Quadratische parametrische Funktion
    print("📈 Test 1: Quadratische Funktion f(x) = ax² + bx + c")
    f1 = Funktion("a*x^2 + b*x + c")

    print("Erste Ableitung:")
    f1_strich = f1.ableitung(1)
    print(f"  f'(x) = {f1_strich.term()}")

    print("Extremstellen mit fortgeschrittener Methode:")
    ergebnisse1 = f1.extremstellen_optimiert()
    for ergebnis in ergebnisse1:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 2: Kubische parametrische Funktion
    print("📈 Test 2: Kubische Funktion f(x) = ax³ + bx² + cx + d")
    f2 = Funktion("a*x^3 + b*x^2 + c*x + d")

    print("Erste Ableitung:")
    f2_strich = f2.ableitung(1)
    print(f"  f'(x) = {f2_strich.term()}")

    print("Extremstellen mit fortgeschrittener Methode:")
    ergebnisse2 = f2.extremstellen_optimiert()
    for ergebnis in ergebnisse2:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 3: Einfache parametrische Funktion
    print("📈 Test 3: Einfache Funktion f(x) = x³ + ax")
    f3 = Funktion("x^3 + a*x")

    print("Erste Ableitung:")
    f3_strich = f3.ableitung(1)
    print(f"  f'(x) = {f3_strich.term()}")

    print("Extremstellen mit fortgeschrittener Methode:")
    ergebnisse3 = f3.extremstellen_optimiert()
    for ergebnis in ergebnisse3:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 4: Vergleich mit alter Methode
    print("📈 Test 4: Vergleich f(x) = ax² + bx + c")
    print("Alte Methode:")
    alte_ergebnisse = f1._extremstellen_parametrisch_fallback()
    for ergebnis in alte_ergebnisse:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print("Neue Methode:")
    neue_ergebnisse = f1._extremstellen_parametrisch_fortgeschritten()
    for ergebnis in neue_ergebnisse:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")


if __name__ == "__main__":
    test_extremstellen_parametrisch()
