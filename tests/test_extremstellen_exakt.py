#!/usr/bin/env python3
"""
Test für exakte Extremstellen-Berechnung

Dieser Test überprüft, dass Extremstellen() exakte symbolische Ergebnisse liefert
und nicht fälschlicherweise zu Floats rundet.
"""

import os
import sys

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import sympy as sp

from schul_mathematik import Extremstellen, Funktion


def test_extremstellen_parametrisiert():
    """Test: Extremstellen bei parametrisierten Funktionen bleiben exakt"""
    print("=== Test 1: Parametrisierte Funktion ===")

    # f(x) = a*x² + x
    f = Funktion("a*x^2 + x")
    print(f"Funktion: {f.term()}")

    extremstellen = Extremstellen(f)
    print(f"Extremstellen: {extremstellen}")

    # Sollte symbolisches Ergebnis liefern
    assert len(extremstellen) == 1, (
        f"Erwartete 1 Extremstelle, got {len(extremstellen)}"
    )

    x_wert, y_wert, art = extremstellen[0]
    print(f"x_wert: {x_wert} (Typ: {type(x_wert)})")
    print(f"y_wert: {y_wert} (Typ: {type(y_wert)})")
    print(f"Art: {art}")

    # Sollte symbolischer Ausdruck sein, kein Float
    assert not isinstance(x_wert, float), (
        f"x_wert sollte kein Float sein, got {type(x_wert)}"
    )
    assert hasattr(x_wert, "free_symbols"), "x_wert sollte SymPy-Ausdruck sein"

    # Überprüfe, dass der Parameter a enthalten ist
    assert sp.Symbol("a") in x_wert.free_symbols, (
        "Parameter a sollte im Ergebnis enthalten sein"
    )

    print("✅ Parametrisierte Extremstellen bleiben exakt\n")


def test_extremstellen_numerisch_exakt():
    """Test: Extremstellen bei numerischen Funktionen bleiben exakt (Brüche)"""
    print("=== Test 2: Numerische Funktion mit Bruch-Ergebnis ===")

    # f(x) = 2x² - x
    f = Funktion("2*x^2 - x")
    print(f"Funktion: {f.term()}")

    extremstellen = Extremstellen(f)
    print(f"Extremstellen: {extremstellen}")

    # Sollte 1 Extremstelle bei x = 1/4 haben
    assert len(extremstellen) == 1, (
        f"Erwartete 1 Extremstelle, got {len(extremstellen)}"
    )

    x_wert, y_wert, art = extremstellen[0]
    print(f"x_wert: {x_wert} (Typ: {type(x_wert)})")
    print(f"Art: {art}")

    # Sollte exakt 1/4 sein, nicht 0.25
    expected = sp.Rational(1, 4)
    assert x_wert == expected, f"Erwartete 1/4, got {x_wert}"

    print("✅ Numerische Extremstellen bleiben als Bruch exakt\n")


def test_extremstellen_reine_zahl():
    """Test: Extremstellen bei reinen Zahlen werden zu Floats"""
    print("=== Test 3: Funktion mit reinem Zahl-Ergebnis ===")

    # f(x) = x² - 4x + 3
    f = Funktion("x^2 - 4*x + 3")
    print(f"Funktion: {f.term()}")

    extremstellen = Extremstellen(f)
    print(f"Extremstellen: {extremstellen}")

    # Sollte 1 Extremstelle bei x = 2 haben
    assert len(extremstellen) == 1, (
        f"Erwartete 1 Extremstelle, got {len(extremstellen)}"
    )

    x_wert, y_wert, art = extremstellen[0]
    print(f"x_wert: {x_wert} (Typ: {type(x_wert)})")
    print(f"Art: {art}")

    # Sollte exakte Ganzzahl sein (wird nicht mehr zu Float konvertiert)
    assert isinstance(x_wert, sp.Integer), (
        f"x_wert sollte SymPy Integer sein, got {type(x_wert)}"
    )
    assert x_wert == 2, f"Erwartete 2, got {x_wert}"

    print("✅ Reine Zahlen werden als exakte SymPy Integers beibehalten\n")


def test_extremstellen_komplex():
    """Test: Komplexere Funktion mit Wurzel-Ergebnis"""
    print("=== Test 4: Funktion mit Wurzel-Ergebnis ===")

    # f(x) = x² - 2x - 1
    f = Funktion("x^2 - 2*x - 1")
    print(f"Funktion: {f.term()}")

    extremstellen = Extremstellen(f)
    print(f"Extremstellen: {extremstellen}")

    # Sollte 1 Extremstelle bei x = 1 haben
    assert len(extremstellen) == 1, (
        f"Erwartete 1 Extremstelle, got {len(extremstellen)}"
    )

    x_wert, y_wert, art = extremstellen[0]
    print(f"x_wert: {x_wert} (Typ: {type(x_wert)})")
    print(f"Art: {art}")

    # Sollte exakte Ganzzahl sein (reine Zahl 1)
    assert isinstance(x_wert, sp.Integer), (
        f"x_wert sollte SymPy Integer sein, got {type(x_wert)}"
    )
    assert x_wert == 1, f"Erwartete 1, got {x_wert}"

    print("✅ Ganzzahl-Ergebnisse werden als exakte SymPy Integers beibehalten\n")


def test_extremstellen_mehrere_parameter():
    """Test: Funktion mit mehreren Parametern"""
    print("=== Test 5: Funktion mit mehreren Parametern ===")

    # f(x) = a*x² + b*x + c
    f = Funktion("a*x^2 + b*x + c")
    print(f"Funktion: {f.term()}")

    extremstellen = Extremstellen(f)
    print(f"Extremstellen: {extremstellen}")

    # Sollte 1 Extremstelle haben
    assert len(extremstellen) == 1, (
        f"Erwartete 1 Extremstelle, got {len(extremstellen)}"
    )

    x_wert, y_wert, art = extremstellen[0]
    print(f"x_wert: {x_wert} (Typ: {type(x_wert)})")
    print(f"Art: {art}")

    # Sollte symbolischer Ausdruck mit Parametern a und b sein
    assert not isinstance(x_wert, float), (
        f"x_wert sollte kein Float sein, got {type(x_wert)}"
    )
    assert hasattr(x_wert, "free_symbols"), "x_wert sollte SymPy-Ausdruck sein"

    # Überprüfe, dass die Parameter a und b enthalten sind
    symbols = x_wert.free_symbols
    assert sp.Symbol("a") in symbols, "Parameter a sollte im Ergebnis enthalten sein"
    assert sp.Symbol("b") in symbols, "Parameter b sollte im Ergebnis enthalten sein"

    print("✅ Mehrere Parameter werden korrekt behandelt\n")


if __name__ == "__main__":
    print("Test der exakten Extremstellen-Berechnung\n")

    test_extremstellen_parametrisiert()
    test_extremstellen_numerisch_exakt()
    test_extremstellen_reine_zahl()
    test_extremstellen_komplex()
    test_extremstellen_mehrere_parameter()

    print("✅ Alle Tests bestanden! Extremstellen bleiben exakt.")
