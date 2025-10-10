#!/usr/bin/env python3
"""
Test-Skript für die erweiterten parametrischen Lösungsstrategien.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion
import logging

# Logging für Debug-Informationen aktivieren
logging.basicConfig(level=logging.DEBUG)


def test_parametrisch_fortgeschritten():
    """Testet die fortgeschrittenen parametrischen Lösungsstrategien."""

    print("=== Test Erweiterte Parametrische Strategien ===\n")

    # Test 1: Quadratische parametrische Funktion
    print("📈 Test 1: Quadratische Funktion f(x) = ax² + bx + c")
    f1 = Funktion("a*x^2 + b*x + c")

    print("Ergebnis mit fortgeschrittener Methode:")
    ergebnisse1 = f1.nullstellen_optimiert()
    for ergebnis in ergebnisse1:
        print(f"  x = {ergebnis.x}, Vielfachheit = {ergebnis.multiplicitaet}")

    print()

    # Test 2: Kubische parametrische Funktion
    print("📈 Test 2: Kubische Funktion f(x) = ax³ + bx² + cx + d")
    f2 = Funktion("a*x^3 + b*x^2 + c*x + d")

    print("Ergebnis mit fortgeschrittener Methode:")
    ergebnisse2 = f2.nullstellen_optimiert()
    for ergebnis in ergebnisse2:
        print(f"  x = {ergebnis.x}, Vielfachheit = {ergebnis.multiplicitaet}")

    print()

    # Test 3: Faktorisierbare Funktion
    print("📈 Test 3: Faktorisierbare Funktion f(x) = x² - (a+b)x + ab")
    f3 = Funktion("x^2 - (a+b)*x + a*b")

    print("Ergebnis mit fortgeschrittener Methode:")
    ergebnisse3 = f3.nullstellen_optimiert()
    for ergebnis in ergebnisse3:
        print(f"  x = {ergebnis.x}, Vielfachheit = {ergebnis.multiplicitaet}")

    print()

    # Test 4: Vergleich mit alter Methode
    print("📈 Test 4: Vergleich f(x) = ax² + bx + c")
    print("Alte Methode:")
    alte_ergebnisse = f1._nullstellen_parametrisch_fallback()
    for ergebnis in alte_ergebnisse:
        print(f"  x = {ergebnis.x}, Vielfachheit = {ergebnis.multiplicitaet}")

    print("Neue Methode:")
    neue_ergebnisse = f1._nullstellen_parametrisch_fortgeschritten()
    for ergebnis in neue_ergebnisse:
        print(f"  x = {ergebnis.x}, Vielfachheit = {ergebnis.multiplicitaet}")


if __name__ == "__main__":
    test_parametrisch_fortgeschritten()
