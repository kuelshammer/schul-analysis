#!/usr/bin/env python3
"""
Test-Skript für die neue Prime-Notation: f' = Ableitung(f)
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import (
    Ableitung,
    GanzrationaleFunktion,
    ParametrischeFunktion,
    Variable,
)


def test_prime_syntax_ganzrational():
    """Testet die Prime-Syntax mit ganzrationalen Funktionen"""
    print("=== Test mit ganzrationalen Funktionen ===")

    # Erste Ableitung
    print("1. Erste Ableitung:")
    f = GanzrationaleFunktion("x^2 + 3x - 2")
    print(f"   f(x) = {f}")

    f_strich = Ableitung(f)  # f' = 2x + 3
    print(f"   f'(x) = {f_strich}")

    ergebnis = f_strich(2)  # Sollte 2*2 + 3 = 7 sein
    print(f"   f'(2) = {ergebnis}")
    print("   Erwartet: 7")
    print("   ✅ Korrekt!" if ergebnis == 7 else "   ❌ Fehler!")

    print()

    # Zweite Ableitung
    print("2. Zweite Ableitung:")
    f_zwei_strich = Ableitung(f_strich)  # f'' = 2
    print(f"   f''(x) = {f_zwei_strich}")

    ergebnis2 = f_zwei_strich(5)  # Sollte 2 sein
    print(f"   f''(5) = {ergebnis2}")
    print("   Erwartet: 2")
    print("   ✅ Korrekt!" if ergebnis2 == 2 else "   ❌ Fehler!")

    print()

    # Direkte zweite Ableitung
    print("3. Direkte zweite Ableitung:")
    f2_strich = Ableitung(f, 2)  # Alternativ: Ableitung(f, ordnung=2)
    print(f"   f''(x) direkt = {f2_strich}")
    print(f"   f''(5) direkt = {f2_strich(5)}")
    print("   ✅ Korrekt!" if f2_strich(5) == 2 else "   ❌ Fehler!")

    print()


def test_prime_syntax_parametrisch():
    """Testet die Prime-Syntax mit parametrischen Funktionen"""
    print("=== Test mit parametrischen Funktionen ===")

    # Erste Ableitung
    print("1. Erste Ableitung:")
    t = Variable("t")
    g = ParametrischeFunktion("t^2 + 2*t", t)
    print(f"   g(t) = {g}")

    g_strich = Ableitung(g)  # g' = 2t + 2
    print(f"   g'(t) = {g_strich}")

    ergebnis = g_strich(3)  # Sollte 2*3 + 2 = 8 sein
    print(f"   g'(3) = {ergebnis}")
    print("   Erwartet: 8")
    print("   ✅ Korrekt!" if ergebnis == 8 else "   ❌ Fehler!")

    print()

    # Zweite Ableitung
    print("2. Zweite Ableitung:")
    g_zwei_strich = Ableitung(g_strich)  # g'' = 2
    print(f"   g''(t) = {g_zwei_strich}")

    ergebnis2 = g_zwei_strich(7)  # Sollte 2 sein
    print(f"   g''(7) = {ergebnis2}")
    print("   Erwartet: 2")
    print("   ✅ Korrekt!" if ergebnis2 == 2 else "   ❌ Fehler!")

    print()


def test_komplexeres_beispiel():
    """Testet mit komplexeren Funktionen"""
    print("=== Komplexeres Beispiel ===")

    # Kubische Funktion
    h = GanzrationaleFunktion("x^3 - 2x^2 + 5x - 1")
    print(f"   h(x) = {h}")

    h_strich = Ableitung(h)  # h' = 3x² - 4x + 5
    print(f"   h'(x) = {h_strich}")

    h_zwei_strich = Ableitung(h_strich)  # h'' = 6x - 4
    print(f"   h''(x) = {h_zwei_strich}")

    h_drei_strich = Ableitung(h_zwei_strich)  # h''' = 6
    print(f"   h'''(x) = {h_drei_strich}")

    # Testwerte
    print(f"   h(1) = {h(1)}")
    print(f"   h'(1) = {h_strich(1)}")  # 3-4+5 = 4
    print(f"   h''(1) = {h_zwei_strich(1)}")  # 6-4 = 2
    print(f"   h'''(1) = {h_drei_strich(1)}")  # 6

    print()


def test_mathematische_notation():
    """Demonstriert die mathematische Notation im Vergleich"""
    print("=== Mathematische Notation Vergleich ===")

    # Mathematisch: f(x) = x² + 3x - 2
    #               f'(x) = 2x + 3
    #               f''(x) = 2

    f = GanzrationaleFunktion("x^2 + 3x - 2")
    f_strich = Ableitung(f)
    f_zwei_strich = Ableitung(f_strich)

    print("   Mathematisch: f(x) = x² + 3x - 2")
    print("   Python Code:  f = GanzrationaleFunktion('x^2 + 3x - 2')")
    print(f"   Ergebnis:     f(x) = {f}")
    print()

    print("   Mathematisch: f'(x) = 2x + 3")
    print("   Python Code:  f_strich = Ableitung(f)")
    print(f"   Ergebnis:     f'(x) = {f_strich}")
    print()

    print("   Mathematisch: f''(x) = 2")
    print("   Python Code:  f_zwei_strich = Ableitung(f_strich)")
    print(f"   Ergebnis:     f''(x) = {f_zwei_strich}")
    print()

    print("   Mathematisch: f'(2) = 2·2 + 3 = 7")
    print("   Python Code:  f_strich(2)")
    print(f"   Ergebnis:     f'(2) = {f_strich(2)}")
    print()


if __name__ == "__main__":
    print("🎯 Prime-Notation Test: f' = Ableitung(f)")
    print("=" * 50)
    print()

    test_prime_syntax_ganzrational()
    test_prime_syntax_parametrisch()
    test_komplexeres_beispiel()
    test_mathematische_notation()

    print("🎉 Alle Tests abgeschlossen!")
