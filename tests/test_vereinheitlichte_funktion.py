#!/usr/bin/env python3
"""
Test der vereinheitlichten Funktion Klasse
"""

from schul_mathematik import Funktion


def test_vereinheitlichte_funktion():
    print("=== Test der vereinheitlichten Funktion Klasse ===")

    # Test 1: Ganzrationale Funktionen
    print("\n1. Test: Ganzrationale Funktionen")
    f1 = Funktion("x^2 + 1")
    print("f1 = Funktion('x^2 + 1')")
    print(f"Term: {f1.term()}")
    print(f"Ist ganzrational: {f1.ist_ganzrational}")
    print(f"Polstellen: {f1.polstellen()}")
    print(f"Variable: {[v.name for v in f1.variablen]}")
    print(f"f1(2) = {f1(2)}")
    print(f"f1(0) = {f1(0)}")

    # Test 2: Gebrochen-rationale Funktionen
    print("\n2. Test: Gebrochen-rationale Funktionen")
    f2 = Funktion("(x^2 - 1)/(x - 1)")
    print("f2 = Funktion('(x^2 - 1)/(x - 1)')")
    print(f"Term: {f2.term()}")
    print(f"Ist ganzrational: {f2.ist_ganzrational}")
    print(f"Polstellen: {f2.polstellen()}")
    print(f"f2(2) = {f2(2)}")
    print(f"f2(0) = {f2(0)}")

    # Test 3: Explizite Trennung (als normaler Bruch)
    print("\n3. Test: Explizite Trennung")
    f3 = Funktion("(x^2 + 1)/(x - 1)")
    print("f3 = Funktion('(x^2 + 1)/(x - 1)')")
    print(f"Term: {f3.term()}")
    print(f"Ist ganzrational: {f3.ist_ganzrational}")
    print(f"f3(2) = {f3(2)}")

    # Test 4: Symbolische Parameter
    print("\n4. Test: Symbolische Parameter")
    f4 = Funktion("a x^2 + b x + c")
    print("f4 = Funktion('a x^2 + b x + c')")
    print(f"Term: {f4.term()}")
    print(f"Variable: {[v.name for v in f4.variablen]}")
    print(f"Parameter: {[p.name for p in f4.parameter]}")
    print(f"f4(1) = {f4(1)}")
    print(f"f4(2) = {f4(2)}")

    # Test 5: Gebrochen-rationale mit Parametern
    print("\n5. Test: Gebrochen-rationale mit Parametern")
    f5 = Funktion("(a x^2 + 1)/(x - 1)")
    print("f5 = Funktion('(a x^2 + 1)/(x - 1)')")
    print(f"Term: {f5.term()}")
    print(f"Variable: {[v.name for v in f5.variablen]}")
    print(f"Parameter: {[p.name for p in f5.parameter]}")
    print(f"f5(0) = {f5(0)}")
    print(f"f5(2) = {f5(2)}")
    try:
        print(f"f5(1) = {f5(1)}")
    except ValueError as e:
        print(f"f5(1) -> Fehler (erwartet): {e}")

    # Test 6: Nullstellen
    print("\n6. Test: Nullstellen")
    f6 = Funktion("x^2 - 4")
    print("f6 = Funktion('x^2 - 4')")
    print(f"Nullstellen: {f6.nullstellen()}")

    f7 = Funktion("a x^2 + 1")
    print("f7 = Funktion('a x^2 + 1')")
    print(f"Nullstellen: {f7.nullstellen()}")

    # Test 7: Ableitung
    print("\n7. Test: Ableitung")
    f8 = Funktion("x^3 + 2x^2 + x")
    print("f8 = Funktion('x^3 + 2x^2 + x')")
    f8_abgeleitet = f8.ableitung()
    print(f"f8' = {f8_abgeleitet.term()}")
    print(f"f8'(1) = {f8_abgeleitet(1)}")

    # Test 8: Polstellen
    print("\n8. Test: Polstellen")
    f9 = Funktion("(x^2 - 4)/(x - 2)")
    print("f9 = Funktion('(x^2 - 4)/(x - 2)')")
    print(f"Polstellen: {f9.polstellen()}")  # Sollte leer sein, da kürzbar

    f10 = Funktion("1/(x - 1)")
    print("f10 = Funktion('1/(x - 1)')")
    print(f"Polstellen: {f10.polstellen()}")

    print("\n=== Test abgeschlossen ===")


if __name__ == "__main__":
    test_vereinheitlichte_funktion()
