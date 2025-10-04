#!/usr/bin/env python3
"""
Test-Skript für den verbesserten Konstruktor
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.ganzrationale import GanzrationaleFunktion


def test_verbesserter_konstruktor():
    """Testet den verbesserten String-Konstruktor"""

    print("=== TEST VERBESSERTER KONSTRUKTOR ===\n")

    # Test-Eingaben, die vorher nicht funktioniert haben
    test_cases = [
        ("x^2+4x-2", "Standard-Schreibweise"),
        ("$x^2+4x-2$", "LaTeX-Format"),
        ("x**2+4*x-2", "Python-Syntax"),
        ("2x", "Implizite Multiplikation"),
        ("x^2 + 4x - 2", "Mit Leerzeichen"),
        ("-x^2 + 3x - 1", "Negativer führender Koeffizient"),
        ("x^2 + x + 1", "Koeffizient 1"),
        ("x^2 - 1", "Ohne x-Term"),
        ("5", "Konstante"),
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


def test_liste_dict_konstruktoren():
    """Testet Listen- und Dictionary-Konstruktoren"""

    print("=== TEST LISTE & DICTIONARY KONSTRUKTOREN ===\n")

    # x^2 - 4x + 3
    print("1. Listen-Konstruktor:")
    try:
        f1 = GanzrationaleFunktion([1, -4, 3])
        print(f"   [1, -4, 3] → {f1.term()}")
        print(f"   Koeffizienten: {f1.koeffizienten}")
        print(f"   Nullstellen: {f1.nullstellen()}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")

    print("\n2. Dictionary-Konstruktor:")
    try:
        f2 = GanzrationaleFunktion({2: 1, 1: -4, 0: 3})
        print(f"   {{2: 1, 1: -4, 0: 3}} → {f2.term()}")
        print(f"   Koeffizienten: {f2.koeffizienten}")
        print(f"   Nullstellen: {f2.nullstellen()}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")

    print("\n3. Dictionary mit Lücken:")
    try:
        f3 = GanzrationaleFunktion({3: 2, 1: -3, 0: 1})  # 2x^3 - 3x + 1
        print(f"   {{3: 2, 1: -3, 0: 1}} → {f3.term()}")
        print(f"   Koeffizienten: {f3.koeffizienten}")
        print(f"   Nullstellen: {f3.nullstellen()}")
    except Exception as e:
        print(f"   ❌ Fehler: {e}")


def test_grenzfälle():
    """Testet Grenzfälle"""

    print("\n=== TEST GRENZFÄLLE ===\n")

    grenzfälle = [
        ("0", "Null-Funktion"),
        ("x", "Lineare Funktion"),
        ("x^0", "x^0 = 1"),
        ("1*x^1 + 2*x^0", "Explizite Schreibweise"),
        ("x^2 + 0*x + 1", "Null-Koeffizient"),
    ]

    for eingabe, beschreibung in grenzfälle:
        print(f"{beschreibung}: '{eingabe}'")
        try:
            f = GanzrationaleFunktion(eingabe)
            print(f"   → {f.term()}")
            print(f"   → Koeffizienten: {f.koeffizienten}")
        except Exception as e:
            print(f"   → Fehler: {e}")
        print()


if __name__ == "__main__":
    test_verbesserter_konstruktor()
    test_liste_dict_konstruktoren()
    test_grenzfälle()
