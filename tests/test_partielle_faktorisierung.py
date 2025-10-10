#!/usr/bin/env python3
"""
Test des erweiterten Systems für partielle Faktorisierung
"""

import sys

sys.path.insert(0, "src")

import sympy as sp

from schul_mathematik.analysis.ganzrationale import GanzrationaleFunktion


def test_partielle_faktorisierung():
    """Testet die partielle Faktorisierung mit dem Beispiel (x^2-4)(x^3+x^2+3x+3)"""

    print("=== Test der partiellen Faktorisierung ===\n")

    # Beispiel 1: (x^2-4)(x^3+x^2+3x+3)
    print("Beispiel 1: (x²-4)(x³+x²+3x+3)")

    # Erweitere das Polynom: (x^2-4)(x^3+x^2+3x+3) = x^5 + x^4 + 3x^3 + 3x^2 - 4x^3 - 4x^2 - 12x - 12
    # = x^5 + x^4 - x^3 - x^2 - 12x - 12
    # ACHTUNG: Koeffizienten sind in umgekehrter Reihenfolge (a0, a1, a2, a3, a4, a5)!
    koeffizienten = [-12, -12, -1, -1, 1, 1]  # x^5 + x^4 - x^3 - x^2 - 12x - 12
    f = GanzrationaleFunktion(koeffizienten)

    print(f"Polynom: {f.term()}")
    print(f"Grad: {len(koeffizienten) - 1}")
    print()

    # Intelligente Analyse durchführen
    analyse = f._intelligente_loesungsanalyse()

    print("=== Ergebnisse der intelligenten Analyse ===")
    print(f"Erkannte Muster: {analyse['muster']}")
    print()

    if "partielle_faktorisierung" in analyse:
        print("=== Partielle Faktorisierung gefunden ===")
        partial = analyse["partielle_faktorisierung"]

        print("Einfache Faktoren:")
        for typ, faktor in partial["einfache_faktoren"]:
            print(f"  - {typ}: {sp.latex(faktor)}")

        print("\nKomplexe Faktoren:")
        for typ, faktor in partial["komplexe_faktoren"]:
            print(f"  - {typ}: {sp.latex(faktor)}")

        print()

    # Lösungsweg generieren
    print("=== Generierter Lösungsweg ===")
    weg = f.nullstellen_weg()
    print(weg)

    print("\n" + "=" * 50 + "\n")

    # Beispiel 2: Noch ein komplexeres Beispiel
    print("Beispiel 2: (x^2-9)(x^4 + 2x^2 + 1)")

    # (x^2-9)(x^4 + 2x^2 + 1) = x^6 + 2x^4 + x^2 - 9x^4 - 18x^2 - 9
    # = x^6 - 7x^4 - 17x^2 - 9
    koeffizienten2 = [
        -9,
        0,
        -17,
        0,
        -7,
        0,
        1,
    ]  # x^6 - 7x^4 - 17x^2 - 9 (in umgekehrter Reihenfolge)
    f2 = GanzrationaleFunktion(koeffizienten2)

    print(f"Polynom: {f2.term()}")
    print(f"Grad: {len(koeffizienten2) - 1}")
    print()

    # Intelligente Analyse durchführen
    analyse2 = f2._intelligente_loesungsanalyse()

    print("=== Ergebnisse der intelligenten Analyse ===")
    print(f"Erkannte Muster: {analyse2['muster']}")
    print()

    if "partielle_faktorisierung" in analyse2:
        print("=== Partielle Faktorisierung gefunden ===")
        partial2 = analyse2["partielle_faktorisierung"]

        print("Einfache Faktoren:")
        for typ, faktor in partial2["einfache_faktoren"]:
            print(f"  - {typ}: {sp.latex(faktor)}")

        print("\nKomplexe Faktoren:")
        for typ, faktor in partial2["komplexe_faktoren"]:
            print(f"  - {typ}: {sp.latex(faktor)}")

    print()

    # Zeige auch die tatsächlichen Nullstellen
    print("=== Tatsächliche Nullstellen ===")
    try:
        nullstellen = f.nullstellen(exakt=True)
        print(f"Beispiel 1 Nullstellen: {nullstellen}")

        nullstellen2 = f2.nullstellen(exakt=True)
        print(f"Beispiel 2 Nullstellen: {nullstellen2}")
    except Exception as e:
        print(f"Fehler bei der Nullstellenberechnung: {e}")


if __name__ == "__main__":
    test_partielle_faktorisierung()
