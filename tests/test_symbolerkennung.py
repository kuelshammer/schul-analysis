#!/usr/bin/env python3
"""
Test für die automatische Symbolerkennung in GanzrationaleFunktion
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import GanzrationaleFunktion


def test_automatische_symbolerkennung():
    """Test der automatischen Variablen- und Parametererkennung"""
    print("=== Test automatische Symbolerkennung ===")

    # Test 1: a x^2 + 1 (x=Variable, a=Parameter)
    print("\n1. Test: f = GanzrationaleFunktion('a x^2 + 1')")
    try:
        f1 = GanzrationaleFunktion("a x^2 + 1")
        print(f"   Term: {f1.term()}")
        print(f"   Hauptvariable: {f1.hauptvariable}")
        print(f"   Variablen: {[str(v) for v in f1.variablen]}")
        print(f"   Parameter: {[str(p) for p in f1.parameter]}")
        # Teste Wert nur, wenn keine Parameter vorhanden
        if not f1.parameter:
            print(f"   f1(2) = {f1.wert(2)}")
        else:
            print("   f1(2) = Kann nicht berechnet werden (Parameter vorhanden)")
    except Exception as e:
        print(f"   Fehler: {e}")

    # Test 2: 100t + 20 (t=Variable)
    print("\n2. Test: g = GanzrationaleFunktion('100t + 20')")
    try:
        f2 = GanzrationaleFunktion("100t + 20")
        print(f"   Term: {f2.term()}")
        print(f"   Hauptvariable: {f2.hauptvariable}")
        print(f"   Variablen: {[str(v) for v in f2.variablen]}")
        print(f"   Parameter: {[str(p) for p in f2.parameter]}")
        print(f"   g(0.5) = {f2.wert(0.5)}")
    except Exception as e:
        print(f"   Fehler: {e}")

    # Test 3: x^2 + 2x + 1 (keine Änderung zur alten Funktionalität)
    print("\n3. Test: h = GanzrationaleFunktion('x^2 + 2x + 1')")
    try:
        f3 = GanzrationaleFunktion("x^2 + 2x + 1")
        print(f"   Term: {f3.term()}")
        print(f"   Hauptvariable: {f3.hauptvariable}")
        print(f"   Variablen: {[str(v) for v in f3.variablen]}")
        print(f"   Parameter: {[str(p) for p in f3.parameter]}")
        print(f"   h(3) = {f3.wert(3)}")
    except Exception as e:
        print(f"   Fehler: {e}")

    # Test 4: Abwärtskompatibilität mit Liste
    print("\n4. Test: k = GanzrationaleFunktion([1, 0, -2, 1])")
    try:
        f4 = GanzrationaleFunktion([1, 0, -2, 1])  # x³ - 2x + 1
        print(f"   Term: {f4.term()}")
        print(f"   Hauptvariable: {f4.hauptvariable}")
        print(f"   Variablen: {[str(v) for v in f4.variablen]}")
        print(f"   Parameter: {[str(p) for p in f4.parameter]}")
        print(f"   k(2) = {f4.wert(2)}")
    except Exception as e:
        print(f"   Fehler: {e}")


if __name__ == "__main__":
    test_automatische_symbolerkennung()
    print("\n=== Test abgeschlossen ===")
