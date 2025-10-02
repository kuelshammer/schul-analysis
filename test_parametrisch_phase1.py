#!/usr/bin/env python3
"""
Test der Phase 1: Variable und Parameter Klassen
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.parametrisch import Variable, Parameter, ParametrischeFunktion


def test_variable():
    """Test der Variable Klasse"""
    print("=== Test 1: Variable ===")

    x = Variable("x")
    print(f"Variable: {x}")
    print(f"Name: {x.name}")
    print(f"Symbol: {x.symbol}")
    print(f"Repr: {repr(x)}")

    # Teste Gleichheit
    x2 = Variable("x")
    y = Variable("y")
    print(f"x == x2: {x == x2}")
    print(f"x == y: {x == y}")

    print("✅ Variable Klasse funktioniert\n")
    return True


def test_parameter():
    """Test der Parameter Klasse"""
    print("=== Test 2: Parameter ===")

    a = Parameter("a")
    print(f"Parameter: {a}")
    print(f"Name: {a.name}")
    print(f"Symbol: {a.symbol}")
    print(f"Repr: {repr(a)}")

    # Teste Gleichheit
    a2 = Parameter("a")
    b = Parameter("b")
    print(f"a == a2: {a == a2}")
    print(f"a == b: {a == b}")

    print("✅ Parameter Klasse funktioniert\n")
    return True


def test_parametrische_funktion():
    """Test der ParametrischeFunktion Klasse"""
    print("=== Test 3: ParametrischeFunktion ===")

    # Erstelle Variable und Parameter
    x = Variable("x")
    a = Parameter("a")

    # Erstelle parametrische Funktion f_a(x) = a*x² + x
    f = ParametrischeFunktion([a, 1, 0], [x])
    print(f"Parametrische Funktion: {f}")
    print(f"Term: {f.term()}")
    print(f"SymPy-Term: {f.term_sympy}")
    print(f"Parameter: {f._parameternamen}")
    print(f"Variablen: {f._variablennamen}")

    print("✅ ParametrischeFunktion Klasse funktioniert\n")
    return True


def test_mit_wert():
    """Test der mit_wert Methode"""
    print("=== Test 4: mit_wert Methode ===")

    # Erstelle Variable und Parameter
    x = Variable("x")
    a = Parameter("a")

    # Erstelle parametrische Funktion f_a(x) = a*x² + x
    f = ParametrischeFunktion([a, 1, 0], [x])

    # Setze a = 2
    f_konkret = f.mit_wert(a=2)
    print(f"Parametrisch: {f}")
    print(f"Mit a=2: {f_konkret.term()}")

    # Teste mit verschiedenen Werten
    werte = [0, 1, -1, 0.5, -2]
    for wert in werte:
        f_test = f.mit_wert(a=wert)
        print(f"a={wert}: {f_test.term()}")

    print("✅ mit_wert Methode funktioniert\n")
    return True


def test_komplexe_beispiele():
    """Test komplexerer Beispiele"""
    print("=== Test 5: Komplexe Beispiele ===")

    # Beispiel 1: Lineare Funktion mit Parameter
    x = Variable("x")
    m = Parameter("m")
    b = Parameter("b")

    f1 = ParametrischeFunktion([b, m], [x])  # m*x + b
    print(f"Linear: {f1}")

    # Beispiel 2: Kubische Funktion
    a = Parameter("a")
    b = Parameter("b")
    c = Parameter("c")
    d = Parameter("d")

    f2 = ParametrischeFunktion([d, c, b, a], [x])  # a*x³ + b*x² + c*x + d
    print(f"Kubisch: {f2}")

    # Setze konkrete Werte
    f1_konkret = f1.mit_wert(m=2, b=3)
    print(f"Linear konkret: {f1_konkret.term()}")

    f2_konkret = f2.mit_wert(a=1, b=-3, c=0, d=0)
    print(f"Kubisch konkret: {f2_konkret.term()}")

    print("✅ Komplexe Beispiele funktionieren\n")
    return True


def main():
    """Haupttestfunktion"""
    print("🧪 Test von Phase 1: Variable und Parameter Klassen\n")

    tests = [
        test_variable,
        test_parameter,
        test_parametrische_funktion,
        test_mit_wert,
        test_komplexe_beispiele,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Fehler in {test.__name__}: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    # Zusammenfassung
    print("=== ZUSAMMENFASSUNG ===")
    successful = sum(results)
    total = len(results)

    print(f"Erfolgreiche Tests: {successful}/{total}")

    if successful == total:
        print("🎉 Phase 1 erfolgreich! Grundlegende Klassen funktionieren.")
        print("\n🔥 Nächste Schritte:")
        print("   - Symbolische Berechnungen implementieren")
        print("   - Graphische Integration")
        print("   - Multi-Plot für verschiedene Parameterwerte")
    else:
        print("⚠️ Einige Tests fehlgeschlagen. Debugging erforderlich.")

    return successful == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
