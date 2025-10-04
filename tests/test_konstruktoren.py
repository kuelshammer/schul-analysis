#!/usr/bin/env python3
"""
Test-Skript für verschiedene Konstruktor-Formate
Analysiert, was mit unterschiedlichen String-Eingaben passiert.
"""

import sympy as sp
from sympy import sympify


def test_konstruktoren():
    """Testet verschiedene String-Eingaben für ganzrationale Funktionen"""

    # Test-Eingaben
    test_strings = [
        "x^2+4x-2",  # Standard
        "$x^2+4x-2$",  # LaTeX-Format
        "x**2+4*x-2",  # Python-Syntax
        "x^2 + 4x - 2",  # Mit Leerzeichen
        "2*x^2 - 3*x + 1",  # Mit Koeffizienten vor x
        "x^3 - 2*x^2 + 5",  # Kubisch
        "-x^2 + 3x - 1",  # Negativer führender Koeffizient
        "x^2 + x + 1",  # Koeffizient 1
        "x^2 - 1",  # Ohne x-Term
        "5",  # Konstante
    ]

    x = sp.symbols("x")

    print("=== TEST VERSCHIEDENER KONSTRUKTOR-FORMATE ===\n")

    for i, test_str in enumerate(test_strings, 1):
        print(f"{i:2d}. Eingabe: '{test_str}'")

        try:
            # Versuch mit sympify
            result = sympify(test_str)
            print(f"    → SymPy-Erfolg: {result}")
            print(f"    → LaTeX: {sp.latex(result)}")

            # Test ob es eine ganzrationale Funktion ist
            if result.is_polynomial(x):
                print("    → Polynomial: Ja")

                # Koeffizienten extrahieren
                from sympy import Poly

                try:
                    poly = Poly(result, x)
                    coeffs = [float(poly.coeff(i)) for i in range(poly.degree() + 1)]
                    print(f"    → Koeffizienten: {coeffs}")
                except Exception:
                    print("    → Koeffizienten: Fehler bei Extraktion")
            else:
                print("    → Polynomial: Nein")

        except Exception as e:
            print(f"    → SymPy-Fehler: {e}")

            # Versuch mit Bereinigung
            try:
                cleaned = test_str.replace("$", "").replace("**", "^")
                result = sympify(cleaned)
                print(f"    → Bereinigt: '{cleaned}' → {result}")
            except Exception as e2:
                print(f"    → Auch nach Bereinigung: {e2}")

        print()


def test_liste_vs_dict():
    """Vergleicht Listen- und Dictionary-Konstruktoren"""

    print("=== VERGLEICH LISTE vs DICTIONARY ===\n")

    # Beispiel: x^2 - 4x + 3
    print("1. Listen-Konstruktor:")
    liste_funktion = [1, -4, 3]  # 1*x^2 - 4*x^1 + 3*x^0
    print("   [1, -4, 3] → 1x² - 4x + 3")

    print("\n2. Dictionary-Konstruktor:")
    dict_funktion = {2: 1, 1: -4, 0: 3}  # x^2 - 4x + 3
    print("   {2: 1, 1: -4, 0: 3} → 1x² - 4x + 3")

    print("\n3. Alternative Dictionary-Konstruktor:")
    dict_funktion2 = {0: 3, 1: -4, 2: 1}  # Reihenfolge egal
    print("   {0: 3, 1: -4, 2: 1} → 3 - 4x + x²")

    print("\n4. Dictionary mit Lücken:")
    dict_funktion3 = {3: 2, 1: -3, 0: 1}  # 2x^3 - 3x + 1
    print("   {3: 2, 1: -3, 0: 1} → 2x³ - 3x + 1")


def test_edge_cases():
    """Testet Edge Cases für Konstruktoren"""

    print("\n=== EDGE CASES ===\n")

    edge_cases = [
        ("0", "Null-Funktion"),
        ("x", "Lineare Funktion ohne Koeffizient"),
        ("2x", "Lineare Funktion ohne Exponent"),
        ("x^0", "x^0 = 1"),
        ("1*x^1 + 2*x^0", "Explizite Schreibweise"),
        ("(x+1)(x-2)", "Faktorisierte Form"),
        ("x^2 + 0*x + 1", "Null-Koeffizient"),
    ]

    x = sp.symbols("x")

    for test_str, description in edge_cases:
        print(f"{description}: '{test_str}'")
        try:
            result = sympify(test_str)
            print(f"   → {result}")
            print(f"   → Polynomial: {result.is_polynomial(x)}")
        except Exception as e:
            print(f"   → Fehler: {e}")
        print()


if __name__ == "__main__":
    test_konstruktoren()
    test_liste_vs_dict()
    test_edge_cases()
