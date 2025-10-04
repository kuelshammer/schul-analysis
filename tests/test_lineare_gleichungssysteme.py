#!/usr/bin/env python3
"""
Test für lineare Gleichungssysteme
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import (
    LGS,
    Variable,
    Parameter,
    ParametrischeFunktion,
    interpolationspolynom,
    plotte_loesung,
)


def test_lgs_basics():
    """Test grundlegende LGS-Funktionalität"""
    print("=== Test LGS Grundfunktionalität ===")

    # Erstelle Variable und Parameter
    x = Variable("x")
    a, b, c = Parameter("a"), Parameter("b"), Parameter("c")

    # Erstelle parametrische Funktion f(x) = ax² + bx + c
    f = ParametrischeFunktion([a, b, c], [x])

    # Erstelle Bedingungen: f(3) = 4, f(2) = 0, f'(0) = 0
    bedingungen = [f(3) == 4, f(2) == 0, f.ableitung()(0) == 0]

    # Erstelle LGS
    lgs = LGS(*bedingungen)

    print(f"Gleichungssystem: {lgs}")
    print(f"Anzahl Gleichungen: {lgs.anzahl_gleichungen}")
    print(f"Anzahl Parameter: {lgs.anzahl_parameter}")

    # Zeige Details
    lgs.zeige_gleichungen()
    lgs.zeige_unbekannte()

    # Löse das System
    try:
        lösung = lgs.löse()
        print(f"Lösung: {lösung}")

        # Verifiziere die Lösung
        f_konkret = f.mit_wert(**{str(p): v for p, v in lösung.items()})
        print(f"Gefundene Funktion: f(x) = {f_konkret.term()}")

        # Teste die Bedingungen
        print("\nVerifikation:")
        print(f"f(3) = {f_konkret.wert(3)} (erwartet: 4)")
        print(f"f(2) = {f_konkret.wert(2)} (erwartet: 0)")
        print(f"f'(0) = {f_konkret.ableitung().wert(0)} (erwartet: 0)")

    except Exception as e:
        print(f"Fehler beim Lösen: {e}")


def test_interpolation():
    """Test Interpolationspolynom-Funktionalität"""
    print("\n=== Test Interpolationspolynom ===")

    # Teste mit 3 Punkten (Parabel)
    punkte = [(1, 2), (2, 3), (3, 6)]

    try:
        f = interpolationspolynom(punkte)
        print(f"Interpolationspolynom: {f.term()}")

        # Verifiziere
        print("\nVerifikation:")
        for x, y_erwartet in punkte:
            y_berechnet = f.wert(x)
            print(f"f({x}) = {y_berechnet:.6f} ≈ {y_erwartet}")

    except Exception as e:
        print(f"Fehler bei Interpolation: {e}")


def test_lgs_fehlerbehandlung():
    """Test Fehlerbehandlung"""
    print("\n=== Test Fehlerbehandlung ===")

    # Erstelle widersprüchliches System
    x = Variable("x")
    a, b = Parameter("a"), Parameter("b")
    f = ParametrischeFunktion([a, b], [x])

    # Widersprüchliche Bedingungen: f(1) = 5 und f(1) = 10
    try:
        lgs = LGS(f(1) == 5, f(1) == 10)
        lösung = lgs.löse()
        print(f"Unerwartete Lösung: {lösung}")
    except Exception as e:
        print(f"Erwarteter Fehler: {e}")


def test_validierung():
    """Test Validierungsfunktionen"""
    print("\n=== Test Validierung ===")

    # Erstelle System mit zu wenig Gleichungen
    x = Variable("x")
    a, b, c = Parameter("a"), Parameter("b"), Parameter("c")
    f = ParametrischeFunktion([a, b, c], [x])

    lgs = LGS(f(1) == 1, f(2) == 4)  # Nur 2 Gleichungen für 3 Parameter

    warnungen = lgs.validiere_gleichungen()
    print("Validierungswarnungen:")
    for warnung in warnungen:
        print(f"  - {warnung}")


if __name__ == "__main__":
    test_lgs_basics()
    test_interpolation()
    test_lgs_fehlerbehandlung()
    test_validierung()

    print("\n=== Alle Tests abgeschlossen ===")
