#!/usr/bin/env python3
"""
Test für die LaTeX-Darstellung in Marimo
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_analysis import Funktion, Term


def test_latex_display():
    """Testet die latex_display Methode"""
    print("Teste latex_display() Methode...")

    # Teste verschiedene Funktionen
    test_funktionen = [
        "x^2 + 2*x + 1",
        "sin(x) + cos(x)",
        "exp(x) + 1",
        "x^3 - 3*x^2 + 2*x",
        "(x+1)/(x-1)",
    ]

    for term in test_funktionen:
        try:
            f = Funktion(term)
            latex_str = f.latex_display()
            print(f"f(x) = {term}")
            print(f"LaTeX: {latex_str}")
            print()
        except Exception as e:
            print(f"Fehler bei {term}: {e}")
            print()


def test_term_wrapper():
    """Testet die Term() Wrapper-Funktion"""
    print("Teste Term() Wrapper...")

    f = Funktion("x^2 + 2*x + 1")

    try:
        # Teste ohne Marimo
        result = Term(f)
        print(f"Term(f) Ergebnis: {result}")
        print(f"Typ: {type(result)}")
    except Exception as e:
        print(f"Fehler bei Term(): {e}")


def test_symypy_compatibility():
    """Testet, dass arithmetische Operationen noch funktionieren"""
    print("Teste SymPy-Kompatibilität...")

    f = Funktion("x^2")
    g = Funktion("2*x + 1")

    try:
        # Teste Addition
        h = f + g
        print(f"f + g = {h.term()}")

        # Teste, dass es noch ein SymPy-Objekt ist
        print(f"Typ von f + g: {type(h)}")

    except Exception as e:
        print(f"Fehler bei arithmetischer Operation: {e}")


if __name__ == "__main__":
    print("=== LaTeX-Darstellung Tests ===")
    print()

    test_latex_display()
    print()
    test_term_wrapper()
    print()
    test_symypy_compatibility()

    print("=== Tests abgeschlossen ===")
