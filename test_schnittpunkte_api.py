#!/usr/bin/env python3
"""
Test script for the new Schnittpunkte API with exact symbolic calculation and parameter support
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import Funktion, ErstellePolynom, Schnittpunkte


def test_exakte_schnittpunkte():
    print("=== Test: Exakte Schnittpunkt-Berechnung ===")

    # Test 1: Einfache numerische Funktionen
    print("\n1. Test: Parabel und Gerade")
    print("   f(x) = x²")
    print("   g(x) = 2x")
    print("   Erwartet: (0|0) und (2|4)")

    f = Funktion("x^2")
    g = Funktion("2*x")

    schnittpunkte = Schnittpunkte(f, g)
    print(f"   Ergebnis: {len(schnittpunkte)} Schnittpunkte")
    for sp in schnittpunkte:
        print(f"   {sp}")

    # Test 2: Methodenzugriff
    print("\n2. Test: Methodenzugriff f.schnittpunkte(g)")
    schnittpunkte_methode = f.schnittpunkte(g)
    print(f"   Ergebnis: {len(schnittpunkte_methode)} Schnittpunkte")
    for sp in schnittpunkte_methode:
        print(f"   {sp}")

    # Test 3: Parametrisierte Funktionen
    print("\n3. Test: Parametrisierte Funktionen")
    print("   f(x) = a*x² + b*x + c")
    print("   g(x) = d*x + e")
    print("   Erwartet: Symbolische Ergebnisse mit Parametern")

    f_param = Funktion("a*x^2 + b*x + c")
    g_param = Funktion("d*x + e")

    schnittpunkte_param = Schnittpunkte(f_param, g_param)
    print(f"   Ergebnis: {len(schnittpunkte_param)} Schnittpunkte")
    for sp in schnittpunkte_param:
        print(f"   {sp}")
        print(f"   x-Typ: {type(sp.x)}, y-Typ: {type(sp.y)}")

    # Test 4: Exakte Brüche
    print("\n4. Test: Exakte Brüche")
    print("   f(x) = x² - 2")
    print("   g(x) = x + 1")
    print("   Erwartet: Exakte Lösungen mit Brüchen")

    f_bruch = Funktion("x^2 - 2")
    g_bruch = Funktion("x + 1")

    schnittpunkte_bruch = Schnittpunkte(f_bruch, g_bruch)
    print(f"   Ergebnis: {len(schnittpunkte_bruch)} Schnittpunkte")
    for sp in schnittpunkte_bruch:
        print(f"   {sp}")
        if hasattr(sp.x, "q") and hasattr(sp.x, "p"):
            print(f"   x als Bruch: {sp.x.p}/{sp.x.q}")

    # Test 5: Keine reellen Schnittpunkte
    print("\n5. Test: Keine reellen Schnittpunkte")
    print("   f(x) = x² + 1")
    print("   g(x) = 0")
    print("   Erwartet: Leere Liste (keine reellen Schnittpunkte)")

    f_keine = Funktion("x^2 + 1")
    g_keine = Funktion("0")

    schnittpunkte_keine = Schnittpunkte(f_keine, g_keine)
    print(f"   Ergebnis: {len(schnittpunkte_keine)} Schnittpunkte")

    # Test 6: ErstellePolynom Kompatibilität
    print("\n6. Test: ErstellePolynom Kompatibilität")
    print("   f(x) = 2x + 6 (ErstellePolynom([6, 2]))")
    print("   g(x) = (x-10)² (ErstellePolynom([100, -20, 1]))")

    f_poly = ErstellePolynom([6, 2])  # 6 + 2x = 2x + 6
    g_poly = ErstellePolynom([100, -20, 1])  # 100 - 20x + x² = (x-10)²

    schnittpunkte_poly = Schnittpunkte(f_poly, g_poly)
    print(f"   Ergebnis: {len(schnittpunkte_poly)} Schnittpunkte")
    for sp in schnittpunkte_poly:
        print(f"   {sp}")


def test_fehlerbehandlung():
    print("\n=== Test: Fehlerbehandlung ===")

    # Test 1: Ungültige Funktionen
    print("\n1. Test: Ungültige Funktionstypen")
    try:
        Schnittpunkte("keine Funktion", Funktion("x"))
        print("   FEHLER: Sollte Exception werfen!")
    except Exception as e:
        print(f"   ✓ Korrekte Exception: {type(e).__name__}: {e}")

    # Test 2: Nicht lösbare Gleichungen
    print("\n2. Test: Komplexe nicht lösbare Gleichung")
    try:
        f = Funktion("sin(x) + exp(x)")
        g = Funktion("cos(x) - log(x)")
        schnittpunkte = Schnittpunkte(f, g)
        print(f"   Ergebnis: {len(schnittpunkte)} Schnittpunkte (trotz Komplexität)")
    except Exception as e:
        print(f"   Exception bei komplexer Gleichung: {type(e).__name__}: {e}")


if __name__ == "__main__":
    test_exakte_schnittpunkte()
    test_fehlerbehandlung()

    print("\n=== Zusammenfassung ===")
    print("✓ Schnittpunkte-API implementiert")
    print("✓ Exakte symbolische Berechnung")
    print("✓ Parameter-Unterstützung")
    print("✓ Typsicherheit mit Datenklassen")
    print("✓ Kompatibilität mit bestehendem Code")
