#!/usr/bin/env python3
"""
Test examples for Taylor polynomials functionality
"""

import math

import numpy as np
from src.schul_analysis.taylorpolynom import Taylorpolynom

from src.schul_analysis import *


def test_taylor_exponential():
    """Test Taylor polynomials for e^x"""
    print("=== Taylorpolynome für e^x ===")

    # e^x Funktion
    f = GanzrationaleFunktion("1")  # Approximation von e^x um x=0

    # Taylorpolynome verschiedenen Grades
    for grad in [1, 2, 3, 5]:
        taylor = Taylorpolynom(f, entwicklungspunkt=0, grad=grad)
        print(f"\n{grad}. Taylorpolynom für e^x:")
        print(f"Polynom: {taylor.term()}")
        print(f"Koeffizienten: {taylor.koeffizienten()}")

        # Test an verschiedenen Stellen
        for x_test in [0, 0.5, 1, 2]:
            taylor_wert = taylor.wert(x_test)
            # e^x Näherung für kleine x: 1 + x + x²/2 + x³/6 + ...
            true_approx = sum([x_test**k / math.factorial(k) for k in range(grad + 1)])
            print(f"  f({x_test}) ≈ {taylor_wert:.6f} (erwartet: {true_approx:.6f})")


def test_taylor_sin():
    """Test Taylor polynomials for sin(x)"""
    print("\n=== Taylorpolynome für sin(x) ===")

    # sin(x) um x=0: x - x³/6 + x⁵/120 - ...
    # Hier testen wir mit einer Approximation

    # Taylorpolynome verschiedenen Grades
    for grad in [3, 5, 7]:
        # Manuell Koeffizienten für sin(x) setzen
        if grad >= 3:
            koeff = [0, 1, 0, -1 / 6]  # x - x³/6
            if grad >= 5:
                koeff.extend([0, 1 / 120])  # + x⁵/120
            if grad >= 7:
                koeff.extend([0, -1 / 5040])  # - x⁷/5040

            taylor_func = GanzrationaleFunktion(koeff[: grad + 1])
            taylor = Taylorpolynom(taylor_func, entwicklungspunkt=0, grad=grad)

            print(f"\n{grad}. Taylorpolynom für sin(x):")
            print(f"Polynom: {taylor.term()}")

            # Test an verschiedenen Stellen
            for x_test in [0, np.pi / 6, np.pi / 4, np.pi / 3]:
                taylor_wert = taylor.wert(x_test)
                true_value = np.sin(x_test)
                fehler = abs(taylor_wert - true_value)
                print(
                    f"  sin({x_test:.3f}) ≈ {taylor_wert:.6f} (wahr: {true_value:.6f}, Fehler: {fehler:.6f})"
                )


def test_taylor_cos():
    """Test Taylor polynomials for cos(x)"""
    print("\n=== Taylorpolynome für cos(x) ===")

    # cos(x) um x=0: 1 - x²/2 + x⁴/24 - ...

    for grad in [2, 4, 6]:
        # Manuell Koeffizienten für cos(x) setzen
        if grad >= 2:
            koeff = [1, 0, -1 / 2]  # 1 - x²/2
            if grad >= 4:
                koeff.extend([0, 1 / 24])  # + x⁴/24
            if grad >= 6:
                koeff.extend([0, -1 / 720])  # - x⁶/720

            taylor_func = GanzrationaleFunktion(koeff[: grad + 1])
            taylor = Taylorpolynom(taylor_func, entwicklungspunkt=0, grad=grad)

            print(f"\n{grad}. Taylorpolynom für cos(x):")
            print(f"Polynom: {taylor.term()}")

            # Test an verschiedenen Stellen
            for x_test in [0, np.pi / 6, np.pi / 4, np.pi / 3]:
                taylor_wert = taylor.wert(x_test)
                true_value = np.cos(x_test)
                fehler = abs(taylor_wert - true_value)
                print(
                    f"  cos({x_test:.3f}) ≈ {taylor_wert:.6f} (wahr: {true_value:.6f}, Fehler: {fehler:.6f})"
                )


def test_taylor_polynomial():
    """Test Taylor polynomials for actual polynomial functions"""
    print("\n=== Taylorpolynome für Polynomfunktionen ===")

    # Polynom f(x) = x² + 3x + 2
    f = GanzrationaleFunktion([1, 3, 2])

    # Entwicklung um verschiedenen Punkten
    for entwicklungspunkt in [0, 1, -1]:
        taylor = Taylorpolynom(f, entwicklungspunkt=entwicklungspunkt, grad=2)
        print(f"\nTaylorpolynom für f(x) = x² + 3x + 2 um x = {entwicklungspunkt}:")
        print(f"Original: {f.term()}")
        print(f"Taylor:   {taylor.term()}")

        # Sollte identisch sein (für Polynome)
        for x_test in [-2, 0, 2]:
            original_wert = f.wert(x_test)
            taylor_wert = taylor.wert(x_test)
            print(f"  f({x_test}) = {original_wert}, Taylor({x_test}) = {taylor_wert}")


def test_maclaurin_special():
    """Test Maclaurin polynomials (Taylor around 0)"""
    print("\n=== MacLaurin-Polynome (Spezialfall) ===")

    # Verschiedene Funktionen
    test_cases = [
        ([1, 2, 1], "f(x) = x² + 2x + 1"),
        ([1, 0, -1], "f(x) = x² - 1"),
        ([2, -3, 1], "f(x) = 2x² - 3x + 1"),
    ]

    for koeff, desc in test_cases:
        f = GanzrationaleFunktion(koeff)
        maclaurin = MacLaurin(f, grad=len(koeff) - 1)

        print(f"\n{desc}:")
        print(f"Original: {f.term()}")
        print(f"MacLaurin: {maclaurin.term()}")

        # Test um x=0
        print(f"  f(0) = {f.wert(0)}, MacLaurin(0) = {maclaurin.wert(0)}")


def test_taylor_koeffizienten():
    """Test Taylor coefficient calculation"""
    print("\n=== Taylor-Koeffizienten ===")

    # f(x) = x³ + 2x² + 3x + 4
    f = GanzrationaleFunktion([1, 2, 3, 4])

    # Entwicklung um x=1
    taylor = Taylorpolynom(f, entwicklungspunkt=1, grad=3)

    print(f"Für f(x) = {f.term()} um x=1:")
    print(f"Taylor-Polynom: {taylor.term()}")

    koeffizienten = taylor.koeffizienten()
    print("Entwickelte Koeffizienten:")
    for i, koeff in enumerate(koeffizienten):
        print(f"  a{i} = {koeff}")


def test_restglied():
    """Test remainder term calculation"""
    print("\n=== Restglied-Berechnung ===")

    # f(x) = x² (einfaches Beispiel)
    f = GanzrationaleFunktion([1, 0, 0])
    taylor = Taylorpolynom(f, entwicklungspunkt=0, grad=1)

    print(f"Für f(x) = {f.term()}:")
    print(f"1. Taylorpolynom: {taylor.term()}")

    # Restglied an verschiedenen Stellen
    for x_test in [0.5, 1, 2]:
        restglied = taylor.restglied_lagrange(x_test)
        wahrer_wert = f.wert(x_test)
        taylor_wert = taylor.wert(x_test)
        print(f"  Bei x = {x_test}:")
        print(f"    Wahrer Wert: {wahrer_wert}")
        print(f"    Taylor-Wert: {taylor_wert}")
        print(f"    Restglied: {restglied}")
        print(
            f"    Prüfung: {taylor_wert} + {restglied} = {taylor_wert + restglied} ≈ {wahrer_wert}"
        )


def test_konvergenzradius():
    """Test convergence radius calculation"""
    print("\n=== Konvergenzradius ===")

    # Geometrische Reihe: 1/(1-x) = 1 + x + x² + x³ + ...
    # Konvergenzradius R = 1

    # Approximation mit Polynom
    koeff = [1] * 5  # 1 + x + x² + x³ + x⁴
    f = GanzrationaleFunktion(koeff)
    taylor = Taylorpolynom(f, entwicklungspunkt=0, grad=4)

    print("Für geometrische Reihe (1 + x + x² + x³ + x⁴):")
    print(f"Taylorpolynom: {taylor.term()}")

    # Konvergenzradius testen
    radius = taylor.konvergenzradius()
    print(f"Geschätzter Konvergenzradius: {radius}")
    print("(Erwartet: 1 für geometrische Reihe)")


def run_all_tests():
    """Run all Taylor polynomial tests"""
    print("Teste Taylorpolynom-Funktionalität")
    print("=" * 50)

    test_taylor_exponential()
    test_taylor_sin()
    test_taylor_cos()
    test_taylor_polynomial()
    test_maclaurin_special()
    test_taylor_koeffizienten()
    test_restglied()
    test_konvergenzradius()

    print("\n" + "=" * 50)
    print("Alle Tests abgeschlossen!")


if __name__ == "__main__":
    run_all_tests()
