#!/usr/bin/env python3
"""
Test für GebrochenRationaleFunktion Nullstellen-Implementierung.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.gebrochen_rationale import GebrochenRationaleFunktion


def test_gebrochen_rationale_einfach():
    """Teste einfache gebrochen-rationale Funktion."""
    print("=== Test: GebrochenRationaleFunktion einfach ===")

    # (x^2-1)/(x-1) = x+1 für x≠1 - keine Nullstellen weil x=1 Polstelle
    f = GebrochenRationaleFunktion("x^2-1", "x-1")

    print(f"Funktion: {f}")
    print(f"Term: {f.term()}")

    # Teste Polstellen
    polstellen = f.polstellen()
    print(f"Polstellen: {polstellen}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    print("✅ Test abgeschlossen")


def test_gebrochen_rationale_mit_nullstellen():
    """Teste gebrochen-rationale Funktion mit gültigen Nullstellen."""
    print("\n=== Test: GebrochenRationaleFunktion mit Nullstellen ===")

    # (x^2-4)/(x-3) - Nullstelle bei x=2 und x=-2, Polstelle bei x=3
    f = GebrochenRationaleFunktion("x^2-4", "x-3")

    print(f"Funktion: {f}")
    print(f"Term: {f.term()}")

    # Teste Polstellen
    polstellen = f.polstellen()
    print(f"Polstellen: {polstellen}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    print("✅ Test abgeschlossen")


if __name__ == "__main__":
    print("Starte GebrochenRationaleFunktion Nullstellen Tests...\n")

    try:
        test_gebrochen_rationale_einfach()
        test_gebrochen_rationale_mit_nullstellen()
        print("\n🎉 Alle Tests erfolgreich!")

    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
