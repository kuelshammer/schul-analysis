#!/usr/bin/env python3
"""
Test für KompositionFunktion Nullstellen-Implementierung.
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis.strukturiert import KompositionFunktion


def test_komposition_funktion_einfach():
    """Teste einfache Kompositionsfunktion."""
    print("=== Test: KompositionFunktion einfach ===")

    # (x-1)^2 - Nullstelle bei x=1
    f = KompositionFunktion("(x-1)^2")

    print(f"Funktion: {f}")
    print(f"Term: {f.term()}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    print("✅ Test abgeschlossen")


def test_komposition_funktion_komplex():
    """Teste komplexere Kompositionsfunktion."""
    print("\n=== Test: KompositionFunktion komplex ===")

    # sin(x)^2 - Nullstellen wo sin(x) = 0, also x = kπ
    f = KompositionFunktion("sin(x)^2")

    print(f"Funktion: {f}")
    print(f"Term: {f.term()}")

    # Teste Nullstellen
    nullstellen = f.nullstellen()
    print(f"Nullstellen: {nullstellen}")
    print(f"Anzahl Nullstellen: {len(nullstellen)}")

    print("✅ Test abgeschlossen")


if __name__ == "__main__":
    print("Starte KompositionFunktion Nullstellen Tests...\n")

    try:
        test_komposition_funktion_einfach()
        test_komposition_funktion_komplex()
        print("\n🎉 Alle Tests erfolgreich!")

    except Exception as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
