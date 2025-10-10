#!/usr/bin/env python3
"""
Test-Skript für die erweiterten parametrischen Wendestellen-Strategien.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion
import logging

# Logging für Debug-Informationen aktivieren
logging.basicConfig(level=logging.DEBUG)


def test_wendestellen_parametrisch():
    """Testet die fortgeschrittenen parametrischen Wendestellen-Strategien."""

    print("=== Test Erweiterte Parametrische Wendestellen-Strategien ===\n")

    # Test 1: Kubische parametrische Funktion
    print("📈 Test 1: Kubische Funktion f(x) = ax³ + bx² + cx + d")
    f1 = Funktion("a*x^3 + b*x^2 + c*x + d")

    print("Zweite Ableitung:")
    f1_doppelstrich = f1.ableitung(2)
    print(f"  f''(x) = {f1_doppelstrich.term()}")

    print("Wendestellen mit fortgeschrittener Methode:")
    ergebnisse1 = f1.wendestellen_optimiert()
    for ergebnis in ergebnisse1:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 2: Einfache kubische Funktion
    print("📈 Test 2: Einfache Funktion f(x) = x³ + ax")
    f2 = Funktion("x^3 + a*x")

    print("Zweite Ableitung:")
    f2_doppelstrich = f2.ableitung(2)
    print(f"  f''(x) = {f2_doppelstrich.term()}")

    print("Wendestellen mit fortgeschrittener Methode:")
    ergebnisse2 = f2.wendestellen_optimiert()
    for ergebnis in ergebnisse2:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 3: Quartische Funktion
    print("📈 Test 3: Quartische Funktion f(x) = ax⁴ + bx³ + cx² + dx + e")
    f3 = Funktion("a*x^4 + b*x^3 + c*x^2 + d*x + e")

    print("Zweite Ableitung:")
    f3_doppelstrich = f3.ableitung(2)
    print(f"  f''(x) = {f3_doppelstrich.term()}")

    print("Wendestellen mit fortgeschrittener Methode:")
    ergebnisse3 = f3.wendestellen_optimiert()
    for ergebnis in ergebnisse3:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print()

    # Test 4: Vergleich mit alter Methode
    print("📈 Test 4: Vergleich f(x) = x³ + ax")
    print("Alte Methode:")
    alte_ergebnisse = f2._wendestellen_parametrisch_fallback()
    for ergebnis in alte_ergebnisse:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")

    print("Neue Methode:")
    neue_ergebnisse = f2._wendestellen_parametrisch_fortgeschritten()
    for ergebnis in neue_ergebnisse:
        print(f"  x = {ergebnis.x}, Typ = {ergebnis.typ}")


if __name__ == "__main__":
    test_wendestellen_parametrisch()
