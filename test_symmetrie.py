#!/usr/bin/env python3
"""
Test-Skript für die neue symmetrische Architektur der mathematischen Analyse.

Dieses Skript testet die drei optimierten Methoden:
- nullstellen_optimiert() für f(x) = 0
- extremstellen_optimiert() für f'(x) = 0
- wendepunkte_optimiert() für f''(x) = 0
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.funktion import Funktion


def test_symmetrische_architektur():
    """Testet die symmetrische Architektur mit verschiedenen Funktionstypen."""

    print("=== Test Symmetrische Architektur ===\n")

    # Test 1: Kubische Funktion (klassischer Fall)
    print("📈 Test 1: Kubische Funktion f(x) = x³ - 3x² + 4")
    f1 = Funktion("x^3 - 3*x^2 + 4")

    print("Nullstellen (f(x) = 0):")
    ns1 = f1.nullstellen_optimiert()
    for ns in ns1:
        print(f"  x = {ns.x}")

    print("Extremstellen (f'(x) = 0):")
    es1 = f1.extremstellen_optimiert()
    for es in es1:
        print(f"  x = {es.x}, Typ = {es.typ}")

    print("Extrempunkte (mit y-Koordinaten):")
    ep1 = f1.extrempunkte_optimiert()
    for ep in ep1:
        print(f"  x = {ep.x}, y = {ep.y}, Typ = {ep.typ}")

    print("Wendepunkte (f''(x) = 0):")
    wp1 = f1.wendepunkte_optimiert()
    for wp in wp1:
        print(f"  x = {wp.x}, Typ = {wp.typ}")

    print()

    # Test 2: Polynom 4. Grades
    print("📈 Test 2: Polynom 4. Grades f(x) = x⁴ - 8x³ + 18x² - 27")
    f2 = Funktion("x^4 - 8*x^3 + 18*x^2 - 27")

    print("Nullstellen (f(x) = 0):")
    ns2 = f2.nullstellen_optimiert()
    for ns in ns2:
        print(f"  x = {ns.x}")

    print("Extremstellen (f'(x) = 0):")
    es2 = f2.extremstellen_optimiert()
    for es in es2:
        print(f"  x = {es.x}, Typ = {es.typ}")

    print("Extrempunkte (mit y-Koordinaten):")
    ep2 = f2.extrempunkte_optimiert()
    for ep in ep2:
        print(f"  x = {ep.x}, y = {ep.y}, Typ = {ep.typ}")

    print("Wendepunkte (f''(x) = 0):")
    wp2 = f2.wendepunkte_optimiert()
    for wp in wp2:
        print(f"  x = {wp.x}, Typ = {wp.typ}")

    print()

    # Test 3: Trigonometrische Funktion
    print("📈 Test 3: Trigonometrische Funktion f(x) = sin(x) + cos(x)")
    f3 = Funktion("sin(x) + cos(x)")

    print("Nullstellen (f(x) = 0):")
    ns3 = f3.nullstellen_optimiert()
    for ns in ns3:
        print(f"  x = {ns.x}")

    print("Extremstellen (f'(x) = 0):")
    es3 = f3.extremstellen_optimiert()
    for es in es3:
        print(f"  x = {es.x}, Typ = {es.typ}")

    print("Extrempunkte (mit y-Koordinaten):")
    ep3 = f3.extrempunkte_optimiert()
    for ep in ep3:
        print(f"  x = {ep.x}, y = {ep.y}, Typ = {ep.typ}")

    print("Wendepunkte (f''(x) = 0):")
    wp3 = f3.wendepunkte_optimiert()
    for wp in wp3:
        print(f"  x = {wp.x}, Typ = {wp.typ}")

    print()

    # Test 4: Parametrische Funktion
    print("📈 Test 4: Parametrische Funktion f(x) = ax² + bx + c")
    f4 = Funktion("a*x^2 + b*x + c")

    print("Nullstellen (f(x) = 0):")
    ns4 = f4.nullstellen_optimiert()
    for ns in ns4:
        print(f"  x = {ns.x}")

    print("Extremstellen (f'(x) = 0):")
    es4 = f4.extremstellen_optimiert()
    for es in es4:
        print(f"  x = {es.x}, Typ = {es.typ}")

    print("Extrempunkte (mit y-Koordinaten):")
    ep4 = f4.extrempunkte_optimiert()
    for ep in ep4:
        print(f"  x = {ep.x}, y = {ep.y}, Typ = {ep.typ}")

    print("Wendepunkte (f''(x) = 0):")
    wp4 = f4.wendepunkte_optimiert()
    for wp in wp4:
        print(f"  x = {wp.x}, Typ = {wp.typ}")

    print("\n=== Symmetrie-Test abgeschlossen ===")


if __name__ == "__main__":
    test_symmetrische_architektur()
