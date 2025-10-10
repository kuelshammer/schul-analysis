#!/usr/bin/env python3
"""
Test-Skript für Linearfaktoren-Eingabe
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion


def test_linearfaktoren():
    """Testet verschiedene Linearfaktoren-Eingaben"""

    print("=== TEST LINEARFAKTOREN ===\n")

    test_cases = [
        ("(x-2)(x+3)", "Einfache Linearfaktoren"),
        ("(x-1)(x-2)(x-3)", "Drei Linearfaktoren"),
        ("(x+1)^2", "Potenzierte Linearfaktoren"),
        ("(x-2)(x+3)^2", "Gemischte Potenzen"),
        ("2(x-1)(x+2)", "Mit Koeffizient"),
        ("(x-1)(x^2+4)", "Gemischt mit Polynom"),
        ("(x-1)(3x+2)", "Mit Koeffizient in Faktor"),
        ("(2x-4)(x+1)", "Koeffizient vor x"),
    ]

    for eingabe, beschreibung in test_cases:
        print(f"Test: {beschreibung}")
        print(f"Eingabe: '{eingabe}'")

        try:
            f = GanzrationaleFunktion(eingabe)
            print("✅ Erfolgreich!")
            print(f"   Original: {f.term_str}")
            print(f"   LaTeX: {f.term_latex()}")
            print(f"   Koeffizienten: {f.koeffizienten}")

            # Teste Berechnungen
            nullstellen = f.nullstellen()
            print(f"   Nullstellen: {nullstellen}")

        except Exception as e:
            print(f"❌ Fehler: {e}")

        print()


if __name__ == "__main__":
    test_linearfaktoren()
