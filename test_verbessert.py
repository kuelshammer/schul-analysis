#!/usr/bin/env python3
"""
Umfassender Test der verbesserten partiellen Faktorisierung
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.ganzrationale import GanzrationaleFunktion
import sympy as sp


def test_verbesserte_faktorisierung():
    """Testet die verbesserten Funktionen für partielle Faktorisierung"""

    print("=== Test der verbesserten partiellen Faktorisierung ===\n")

    # Test 1: Lineare Faktoren
    print("Test 1: Reine lineare Faktoren")
    koeffizienten = [-6, 11, -6, 1]  # x^3 - 6x^2 + 11x - 6 = (x-1)(x-2)(x-3)
    f = GanzrationaleFunktion(koeffizienten)

    print(f"Polynom: {f.term()}")
    analyse = f._intelligente_loesungsanalyse()

    if "partielle_faktorisierung" in analyse:
        partial = analyse["partielle_faktorisierung"]
        print("Einfache Faktoren:")
        for typ, faktor in partial["einfache_faktoren"]:
            print(f"  {typ}: {faktor}")

            # Teste die neuen Berechnungsfunktionen
            if typ == "linear":
                nullstellen = f._berechne_lineare_nullstelle(faktor)
                print(f"    Berechnete Nullstellen: {nullstellen}")

    print("\n" + "=" * 50 + "\n")

    # Test 2: Quadratische Faktoren mit reellen Nullstellen
    print("Test 2: Quadratische Faktoren mit reellen Nullstellen")
    koeffizienten = [
        -4,
        0,
        5,
        0,
        -4,
        0,
        1,
    ]  # x^6 - 4x^5 + 5x^4 - 4x^2 + 4 = (x^2-1)(x^2-2)(x^2-2x+2)
    f2 = GanzrationaleFunktion(koeffizienten)

    print(f"Polynom: {f2.term()}")
    analyse2 = f2._intelligente_loesungsanalyse()

    if "partielle_faktorisierung" in analyse2:
        partial2 = analyse2["partielle_faktorisierung"]
        print("Einfache Faktoren:")
        for typ, faktor in partial2["einfache_faktoren"]:
            print(f"  {typ}: {faktor}")

            if typ == "quadratisch_reell":
                nullstellen = f2._berechne_quadratische_nullstellen(faktor)
                print(f"    Berechnete Nullstellen: {nullstellen}")

    print("\n" + "=" * 50 + "\n")

    # Test 3: Perfekte Potenzen
    print("Test 3: Perfekte Potenzen")
    koeffizienten = [-1, 0, 3, 0, -3, 0, 1]  # x^6 - 3x^4 + 3x^2 - 1 = (x^2-1)^3
    f3 = GanzrationaleFunktion(koeffizienten)

    print(f"Polynom: {f3.term()}")
    analyse3 = f3._intelligente_loesungsanalyse()

    if "partielle_faktorisierung" in analyse3:
        partial3 = analyse3["partielle_faktorisierung"]
        print("Einfache Faktoren:")
        for typ, faktor in partial3["einfache_faktoren"]:
            print(f"  {typ}: {faktor}")

    print("\n" + "=" * 50 + "\n")

    # Test 4: Komplexe Faktoren
    print("Test 4: Komplexe Faktoren")
    koeffizienten = [4, 0, 5, 0, 1]  # x^4 + 5x^2 + 4 = (x^2+1)(x^2+4)
    f4 = GanzrationaleFunktion(koeffizienten)

    print(f"Polynom: {f4.term()}")
    analyse4 = f4._intelligente_loesungsanalyse()

    if "partielle_faktorisierung" in analyse4:
        partial4 = analyse4["partielle_faktorisierung"]
        print("Komplexe Faktoren:")
        for typ, faktor in partial4["komplexe_faktoren"]:
            print(f"  {typ}: {faktor}")

    print("\n" + "=" * 50 + "\n")

    # Test 5: Fehlerbehandlung
    print("Test 5: Fehlerbehandlung bei ungültigen Faktoren")

    # Teste die Berechnungsfunktionen direkt
    x = sp.symbols("x")

    # Ungültiger linearer Faktor
    try:
        print("Teste ungültigen linearen Faktor:")
        invalid_linear = x**2 + 1  # Eigentlich quadratisch
        result = f._berechne_lineare_nullstelle(invalid_linear)
        print(f"  Ergebnis: {result} (sollte leer sein)")
    except Exception as e:
        print(f"  Fehler: {e}")

    # Ungültiger quadratischer Faktor
    try:
        print("Teste ungültigen quadratischen Faktor:")
        invalid_quad = x**3 + 1  # Eigentlich kubisch
        result = f._berechne_quadratische_nullstellen(invalid_quad)
        print(f"  Ergebnis: {result} (sollte leer sein)")
    except Exception as e:
        print(f"  Fehler: {e}")


if __name__ == "__main__":
    test_verbesserte_faktorisierung()
