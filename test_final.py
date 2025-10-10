#!/usr/bin/env python3
"""
Final test der korrigierten Implementierung für sin(x) + cos(x) = 0
"""

from src.schul_mathematik.analysis.funktion import erstelle_funktion_automatisch
import sympy as sp


def test_final():
    """Finaler Test der korrigierten Nullstellen-Berechnung"""
    print("=== Finaler Test: sin(x) + cos(x) = 0 ===\n")

    # Erstelle die Summenfunktion automatisch
    summe = erstelle_funktion_automatisch("sin(x) + cos(x)")

    print(f"Funktion: {summe}")
    print(f"Term: {summe.term()}")
    print(f"Typ: {type(summe).__name__}")

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
    else:
        print("Keine Nullstellen gefunden!")

    # Erwartete Lösungen
    print("\nErwartete Lösungen für sin(x) + cos(x) = 0:")
    print("In [-2π, 2π]: -5π/4, -π/4, 3π/4, 7π/4")

    # Überprüfe, ob alle erwarteten Lösungen gefunden wurden
    erwartete = {
        sp.sympify("-5*pi/4"),
        sp.sympify("-pi/4"),
        sp.sympify("3*pi/4"),
        sp.sympify("7*pi/4"),
    }

    if nullstellen:
        gefundene = {ns.x for ns in nullstellen if hasattr(ns, "x")}
        if gefundene == erwartete:
            print("\n✅ PERFECT! Alle erwarteten Lösungen wurden gefunden!")
        else:
            print(f"\n⚠️  Abweichung:")
            print(f"Erwartet: {erwartete}")
            print(f"Gefunden: {gefundene}")
            print(f"Fehlend: {erwartete - gefundene}")
            print(f"Zusätzlich: {gefundene - erwartete}")

    return len(nullstellen) == 4


if __name__ == "__main__":
    erfolg = test_final()
    print(f"\nTest {'erfolgreich' if erfolg else 'fehlgeschlagen'}")
