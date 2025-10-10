#!/usr/bin/env python3
"""
Test-Skript für die neuen intelligenten Nullstellenberechnungen.

Testet:
1. ProduktFunktion mit Nullproduktsatz und Sympy-Vereinfachung
2. SummenFunktion mit pragmatischem Ansatz
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik.analysis import Funktion


def test_produkt_funktion():
    """Testet die intelligente Nullstellenberechnung für ProduktFunktion."""
    print("=== Test ProduktFunktion ===")

    # Test 1: Einfaches Produkt
    print("\n1. Einfaches Produkt: (x-1)*(x-2)")
    f1 = Funktion("(x-1)*(x-2)")
    print(f"Funktionstyp: {f1.funktionstyp}")
    nullstellen = f1.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 2: Produkt mit Vielfachheit
    print("\n2. Produkt mit Vielfachheit: (x-1)^2 * (2x-2)")
    f2 = Funktion("(x-1)**2 * (2*x-2)")
    print(f"Funktionstyp: {f2.funktionstyp}")
    nullstellen = f2.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 3: Parametrisiertes Produkt
    print("\n3. Parametrisiertes Produkt: (x-a)*(x-b)")
    f3 = Funktion("(x-a)*(x-b)")
    print(f"Funktionstyp: {f3.funktionstyp}")
    nullstellen = f3.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 4: Gemischtes Produkt
    print("\n4. Gemischtes Produkt: x^2 * sin(x)")
    f4 = Funktion("x**2 * sin(x)")
    print(f"Funktionstyp: {f4.funktionstyp}")

    # Debug: Schauen wir uns die Faktoren an
    if hasattr(f4, "faktoren"):
        print(f"Faktoren: {[str(f) for f in f4.faktoren]}")
        for i, faktor in enumerate(f4.faktoren):
            print(f"Faktor {i}: {faktor}, Typ: {type(faktor)}")
            if hasattr(faktor, "nullstellen"):
                try:
                    faktor_nullstellen = faktor.nullstellen()
                    print(f"  Nullstellen von Faktor {i}: {faktor_nullstellen}")
                    for j, ns in enumerate(faktor_nullstellen):
                        print(f"    Nullstelle {j}: {ns}, Typ: {type(ns)}")
                        if hasattr(ns, "x"):
                            print(f"    ns.x: {ns.x}, Typ: {type(ns.x)}")
                        else:
                            print(f"    ns hat kein x-Attribut: {dir(ns)}")
                except Exception as e:
                    print(f"  Fehler bei Nullstellen von Faktor {i}: {e}")

    nullstellen = f4.nullstellen()
    print(f"Nullstellen: {nullstellen}")


def test_summe_funktion():
    """Testet die pragmatische Nullstellenberechnung für SummenFunktion."""
    print("\n=== Test SummenFunktion ===")

    # Test 1: Lineare Summe
    print("\n1. Lineare Summe: (2x+1) + (3x-2)")
    f1 = Funktion("(2*x+1) + (3*x-2)")
    print(f"Funktionstyp: {f1.funktionstyp}")
    nullstellen = f1.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 2: Quadratische Summe
    print("\n2. Quadratische Summe: x^2 + 2x + 1 + x^2 - 4x")
    f2 = Funktion("x**2 + 2*x + 1 + x**2 - 4*x")
    print(f"Funktionstyp: {f2.funktionstyp}")
    nullstellen = f2.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 3: Einfache exponentielle Summe
    print("\n3. Einfache exponentielle Summe: exp(x) + 1")
    f3 = Funktion("exp(x) + 1")
    print(f"Funktionstyp: {f3.funktionstyp}")
    nullstellen = f3.nullstellen()
    print(f"Nullstellen: {nullstellen}")

    # Test 4: Schwere trigonometrische Summe (sollte leere Liste zurückgeben)
    print("\n4. Schwere trigonometrische Summe: sin(x) + cos(x)")
    f4 = Funktion("sin(x) + cos(x)")
    print(f"Funktionstyp: {f4.funktionstyp}")
    nullstellen = f4.nullstellen()
    print(f"Nullstellen: {nullstellen}")


def test_vereinfachung():
    """Testet die Sympy-Vereinfachung direkt."""
    print("\n=== Test Sympy-Vereinfachung ===")

    import sympy as sp

    x, a, b = sp.symbols("x a b")

    # Test 1: Symbolische Vereinfachung
    print("\n1. Vereinfachung von -b/a vs c")
    ausdruck1 = -b / a
    ausdruck2 = c = sp.Symbol("c")
    print(f"ausdruck1: {ausdruck1}")
    print(f"ausdruck2: {ausdruck2}")
    print(
        f"Vereinfacht: {sp.simplify(ausdruck1)} == {sp.simplify(ausdruck2)}? {sp.simplify(ausdruck1) == sp.simplify(ausdruck2)}"
    )

    # Test 2: Komplexe Vereinfachung
    print("\n2. Vereinfachung von (x-a) + (a-x)")
    ausdruck3 = (x - a) + (a - x)
    print(f"ausdruck3: {ausdruck3}")
    print(f"Vereinfacht: {sp.simplify(ausdruck3)}")


if __name__ == "__main__":
    print("Teste die neuen intelligenten Nullstellenberechnungen...")

    try:
        test_produkt_funktion()
        test_summe_funktion()
        test_vereinfachung()
        print("\n=== Alle Tests abgeschlossen ===")
    except Exception as e:
        print(f"Fehler beim Testen: {e}")
        import traceback

        traceback.print_exc()
