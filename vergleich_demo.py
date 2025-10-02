#!/usr/bin/env python3
"""
Vergleichs-Demo: Taylorpolynome vs. Schmiegkurven (Interpolation)

Zeigt den Unterschied zwischen zwei wichtigen mathematischen Konzepten:
1. Taylorpolynome: Approximation einer Funktion um einen Punkt
2. Schmiegkurven: Interpolation durch vorgegebene Punkte
"""

import math

from src.schul_analysis import *


def demo_taylor_vs_schmiegkurve():
    """Demonstriert den Unterschied zwischen Taylor und Interpolation"""
    print("=== VERGLEICH: TAYLORPOLYNOM vs. SCHMIEGKURVE ===\n")

    print("1. TAYLORPOLYNOM (Funktionsapproximation)")
    print("   Problem: Approximiere sin(x) um x=0")
    print("   Eingabe: Funktion + Entwicklungspunkt + Grad")

    # Taylorpolynom für sin(x)
    # sin(x) ≈ x - x³/6 + x⁵/120
    taylor_sin = GanzrationaleFunktion([0, 1, 0, -1 / 6, 0, 1 / 120])
    taylor = Taylorpolynom(taylor_sin, entwicklungspunkt=0, grad=5)

    print(f"   Ergebnis: {taylor.term()}")
    print("   Verwendung: sin(x) ≈ x - x³/6 + x⁵/120")
    print()

    # Werte vergleichen
    print("   Approximationsgüte:")
    for x in [0, 0.5, 1, 1.5]:
        exact = math.sin(x)
        approx = taylor.wert(x)
        print(
            f"   x={x:.1f}: sin(x)={exact:.4f}, Taylor={approx:.4f}, Fehler={abs(exact - approx):.4f}"
        )
    print()

    print("2. SCHMIEGKURVE (Interpolation)")
    print("   Problem: Finde Kurve durch Punkte (0,0), (1,0.8), (2,0.9)")
    print("   Eingabe: Punkte + optionale Bedingungen")

    # Schmiegkurve durch Punkte
    punkte = [(0, 0), (1, 0.8), (2, 0.9)]
    schmiegkurve = Schmiegkurve(punkte)  # Einfache Punkteliste

    print(f"   Ergebnis: {schmiegkurve.term()}")
    print("   Verwendung: Kurve verläuft genau durch die vorgegebenen Punkte")
    print()

    # Punkte überprüfen
    print("   Interpolationsgüte:")
    for x, y_erwartet in punkte:
        y_aktuell = schmiegkurve.wert(x)
        print(
            f"   ({x},{y_erwartet}): Tatsächlich=({x},{y_aktuell:.3f}), Fehler={abs(y_erwartet - y_aktuell):.6f}"
        )
    print()


def demo_hermite_interpolation():
    """Demonstriert Hermite-Interpolation mit Ableitungsbedingungen"""
    print("3. HERMITE-INTERPOLATION (Erweiterte Schmiegkurve)")
    print("   Problem: Finde Kurve durch (0,1) mit Steigung -1 und durch (1,0)")
    print("   Eingabe: Punkte + Ableitungsbedingungen")

    # Hermite-Interpolation (vereinfacht)
    punkte = [(0, 1), (1, 0)]
    tangenten = [-1, None]  # Steigung -1 bei x=0, keine Bedingung bei x=1
    hermite = Schmiegkurve(punkte, tangenten=tangenten)

    print(f"   Ergebnis: {hermite.term()}")
    print()

    # Bedingungen überprüfen
    print("   Bedingungen überprüfen:")
    print(f"   f(0) = {hermite.wert(0):.3f} (erwartet: 1.0)")

    # Numerische Ableitung zur Steigungsprüfung
    h = 0.0001
    steigung = (hermite.wert(0 + h) - hermite.wert(0)) / h
    print(f"   f'(0) ≈ {steigung:.3f} (erwartet: -1.0)")
    print(f"   f(1) = {hermite.wert(1):.3f} (erwartet: 0.0)")
    print()


def demo_schmiegparabel():
    """Demonstriert die Schmiegparabel als spezialisierte Interpolation"""
    print("4. SCHMIEGPARABEL (Quadratische Interpolation)")
    print("   Problem: Finde Parabel durch 3 Punkte mit optionalen Tangenten")

    # Schmiegparabel
    p1 = (0, 0)
    p2 = (1, 1)
    p3 = (2, 0)
    parabel = Schmiegkurve.schmiegparabel(p1, p2, p3)

    print(f"   Punkte: {p1}, {p2}, {p3}")
    print(f"   Ergebnis: {parabel.term()}")
    print()

    # Punkte überprüfen
    print("   Interpolation überprüfen:")
    for x, y_erwartet in [p1, p2, p3]:
        y_aktuell = parabel.wert(x)
        print(
            f"   ({x},{y_erwartet}): Tatsächlich=({x},{y_aktuell:.3f}), Fehler={abs(y_erwartet - y_aktuell):.6f}"
        )
    print()


def demo_vergleich_taylor_interpolation():
    """Vergleicht Taylor und Interpolation am gleichen Beispiel"""
    print("5. DIRECTER VERGLEICH: Taylor vs. Interpolation")
    print("   Szenario: Wir haben eine Funktion f(x) = x² - 2x + 2")
    print("   und möchten sie am Punkt x=1 approximieren/interpolieren")
    print()

    # Originalfunktion
    f = GanzrationaleFunktion([1, -2, 2])  # x² - 2x + 2
    print(f"   Originalfunktion: {f.term()}")
    print()

    # Taylor-Ansatz
    print("   TAYLOR-ANSATZ:")
    taylor = Taylorpolynom(f, entwicklungspunkt=1, grad=2)
    print(f"   Taylorpolynom um x=1: {taylor.term()}")
    print("   Eigenschaft: Perfekte Approximation um x=1")
    print(f"   f(1) = {f.wert(1)}, Taylor(1) = {taylor.wert(1)}")
    print()

    # Interpolations-Ansatz
    print("   INTERPOLATIONS-ANSATZ:")
    # Wir brauchen Punkte, die auf der Funktion liegen
    punkte = [(0, f.wert(0)), (1, f.wert(1)), (2, f.wert(2))]
    interpolation = Schmiegkurve(punkte)
    p0 = (0, f.wert(0))
    p1 = (1, f.wert(1))
    p2 = (2, f.wert(2))
    print(f"   Punkte: {p0}, {p1}, {p2}")
    print(f"   Interpolationspolynom: {interpolation.term()}")
    print("   Eigenschaft: Perfekte Interpolation durch die Punkte")
    print()

    # Vergleich an verschiedenen Stellen
    print("   Vergleich an verschiedenen Stellen:")
    for x in [0.5, 1.5]:
        original = f.wert(x)
        taylor_wert = taylor.wert(x)
        interp_wert = interpolation.wert(x)
        print(
            f"   x={x}: Original={original:.3f}, Taylor={taylor_wert:.3f}, Interpolation={interp_wert:.3f}"
        )
    print()


def demo_praktische_anwendungen():
    """Zeigt praktische Anwendungen beider Konzepte"""
    print("6. PRAKTISCHE ANWENDUNGEN")
    print()

    print("   TAYLORPOLYNOME - gut für:")
    print("   • Funktionserklärung in der Nähe eines Punktes")
    print("   • Numerische Berechnungen (z.B. Taschenrechner)")
    print("   • Physikalische Approximationen")
    print("   • Konvergenzanalyse von Reihen")
    print()

    print("   SCHMIEGKURVEN - gut für:")
    print("   • Dateninterpolation (Messpunkte verbinden)")
    print("   • Kurvenkonstruktion durch vorgegebene Bedingungen")
    print("   • Computergrafik (Bezier-Kurven)")
    print("   • Numerische Analysis mit Randbedingungen")
    print()


def run_vergleichs_demo():
    """Führt die komplette Vergleichsdemo durch"""
    print("VERGLEICHSDemo: Taylorpolynome vs. Schmiegkurven")
    print("=" * 60)

    demo_taylor_vs_schmiegkurve()
    demo_hermite_interpolation()
    demo_schmiegparabel()
    demo_vergleich_taylor_interpolation()
    demo_praktische_anwendungen()

    print("=" * 60)
    print("FAZIT:")
    print("• Taylorpolynome: Approximation von Funktionen um einen Punkt")
    print("• Schmiegkurven: Exakte Interpolation durch Punkte mit Bedingungen")
    print("• Beide sind wichtige, komplementäre Werkzeuge der Analysis!")
    print()


if __name__ == "__main__":
    run_vergleichs_demo()
