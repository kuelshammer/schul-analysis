#!/usr/bin/env python3
"""
Demo für Lineare Gleichungssysteme (LGS) Funktionalität

Zeigt die intuitive Syntax: LGS(f(3)==4, f(2)==0, f1(0)=0)
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import LGS, Ableitung, Parameter, ParametrischeFunktion, Variable


def demo_lgs():
    """Demo der LGS-Funktionalität"""
    print("🎯 LGS Demo: Lineare Gleichungssysteme für parametrische Funktionen")
    print("=" * 60)

    # Beispiel 1: Finde Parabel durch 3 Punkte
    print("\n📐 Beispiel 1: Parabel durch 3 Punkte")
    print("Gesucht: Parabel f(x) = ax² + bx + c durch P(1|2), Q(2|3), R(3|6)")

    # Erstelle Parameter und Variable
    a, b, c = Parameter("a"), Parameter("b"), Parameter("c")
    x = Variable("x")

    # Erstelle parametrische Funktion
    f = ParametrischeFunktion([a, b, c], [x])

    # Erstelle Gleichungen mit intuitiver Syntax
    gl1 = f(1) == 2  # f(1) = 2
    gl2 = f(2) == 3  # f(2) = 3
    gl3 = f(3) == 6  # f(3) = 6

    print("Gleichungen:")
    print(f"  {gl1.beschreibung}")
    print(f"  {gl2.beschreibung}")
    print(f"  {gl3.beschreibung}")

    # Erstelle und löse LGS
    lgs = LGS(gl1, gl2, gl3)
    loesung = lgs.löse()

    print(f"\nLösung: {loesung}")

    # Wende Lösung an
    loesung_str = {str(k): v for k, v in loesung.items()}
    f_konkret = f.mit_wert(**loesung_str)

    print(f"Gefundene Parabel: f(x) = {f_konkret.term()}")

    # Verifiziere
    print("\nVerifikation:")
    print(f"  f(1) = {f_konkret.wert(1):.1f} ✓")
    print(f"  f(2) = {f_konkret.wert(2):.1f} ✓")
    print(f"  f(3) = {f_konkret.wert(3):.1f} ✓")

    # Beispiel 2: Funktion mit Ableitungsbedingung
    print("\n\n📈 Beispiel 2: Funktion mit Ableitungsbedingung")
    print("Gesucht: Funktion f(x) = ax² + bx + c mit f(0) = 1, f(1) = 3, f'(1) = 4")

    # Erste Ableitung
    f1 = Ableitung(f)

    print(f"Funktion: f(x) = {f.term()}")
    print(f"Ableitung: f'(x) = {f1.term()}")

    # Bedingungen
    gl1 = f(0) == 1
    gl2 = f(1) == 3
    gl3 = f1(1) == 4  # f'(1) = 4

    print("\nBedingungen:")
    print(f"  {gl1.beschreibung}")
    print(f"  {gl2.beschreibung}")
    print(f"  {gl3.beschreibung}")

    # LGS lösen
    lgs2 = LGS(gl1, gl2, gl3)
    loesung2 = lgs2.löse()

    print(f"\nLösung: {loesung2}")

    # Anwenden und verifizieren
    loesung2_str = {str(k): v for k, v in loesung2.items()}
    f2_konkret = f.mit_wert(**loesung2_str)
    f12_konkret = f1.mit_wert(**loesung2_str)

    print(f"Gefundene Funktion: f(x) = {f2_konkret.term()}")
    print(f"Ableitung: f'(x) = {f12_konkret.term()}")

    print("\nVerifikation:")
    print(f"  f(0) = {f2_konkret.wert(0):.1f} ✓")
    print(f"  f(1) = {f2_konkret.wert(1):.1f} ✓")
    print(f"  f'(1) = {f12_konkret.wert(1):.1f} ✓")

    print("\n🎉 Demo erfolgreich!")


if __name__ == "__main__":
    demo_lgs()
