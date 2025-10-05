#!/usr/bin/env python3
"""
Minimaler Test der Magic Factory Architecture
"""

from schul_analysis import Funktion


def main():
    print("=== Magic Factory Architecture Test ===\n")

    # Test 1: Quadratische Funktion
    print("1. Quadratische Funktion:")
    f = Funktion("x^2 - 4x + 3")
    print(f"   Funktion: f(x) = {f.term()}")
    print(f"   Typ: {type(f).__name__}")
    print(f"   Ist quadratisch: {f.ist_quadratisch()}")
    print(f"   Grad: {f.grad()}")

    # Nullstellen
    nullstellen = f.nullstellen()
    print(f"   Nullstellen: {nullstellen}")

    # Spezialmethoden
    try:
        scheitelpunkt = f.get_scheitelpunkt()
        oeffnungsfaktor = f.get_oeffnungsfaktor()
        print(f"   Scheitelpunkt: {scheitelpunkt}")
        print(f"   Öffnungsfaktor: {oeffnungsfaktor}")
    except Exception as e:
        print(f"   Fehler bei Spezialmethoden: {e}")

    print()

    # Test 2: Lineare Funktion
    print("2. Lineare Funktion:")
    g = Funktion("2x + 3")
    print(f"   Funktion: g(x) = {g.term()}")
    print(f"   Typ: {type(g).__name__}")
    print(f"   Ist linear: {g.ist_linear()}")

    # Spezialmethoden
    try:
        steigung = g.steigung if hasattr(g, "steigung") else "Nicht verfügbar"
        print(f"   Steigung: {steigung}")
    except Exception as e:
        print(f"   Fehler bei Steigung: {e}")

    print()

    # Test 3: Andere Funktion
    print("3. Andere Funktion (nicht ganzrational):")
    h = Funktion("sin(x)")
    print(f"   Funktion: h(x) = {h.term()}")
    print(f"   Typ: {type(h).__name__}")
    print(f"   Ist ganzrational: {h.ist_ganzrational()}")

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    main()
