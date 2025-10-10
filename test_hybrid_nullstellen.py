#!/usr/bin/env python3
"""
Test-Skript für die Hybrid-Nullstellen-API (Option C).

Testet:
1. nullstellen() - gibt strukturierte Nullstellen mit Vielfachheit zurück
2. nullstellen_mit_wiederholungen() - gibt Liste mit Wiederholungen zurück
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion


def test_hybrid_api():
    """Testet die Hybrid-API für Nullstellen."""
    print("=== Test Hybrid-Nullstellen-API ===")

    # Test 1: Funktion mit einfacher Nullstelle
    print("\n1. Einfache Nullstelle: x^2 - 4")
    f1 = Funktion("x^2 - 4")

    # Strukturierte Nullstellen
    nullstellen = f1.nullstellen()
    print(f"nullstellen(): {nullstellen}")

    # Nullstellen mit Wiederholungen
    nullstellen_wiederholungen = f1.nullstellen_mit_wiederholungen()
    print(f"nullstellen_mit_wiederholungen(): {nullstellen_wiederholungen}")

    # Test 2: Funktion mit mehrfacher Nullstelle
    print("\n2. Mehrfache Nullstelle: (x-1)^2 * (x-2)")
    f2 = Funktion("(x-1)**2 * (x-2)")

    # Strukturierte Nullstellen
    nullstellen = f2.nullstellen()
    print(f"nullstellen(): {nullstellen}")

    # Nullstellen mit Wiederholungen
    nullstellen_wiederholungen = f2.nullstellen_mit_wiederholungen()
    print(f"nullstellen_mit_wiederholungen(): {nullstellen_wiederholungen}")

    # Test 3: Trigonometrische Funktion
    print("\n3. Trigonometrische Funktion: sin(x) + cos(x)")
    f3 = Funktion("sin(x) + cos(x)")

    # Strukturierte Nullstellen
    nullstellen = f3.nullstellen()
    print(f"nullstellen(): {nullstellen}")

    # Nullstellen mit Wiederholungen
    nullstellen_wiederholungen = f3.nullstellen_mit_wiederholungen()
    print(f"nullstellen_mit_wiederholungen(): {nullstellen_wiederholungen}")

    # Test 4: Produktfunktion
    print("\n4. Produktfunktion: x^2 * sin(x)")
    f4 = Funktion("x**2 * sin(x)")

    # Strukturierte Nullstellen
    nullstellen = f4.nullstellen()
    print(f"nullstellen(): {nullstellen}")

    # Nullstellen mit Wiederholungen
    nullstellen_wiederholungen = f4.nullstellen_mit_wiederholungen()
    print(f"nullstellen_mit_wiederholungen(): {nullstellen_wiederholungen}")


def test_kompatibilitaet():
    """Testet die Kompatibilität mit bestehendem Code."""
    print("\n=== Test Kompatibilität ===")

    # Teste, ob die alten Methoden noch funktionieren
    f = Funktion("x^2 - 4")

    # Alte Methoden sollten noch funktionieren
    try:
        nullstellen_alt = f.Nullstellen()
        print(f"Alte Methode Nullstellen(): {nullstellen_alt}")
    except Exception as e:
        print(f"Fehler bei alter Methode: {e}")

    # Neue Methode sollte auch funktionieren
    try:
        nullstellen_neu = f.nullstellen()
        print(f"Neue Methode nullstellen(): {nullstellen_neu}")
    except Exception as e:
        print(f"Fehler bei neuer Methode: {e}")

    # Hybrid-Methode
    try:
        nullstellen_hybrid = f.nullstellen_mit_wiederholungen()
        print(f"Hybrid-Methode nullstellen_mit_wiederholungen(): {nullstellen_hybrid}")
    except Exception as e:
        print(f"Fehler bei Hybrid-Methode: {e}")


def test_datenklasse_methoden():
    """Testet die Methoden der Nullstelle-Datenklasse."""
    print("\n=== Test Nullstelle-Datenklasse ===")

    f = Funktion("(x-1)**2 * (x-2)")
    nullstellen = f.nullstellen()

    for nullstelle in nullstellen:
        print(f"\nNullstelle: {nullstelle}")
        print(f"  to_float(): {nullstelle.to_float()}")
        print(
            f"  to_list_with_multiplicity(): {nullstelle.to_list_with_multiplicity()}"
        )

        # Teste Iteration
        print("  Iteration:")
        for i, wert in enumerate(nullstelle):
            print(f"    {i}: {wert}")


if __name__ == "__main__":
    print("Teste die Hybrid-Nullstellen-API...")

    try:
        test_hybrid_api()
        test_kompatibilitaet()
        test_datenklasse_methoden()
        print("\n=== Alle Tests abgeschlossen ===")
    except Exception as e:
        print(f"Fehler beim Testen: {e}")
        import traceback

        traceback.print_exc()
