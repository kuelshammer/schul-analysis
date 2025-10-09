#!/usr/bin/env python3
"""
Test-Script für Taylorpolynom und Tangente Funktionalität mit Zeichne()
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_mathematik.analysis.api import *
from schul_mathematik.analysis.funktion import Funktion


def test_taylor_tangente_zeichnen():
    """Testet, ob Taylorpolynom und Tangente mit Zeichne() funktionieren"""

    print("=== Test: Taylorpolynom und Tangente mit Zeichne() ===\n")

    # Test 1: Tangente mit Zeichne()
    print("1. Test: Tangente an x² bei x=1 und zeichnen")
    f = ErstellePolynom([1, 0, 0])  # x²
    try:
        t = Tangente(f, 1)
        print(f"✅ Tangente erstellt: {t.term()}")
        print(f"   Typ: {type(t)}")

        # Teste, ob es gezeichnet werden kann
        fig = Zeichne(t, x_bereich=(-2, 4), anzeigen=False)
        print("✅ Tangente kann gezeichnet werden")

        # Teste Werte
        print(f"   t(0) = {t(0)}")  # Sollte -1 sein
        print(f"   t(1) = {t(1)}")  # Sollte 1 sein
        print(f"   t(2) = {t(2)}")  # Sollte 3 sein

    except Exception as e:
        print(f"❌ Fehler bei Tangente: {e}")
        import traceback

        traceback.print_exc()

    # Test 2: Taylorpolynom mit Zeichne()
    print("\n2. Test: Taylorpolynom für sin(x) (Grad 3) und zeichnen")
    try:
        g = Funktion("sin(x)")
        taylor = Taylorpolynom(g, grad=3)
        print(f"✅ Taylorpolynom erstellt: {taylor.term()}")
        print(f"   Typ: {type(taylor)}")

        # Teste, ob es gezeichnet werden kann
        fig = Zeichne(taylor, x_bereich=(-3, 3), anzeigen=False)
        print("✅ Taylorpolynom kann gezeichnet werden")

        # Teste Werte
        print(f"   t(0) = {taylor(0)}")  # Sollte 0 sein
        print(f"   t(1) = {taylor(1)}")  # Sollte ca. 0.833 sein (1 - 1/6)
        print(f"   t(-1) = {taylor(-1)}")  # Sollte ca. -0.833 sein

    except Exception as e:
        print(f"❌ Fehler bei Taylorpolynom: {e}")
        import traceback

        traceback.print_exc()

    # Test 3: Vergleich Original und Approximation
    print("\n3. Test: Vergleich sin(x) und Taylorpolynom (Grad 3)")
    try:
        g = Funktion("sin(x)")
        taylor = Taylorpolynom(g, grad=3)

        # Beide zusammen zeichnen
        fig = Zeichne(g, taylor, x_bereich=(-3, 3), anzeigen=False)
        print("✅ Original und Taylorpolynom können zusammen gezeichnet werden")

        # Werte vergleichen
        x_test = 0.5
        original_wert = g(x_test)
        taylor_wert = taylor(x_test)
        print(
            f"   Bei x={x_test}: sin(x) = {original_wert:.4f}, Taylor = {taylor_wert:.4f}"
        )

    except Exception as e:
        print(f"❌ Fehler beim Vergleich: {e}")

    # Test 4: Taylorpolynom mit Entwicklungspunkt
    print("\n4. Test: Taylorpolynom für x² bei x=1 (Grad 2)")
    try:
        f = ErstellePolynom([1, 0, 0])  # x²
        taylor = Taylorpolynom(f, grad=2, entwicklungspunkt=1)
        print(f"✅ Taylorpolynom bei x=1: {taylor.term()}")
        print(f"   Typ: {type(taylor)}")

        # Teste, ob es gezeichnet werden kann
        fig = Zeichne(f, taylor, x_bereich=(-1, 3), anzeigen=False)
        print("✅ Original und Taylorpolynom können gezeichnet werden")

        # Teste, ob sie am Entwicklungspunkt übereinstimmen
        print(f"   f(1) = {f(1)}, taylor(1) = {taylor(1)}")

    except Exception as e:
        print(f"❌ Fehler bei Taylorpolynom mit Entwicklungspunkt: {e}")

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_taylor_tangente_zeichnen()
