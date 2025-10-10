#!/usr/bin/env python3
"""
Test für QuotientFunktion Nullstellen-Implementierung.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.strukturiert import QuotientFunktion
from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion
import sympy as sp


def test_quotient_funktion_einfach():
    """Teste einfache Quotientenfunktion."""
    print("=== Test: QuotientFunktion einfach ===")

    # (x-1)/(x-2) - Nullstelle bei x=1, Polstelle bei x=2
    f = QuotientFunktion("(x-1)/(x-2)")

    print(f"Funktion: {f}")
    print(f"Term: {f.term()}")

    # Teste Polstellen
    polstellen = f.polstellen()
    print(f"Polstellen: {polstellen}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Erwartet: Nur x=1, nicht x=2 (weil Polstelle)
    assert len(nullstellen) == 1, f"Erwartete 1 Nullstelle, aber got {len(nullstellen)}"

    # Überprüfe, dass es nicht die Polstelle ist
    for ns in nullstellen:
        x_wert = ns.x if hasattr(ns, "x") else ns
        assert x_wert != 2, f"Nullstelle sollte nicht Polstelle sein: {x_wert}"
        assert x_wert == 1, f"Erwartete Nullstelle x=1, aber got {x_wert}"

    print("✅ Einfacher QuotientFunktion-Test bestanden")


def test_quotient_funktion_mehrfache_nullstellen():
    """Teste Quotientenfunktion mit mehrfachen Nullstellen."""
    print("\n=== Test: QuotientFunktion mehrfache Nullstellen ===")

    # (x-1)²(x-3)/((x-2)(x-1)) - Vereinfacht zu (x-1)(x-3)/(x-2) für x≠1
    # Aber: x=1 ist Polstelle, also nur Nullstelle bei x=3
    zaehler = GanzrationaleFunktion([1, -7, 15, -9])  # (x-1)²(x-3) = x³-7x²+15x-9
    nenner = GanzrationaleFunktion([1, -3, 2])  # (x-1)(x-2) = x²-3x+2
    f = QuotientFunktion([zaehler, nenner])

    print(f"Funktion: {f}")
    print(f"Zähler: {zaehler.term()}")
    print(f"Nenner: {nenner.term()}")

    # Teste Polstellen
    polstellen = f.polstellen()
    print(f"Polstellen: {polstellen}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Erwartet: Nur x=3, nicht x=1 (weil Polstelle)
    assert len(nullstellen) == 1, f"Erwartete 1 Nullstelle, aber got {len(nullstellen)}"

    # Überprüfe, dass es die richtigen Werte sind
    for ns in nullstellen:
        x_wert = ns.x if hasattr(ns, "x") else ns
        assert x_wert != 1, f"Nullstelle sollte nicht Polstelle sein: {x_wert}"
        assert x_wert == 3, f"Erwartete Nullstelle x=3, aber got {x_wert}"

    print("✅ Mehrfache Nullstellen-Test bestanden")


def test_quotient_funktion_keine_nullstellen():
    """Teste Quotientenfunktion ohne Nullstellen."""
    print("\n=== Test: QuotientFunktion keine Nullstellen ===")

    # 1/(x-2) - keine Nullstellen, Polstelle bei x=2
    zaehler = GanzrationaleFunktion([1])  # 1
    nenner = GanzrationaleFunktion([1, -2])  # x-2
    f = QuotientFunktion([zaehler, nenner])

    print(f"Funktion: {f}")
    print(f"Zähler: {zaehler.term()}")
    print(f"Nenner: {nenner.term()}")

    # Teste Polstellen
    polstellen = f.polstellen()
    print(f"Polstellen: {polstellen}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Erwartet: Keine Nullstellen
    assert len(nullstellen) == 0, (
        f"Erwartete keine Nullstellen, aber got {len(nullstellen)}"
    )

    print("✅ Keine Nullstellen-Test bestanden")


def test_quotient_funktion_hybrid_api():
    """Teste Hybrid-API für QuotientFunktion."""
    print("\n=== Test: QuotientFunktion Hybrid-API ===")

    # (x-1)²/(x-2) - doppelte Nullstelle bei x=1, Polstelle bei x=2
    zaehler = GanzrationaleFunktion([1, -2, 1])  # (x-1)²
    nenner = GanzrationaleFunktion([1, -2])  # x-2
    f = QuotientFunktion([zaehler, nenner])

    print(f"Funktion: {f}")

    # Teste strukturierte API
    strukturiert = f.nullstellen()
    print(f"Strukturierte API: {strukturiert}")

    # Teste Hybrid-API
    hybrid = f.nullstellen_mit_wiederholungen()
    print(f"Hybrid-API: {hybrid}")

    # Beide sollten gleiche Anzahl haben (keine Vielfachheit bei Quotienten)
    assert len(strukturiert) == len(hybrid), (
        f"Unterschiedliche Anzahl: {len(strukturiert)} vs {len(hybrid)}"
    )

    print("✅ Hybrid-API-Test bestanden")


if __name__ == "__main__":
    print("Starte QuotientFunktion Nullstellen Tests...\n")

    try:
        test_quotient_funktion_einfach()
        test_quotient_funktion_mehrfache_nullstellen()
        test_quotient_funktion_keine_nullstellen()
        test_quotient_funktion_hybrid_api()

        print("\n🎉 Alle QuotientFunktion Tests erfolgreich bestanden!")

    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
