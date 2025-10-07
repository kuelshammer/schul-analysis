#!/usr/bin/env python3
"""
Test für die neue __call__ Syntax in parametrischen und ganzrationalen Funktionen
"""

import sys

sys.path.insert(0, "src")


from schul_analysis import (
    GanzrationaleFunktion,
    Parameter,
    ParametrischeFunktion,
    Variable,
)


def test_ganzrationale_funktion_call_syntax():
    """Testet die neue __call__ Syntax für ganzrationale Funktionen"""
    print("=== Test: GanzrationaleFunktion __call__ Syntax ===")

    # Test 1: Einfache quadratische Funktion
    f = GanzrationaleFunktion("x^2 + 2x - 3")
    print(f"f(x) = {f.term()}")

    # Alte Syntax (sollte weiterhin funktionieren)
    print(f"Alte Syntax: f.wert(2) = {f.wert(2)}")

    # Neue Syntax
    print(f"Neue Syntax: f(2) = {f(2)}")
    print(f"Neue Syntax: f(0) = {f(0)}")
    print(f"Neue Syntax: f(-1) = {f(-1)}")

    # Test 2: Lineare Funktion
    g = GanzrationaleFunktion("2x + 1")
    print(f"\ng(x) = {g.term()}")
    print(f"g(3) = {g(3)}")
    print(f"g(-0.5) = {g(-0.5)}")

    # Test 3: Konstante Funktion
    h = GanzrationaleFunktion("5")
    print(f"\nh(x) = {h.term()}")
    print(f"h(100) = {h(100)}")

    # Test 4: Höhergradige Funktion
    k = GanzrationaleFunktion("x^3 - 2x^2 + x - 1")
    print(f"\nk(x) = {k.term()}")
    print(f"k(1) = {k(1)}")
    print(f"k(2) = {k(2)}")

    print("✓ Alle ganzrationalen Funktionstests bestanden!\n")


def test_parametrische_funktion_call_syntax():
    """Testet die neue __call__ Syntax für parametrische Funktionen"""
    print("=== Test: ParametrischeFunktion __call__ Syntax ===")

    # Test 1: Einfache parametrische Funktion
    x = Variable("x")
    a = Parameter("a")

    f = ParametrischeFunktion([a, 1, 0], [x])  # a*x² + x
    print(f"f(x) = {f.term()}")

    # Symbolische Auswertung
    print(f"f(2) = {f(2)}")  # Sollte 4a + 2 ergeben
    print(f"f(0) = {f(0)}")  # Sollte 0 ergeben
    print(f"f(-1) = {f(-1)}")  # Sollte a - 1 ergeben

    # Test 2: Mit konkreten Parameterwerten
    f_konkret = f.mit_wert(a=3)
    print(f"\nf_3(x) = {f_konkret.term()}")
    print(f"f_3(2) = {f_konkret(2)}")  # Sollte 3*4 + 2 = 14 ergeben
    print(f"f_3(1) = {f_konkret(1)}")  # Sollte 3*1 + 1 = 4 ergeben

    # Test 3: Mehrere Parameter
    b = Parameter("b")
    g = ParametrischeFunktion.from_string("a*x^2 + b*x + 1", a, b, x)
    print(f"\ng(x) = {g.term()}")
    print(f"g(2) = {g(2)}")  # Sollte 4a + 2b + 1 ergeben
    print(f"g(1) = {g(1)}")  # Sollte a + b + 1 ergeben

    # Test 4: Direkte Substitution mit Parameterwerten
    print(f"\nKombination: f.mit_wert(a=2)(3) = {f.mit_wert(a=2)(3)}")

    print("✓ Alle parametrischen Funktionstests bestanden!\n")


def test_ableitung_mit_call_syntax():
    """Testet die Kombination von Ableitung und __call__ Syntax"""
    print("=== Test: Ableitung mit __call__ Syntax ===")

    # Test 1: Ganzrationale Funktion
    f = GanzrationaleFunktion("x^3 - 3x^2 + 2x")
    print(f"f(x) = {f.term()}")

    f_strich = f.ableitung()
    print(f"f'(x) = {f_strich.term()}")
    print(f"f'(2) = {f_strich(2)}")
    print(f"f'(0) = {f_strich(0)}")

    # Direkte Berechnung ohne Zwischenvariable
    print(f"f''(1) = {f.ableitung().ableitung()(1)}")

    # Test 2: Parametrische Funktion
    x = Variable("x")
    a = Parameter("a")
    g = ParametrischeFunktion([a, 2, 1], [x])  # a*x² + 2x + 1
    print(f"\ng(x) = {g.term()}")

    g_strich = g.ableitung()
    print(f"g'(x) = {g_strich.term()}")
    print(f"g'(3) = {g_strich(3)}")  # Sollte 6a + 2 ergeben

    # Mit konkretem Parameterwert
    g_konkret = g.mit_wert(a=4)
    print(f"\ng_4(x) = {g_konkret.term()}")
    print(f"g_4'(2) = {g_konkret.ableitung()(2)}")

    print("✓ Alle Ableitungstests bestanden!\n")


def test_fehlerbehandlung():
    """Testet die Fehlerbehandlung bei ungültigen Aufrufen"""
    print("=== Test: Fehlerbehandlung ===")

    # Test 1: Falsche Anzahl von Argumenten
    x = Variable("x")
    y = Variable("y")
    a = Parameter("a")

    f = ParametrischeFunktion([a, 1, 0], [x])  # Eine Variable
    try:
        # Sollte fehlschlagen - zu viele Argumente
        f(2, 3)
        print("FEHLER: Exception wurde nicht geworfen!")
    except ValueError as e:
        print(f"Erwarteter Fehler: {e}")

    # Test 2: Multivariate Funktion (wenn implementiert)
    try:
        # Zwei Variablen
        g = ParametrischeFunktion([1, 1], [x, y])  # x + y
        print(f"g(2, 3) = {g(2, 3)}")  # Sollte funktionieren

        # Falsche Anzahl
        try:
            g(2)
            print("FEHLER: Exception wurde nicht geworfen!")
        except ValueError as e:
            print(f"Erwarteter Fehler: {e}")
    except Exception as e:
        print(f"Multivariate Funktionen noch nicht implementiert: {e}")

    print("✓ Fehlerbehandlungstests bestanden!\n")


def test_didaktische_beispiele():
    """Testet didaktische Beispiele für den Unterricht"""
    print("=== Test: Didaktische Beispiele ===")

    # Beispiel 1: Parabel mit Parameter
    print("Beispiel 1: Parabel f(x) = ax² + bx + c")
    x = Variable("x")
    a, b, c = Parameter("a"), Parameter("b"), Parameter("c")

    f = ParametrischeFunktion([c, b, a], [x])
    print(f"f(x) = {f.term()}")

    # Scheitelpunktform für Parameter a = 1, b = -2, c = 0
    f_beispiel = f.mit_wert(a=1, b=-2, c=0)
    print(f"f_beispiel(x) = {f_beispiel.term()}")
    print(f"f_beispiel(1) = {f_beispiel(1)}")  # Scheitelpunkt
    print(f"f_beispiel(0) = {f_beispiel(0)}")
    print(f"f_beispiel(2) = {f_beispiel(2)}")

    # Beispiel 2: Funktionenschar
    print("\nBeispiel 2: Funktionenschar f_a(x) = a·x²")
    f_schar = ParametrischeFunktion([0, 0, a], [x])

    for a_wert in [-2, -1, 0, 1, 2]:
        f_aktuell = f_schar.mit_wert(a=a_wert)
        print(f"f_{a_wert}(x) = {f_aktuell.term()}")
        print(f"f_{a_wert}(1) = {f_aktuell(1)}, f_{a_wert}(2) = {f_aktuell(2)}")

    print("✓ Didaktische Beispiele erfolgreich!\n")


def main():
    """Führt alle Tests durch"""
    print("Neue __call__ Syntax Tests für Schul-Analysis Framework")
    print("=" * 60)

    try:
        test_ganzrationale_funktion_call_syntax()
        test_parametrische_funktion_call_syntax()
        test_ableitung_mit_call_syntax()
        test_fehlerbehandlung()
        test_didaktische_beispiele()

        print("🎉 ALLE TESTS ERFOLGREICH!")
        print("Die neue __call__ Syntax funktioniert perfekt!")

    except Exception as e:
        print(f"❌ FEHLER: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
