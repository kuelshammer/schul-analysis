#!/usr/bin/env python3
"""
Teste das Problem mit symbolischen Nullstellen bei parametrisierten Funktionen
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import GanzrationaleFunktion


def test_nullstellen_mit_parametern():
    """Testet die Berechnung von symbolischen Nullstellen"""
    print("=== Test: Symbolische Nullstellen mit Parametern ===")

    # Erstelle Funktion mit Parametern
    g = GanzrationaleFunktion("a x^2 + 1")
    print(f"Funktion: {g.term()}")
    print(f"Variable: {[v.name for v in g.variablen]}")
    print(f"Parameter: {[p.name for p in g.parameter]}")
    print(f"Grad: {g.grad()}")
    print()

    # Versuche, Nullstellen zu berechnen
    print("Versuche g.nullstellen() aufzurufen...")
    try:
        nullstellen = g.nullstellen()
        print(f"Ergebnis: {nullstellen}")
        print(f"Typ: {type(nullstellen)}")
        if nullstellen:
            for i, ns in enumerate(nullstellen):
                print(f"  Nullstelle {i + 1}: {ns} (Typ: {type(ns)})")
        else:
            print("  Keine Nullstellen gefunden")
    except Exception as e:
        print(f"Fehler: {e}")
        import traceback

        traceback.print_exc()

    print()

    # Teste mit konkreten Werten
    print("Teste mit konkreten Parameterwerten:")
    print("Setze a = 1...")
    # Da wir keine mit_wert() Methode haben, erstellen wir eine neue Funktion
    g_konkret = GanzrationaleFunktion("1*x^2 + 1")
    print(f"Konkrete Funktion: {g_konkret.term()}")
    try:
        nullstellen_konkret = g_konkret.nullstellen()
        print(f"Nullstellen: {nullstellen_konkret}")
    except Exception as e:
        print(f"Fehler bei konkreten Nullstellen: {e}")


def test_analyse_des_problems():
    """Analysiert das Problem Schritt für Schritt"""
    print("\n=== Analyse des Problems ===")

    # Erstelle Funktion
    g = GanzrationaleFunktion("a x^2 + 1")
    print(f"Term als SymPy: {g.term_sympy}")
    print(f"Term-Typ: {type(g.term_sympy)}")
    print(f"Hauptvariable: {g.hauptvariable.name if g.hauptvariable else 'None'}")
    print()

    # Teste manuelle Berechnung mit SymPy
    import sympy as sp

    print("Manuelle Berechnung mit SymPy:")

    # Extrahiere Symbole
    if g.hauptvariable:
        x = g.hauptvariable.symbol
        print(f"Variable x: {x}")

        # Berechne Nullstellen manuell
        try:
            manual_solution = sp.solve(g.term_sympy, x)
            print(f"Manuelle Lösung: {manual_solution}")
            print(f"Typ der Lösung: {type(manual_solution)}")
        except Exception as e:
            print(f"Fehler bei manueller Lösung: {e}")

    print()

    # Teste die verwendete nullstellen()-Methode
    print("Untersuche die nullstellen()-Methode:")
    try:
        # Direkter Zugriff auf die Methode
        nullstellen = g.nullstellen()
        print(f"nullstellen() liefert: {nullstellen}")
    except Exception as e:
        print(f"nullstellen() schlägt fehl: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_nullstellen_mit_parametern()
    test_analyse_des_problems()
