#!/usr/bin/env python3
"""
Test der neuen extremstellen_optimiert() Methode, die unser starkes Nullstellen-Framework nutzt.
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis import Funktion


def test_standard_polynom():
    """Test mit Standard-Polynom x³ - 3x² + 4"""
    print("=== Test 1: Standard-Polynom ===")
    f = Funktion("x^3 - 3x^2 + 4")

    print(f"Funktion: {f.term()}")
    print(f"Erste Ableitung: {f.ableitung().term()}")

    # Alte Methode
    try:
        alte_extrema = f.extremstellen()
        print(f"Alte extremstellen(): {alte_extrema}")
    except Exception as e:
        print(f"Fehler bei alter Methode: {e}")

    # Neue Methode
    try:
        neue_extrema = f.extremstellen_optimiert()
        print(f"Neue extremstellen_optimiert():")
        for extremum in neue_extrema:
            print(f"  {extremum}")
    except Exception as e:
        print(f"Fehler bei neuer Methode: {e}")


def test_trigonometrische_funktion():
    """Test mit trigonometrischer Funktion sin(x) + cos(x)"""
    print("\n=== Test 2: Trigonometrische Funktion ===")
    f = Funktion("sin(x) + cos(x)")

    print(f"Funktion: {f.term()}")
    print(f"Erste Ableitung: {f.ableitung().term()}")

    # Alte Methode
    try:
        alte_extrema = f.extremstellen()
        print(f"Alte extremstellen(): {alte_extrema}")
    except Exception as e:
        print(f"Fehler bei alter Methode: {e}")

    # Neue Methode - sollte mehr Lösungen liefern!
    try:
        neue_extrema = f.extremstellen_optimiert()
        print(f"Neue extremstellen_optimiert():")
        for extremum in neue_extrema:
            print(f"  {extremum}")
    except Exception as e:
        print(f"Fehler bei neuer Methode: {e}")


def test_parametrisierte_funktion():
    """Test mit parametrisierter Funktion ax² + bx + c"""
    print("\n=== Test 3: Parametrisierte Funktion ===")
    f = Funktion("a*x^2 + b*x + c")

    print(f"Funktion: {f.term()}")
    print(f"Erste Ableitung: {f.ableitung().term()}")

    # Alte Methode
    try:
        alte_extrema = f.extremstellen()
        print(f"Alte extremstellen(): {alte_extrema}")
    except Exception as e:
        print(f"Fehler bei alter Methode: {e}")

    # Neue Methode
    try:
        neue_extrema = f.extremstellen_optimiert()
        print(f"Neue extremstellen_optimiert():")
        for extremum in neue_extrema:
            print(f"  {extremum}")
    except Exception as e:
        print(f"Fehler bei neuer Methode: {e}")


def test_vielfachheit():
    """Test mit Funktion, die mehrfache Nullstellen in der Ableitung hat"""
    print("\n=== Test 4: Vielfachheit ===")
    f = Funktion("x^4 - 4x^3 + 6x^2")

    print(f"Funktion: {f.term()}")
    print(f"Erste Ableitung: {f.ableitung().term()}")

    # Prüfe die Nullstellen der Ableitung
    f_strich = f.ableitung()
    nullstellen_f_strich = f_strich.nullstellen()
    print(f"Nullstellen der Ableitung: {nullstellen_f_strich}")

    # Alte Methode
    try:
        alte_extrema = f.extremstellen()
        print(f"Alte extremstellen(): {alte_extrema}")
    except Exception as e:
        print(f"Fehler bei alter Methode: {e}")

    # Neue Methode
    try:
        neue_extrema = f.extremstellen_optimiert()
        print(f"Neue extremstellen_optimiert():")
        for extremum in neue_extrema:
            print(f"  {extremum}")
    except Exception as e:
        print(f"Fehler bei neuer Methode: {e}")


def test_kompatibilitaets_methoden():
    """Test der Kompatibilitäts-Methoden"""
    print("\n=== Test 5: Kompatibilitäts-Methoden ===")
    f = Funktion("x^2 - 4x + 3")

    print(f"Funktion: {f.term()}")

    # Teste verschiedene Methoden
    try:
        methoden = [
            ("extremstellen()", lambda: f.extremstellen()),
            ("Extremstellen()", lambda: f.Extremstellen()),
            ("extremstellen_optimiert()", lambda: f.extremstellen_optimiert()),
            ("extrema_mit_wiederholungen()", lambda: f.extrema_mit_wiederholungen()),
        ]

        for name, methode in methoden:
            try:
                result = methode()
                print(f"{name}: {result}")
            except Exception as e:
                print(f"Fehler bei {name}: {e}")

    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")


if __name__ == "__main__":
    print("Test der neuen extremstellen_optimiert() Methode")
    print("=" * 50)

    test_standard_polynom()
    test_trigonometrische_funktion()
    test_parametrisierte_funktion()
    test_vielfachheit()
    test_kompatibilitaets_methoden()

    print("\n" + "=" * 50)
    print("Test abgeschlossen!")
