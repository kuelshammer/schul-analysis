#!/usr/bin/env python3
"""
Demo für Wendepunkte-Berechnung im Schul-Analysis Framework

Dieses Skript demonstriert die neue Wendepunkte-Funktionalität.
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import GanzrationaleFunktion, Extremstellen, Wendepunkte, Graph


def demo_wendepunkte():
    """Demonstriert die Wendepunkte-Berechnung mit verschiedenen Beispielen"""

    print("=== WENDEPUNKTE-DEMO ===\n")

    # Beispiel 1: Einfacher kubischer Fall
    print("1. Einfache kubische Funktion: f(x) = x³")
    f1 = GanzrationaleFunktion("x^3")
    print(f"Funktion: {f1.term()}")

    wendepunkte1 = Wendepunkte(f1)
    extremstellen1 = Extremstellen(f1)

    print(f"Wendepunkte: {wendepunkte1}")
    print(f"Extremstellen: {extremstellen1}")
    print()

    # Beispiel 2: Funktion mit mehreren Wendepunkten
    print("2. Funktion mit mehreren Wendepunkten: f(x) = x⁴ - 4x³")
    f2 = GanzrationaleFunktion("x^4 - 4*x^3")
    print(f"Funktion: {f2.term()}")

    wendepunkte2 = Wendepunkte(f2)
    extremstellen2 = Extremstellen(f2)

    print(f"Wendepunkte: {wendepunkte2}")
    print(f"Extremstellen: {extremstellen2}")
    print()

    # Beispiel 3: Sinus-ähnliche Funktion
    print("3. Komplexere Funktion: f(x) = x³ - 6x² + 9x + 1")
    f3 = GanzrationaleFunktion("x^3 - 6*x^2 + 9*x + 1")
    print(f"Funktion: {f3.term()}")

    wendepunkte3 = Wendepunkte(f3)
    extremstellen3 = Extremstellen(f3)

    print(f"Wendepunkte: {wendepunkte3}")
    print(f"Extremstellen: {extremstellen3}")

    # Zeige Graph
    print("\nErstelle Graph der Funktion...")
    try:
        graph = Graph(f3, x_bereich=(-1, 5))
        print(f"Graph erstellt für f(x) = {f3.term()}")
        print("Der Graph zeigt die Funktion mit ihren Extremstellen und Wendepunkten.")
    except Exception as e:
        print(f"Fehler beim Erstellen des Graphen: {e}")

    print()

    # Beispiel 4: Polynom 5. Grades
    print("4. Polynom 5. Grades: f(x) = x⁵ - 5x⁴ + 5x³ + 5x² - 6x")
    f4 = GanzrationaleFunktion("x^5 - 5*x^4 + 5*x^3 + 5*x^2 - 6*x")
    print(f"Funktion: {f4.term()}")

    wendepunkte4 = Wendepunkte(f4)
    extremstellen4 = Extremstellen(f4)
    nullstellen4 = f4.nullstellen()

    print(f"Nullstellen: {nullstellen4}")
    print(f"Extremstellen: {extremstellen4}")
    print(f"Wendepunkte: {wendepunkte4}")
    print()

    # Beispiel 5: Spezialfall ohne Wendepunkte
    print("5. Parabel (keine Wendepunkte): f(x) = x² - 4x + 3")
    f5 = GanzrationaleFunktion("x^2 - 4*x + 3")
    print(f"Funktion: {f5.term()}")

    wendepunkte5 = Wendepunkte(f5)
    extremstellen5 = Extremstellen(f5)

    print(f"Wendepunkte: {wendepunkte5}")
    print(f"Extremstellen: {extremstellen5}")
    print()

    # Zusammenfassung
    print("=== ZUSAMMENFASSUNG ===")
    print("Die Wendepunkte-Funktion:")
    print("- Berechnet alle Wendepunkte einer ganzrationalen Funktion")
    print(
        "- Verwendet die mathematisch korrekte Definition (f''(x) = 0 und f'''(x) ≠ 0)"
    )
    print("- Behandelt auch Spezialfälle mit höheren Ableitungen")
    print("- Gibt Wendepunkte als (x-Koordinate, Typ) Tupel zurück")
    print("- Integriert sich nahtlos in das Schul-Analysis Framework ein")


if __name__ == "__main__":
    demo_wendepunkte()
