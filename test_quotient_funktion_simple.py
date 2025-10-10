#!/usr/bin/env python3
"""
Einfacher Test für QuotientFunktion Nullstellen-Implementierung.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.strukturiert import QuotientFunktion


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

    print("✅ Test abgeschlossen")


if __name__ == "__main__":
    print("Starte einfacher QuotientFunktion Test...\n")

    try:
        test_quotient_funktion_einfach()
        print("\n🎉 Test erfolgreich!")

    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
