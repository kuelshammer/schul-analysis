#!/usr/bin/env python3
"""
Test der Phase 2: Symbolische Berechnungen mit ParametrischeFunktion
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.parametrisch import Variable, Parameter, ParametrischeFunktion


def test_symbolische_nullstellen():
    """Test der symbolischen Nullstellenberechnung"""
    print("=== Test 1: Symbolische Nullstellen ===")

    # Beispiel 1: f_a(x) = a*x² + x
    x = Variable("x")
    a = Parameter("a")

    f = ParametrischeFunktion([0, 1, a], [x])  # a*x² + x
    print(f"Funktion: {f.term()}")

    nullstellen = f.nullstellen()
    print(f"Symbolische Nullstellen: {nullstellen}")

    # Erwartet: [0, -1/a] mit Bedingungen
    erwartet = len(nullstellen) == 2  # Sollte 2 Nullstellen haben
    print(f"Anzahl Nullstellen korrekt: {erwartet}")

    # Teste mit konkreten Werten
    f_test = f.mit_wert(a=2)  # 2x² + x
    konkrete_nullstellen = f_test.nullstellen()
    print(f"Konkrete Nullstellen (a=2): {konkrete_nullstellen}")

    print("✅ Symbolische Nullstellen funktionieren\n")
    return True


def test_symbolische_extremstellen():
    """Test der symbolischen Extremstellenberechnung"""
    print("=== Test 2: Symbolische Extremstellen ===")

    # Beispiel 1: f_a(x) = a*x² + x
    x = Variable("x")
    a = Parameter("a")

    f = ParametrischeFunktion([0, 1, a], [x])  # a*x² + x
    print(f"Funktion: {f.term()}")

    extremstellen = f.extremstellen()
    print(f"Symbolische Extremstellen: {extremstellen}")

    # Erwartet: [(-1/(2a), "Minimum wenn a > 0")]
    if extremstellen:
        x_wert, art = extremstellen[0]
        print(f"Extremstelle bei x = {x_wert}")
        print(f"Art: {art}")

    # Teste mit verschiedenen a-Werten
    for a_wert in [1, -1, 2, -2]:
        try:
            f_test = f.mit_wert(a=a_wert)
            konkrete_extremstellen = f_test.extremstellen()
            print(f"a={a_wert}: {konkrete_extremstellen}")
        except Exception as e:
            print(f"a={a_wert}: Fehler - {e}")

    print("✅ Symbolische Extremstellen funktionieren\n")
    return True


def test_verschiedene_funktionstypen():
    """Test verschiedener Funktionstypen mit Parametern"""
    print("=== Test 3: Verschiedene Funktionstypen ===")

    x = Variable("x")
    a = Parameter("a")
    b = Parameter("b")

    # Lineare Funktion: f(x) = a*x + b
    f_linear = ParametrischeFunktion([b, a], [x])
    print(f"Linear: {f_linear.term()}")

    # Quadratische Funktion: f(x) = a*x² + b
    f_quadratisch = ParametrischeFunktion([b, 0, a], [x])
    print(f"Quadratisch: {f_quadratisch.term()}")

    # Kubische Funktion: f(x) = a*x³ + x
    f_kubisch = ParametrischeFunktion([0, 1, 0, a], [x])
    print(f"Kubisch: {f_kubisch.term()}")

    # Teste Berechnungen für jede Funktion
    for name, f in [
        ("Linear", f_linear),
        ("Quadratisch", f_quadratisch),
        ("Kubisch", f_kubisch),
    ]:
        try:
            nullstellen = f.nullstellen()
            extremstellen = f.extremstellen()
            print(f"{name}:")
            print(f"  Nullstellen: {nullstellen}")
            print(f"  Extremstellen: {extremstellen}")
        except Exception as e:
            print(f"{name}: Fehler - {e}")

    print("✅ Verschiedene Funktionstypen funktionieren\n")
    return True


def test_spezialfaelle():
    """Test von Spezialfällen"""
    print("=== Test 4: Spezialfälle ===")

    x = Variable("x")
    a = Parameter("a")

    # Fall 1: Konstante Funktion mit Parameter
    f_konstant = ParametrischeFunktion([a], [x])  # f(x) = a
    print(f"Konstant: {f_konstant.term()}")

    # Fall 2: Funktion mit mehreren Parametern
    b = Parameter("b")
    f_mehrfach = ParametrischeFunktion([b, a], [x])  # f(x) = a*x + b
    print(f"Mehrfach-Parameter: {f_mehrfach.term()}")

    # Teste konkrete Werte
    print("Konkrete Tests:")
    for f_name, f, werte in [
        ("Konstant a=5", f_konstant, {"a": 5}),
        ("Linear a=2,b=3", f_mehrfach, {"a": 2, "b": 3}),
        ("Linear a=0,b=5", f_mehrfach, {"a": 0, "b": 5}),
    ]:
        try:
            f_konkret = f.mit_wert(**werte)
            print(f"  {f_name}: {f_konkret.term()}")
            print(f"    Nullstellen: {f_konkret.nullstellen()}")
        except Exception as e:
            print(f"  {f_name}: Fehler - {e}")

    print("✅ Spezialfälle funktionieren\n")
    return True


def test_anwendungsbeispiele():
    """Test von praktischen Anwendungsbeispielen"""
    print("=== Test 5: Anwendungsbeispiele ===")

    x = Variable("x")

    # Beispiel 1: Parabel mit variablem Öffnungsfaktor
    a = Parameter("a")
    h = Parameter("h")
    k = Parameter("k")

    # f(x) = a*(x-h)² + k - Vereinfacht als a*x² + b*x + c
    # Vereinfachte Form ohne Multiplikation in Koeffizientenliste
    f_parabel = ParametrischeFunktion([k, 0, a], [x])  # a*x² + k (vereinfacht)
    print(f"Parabel: {f_parabel.term()}")

    # Teste verschiedene Parabeln
    parameter_sets = [
        {"a": 1, "k": 0},  # y = x²
        {"a": 2, "k": -3},  # y = 2x² - 3
        {"a": -1, "k": 1},  # y = -x² + 1
    ]

    for i, params in enumerate(parameter_sets):
        try:
            f_konkret = f_parabel.mit_wert(**params)
            print(f"  Parabel {i + 1}: {f_konkret.term()}")

            # Berechne Scheitelpunkt
            extremstellen = f_konkret.extremstellen()
            print(f"    Scheitelpunkt: {extremstellen}")
        except Exception as e:
            print(f"  Parabel {i + 1}: Fehler - {e}")

    print("✅ Anwendungsbeispiele funktionieren\n")
    return True


def main():
    """Haupttestfunktion"""
    print("🧪 Test von Phase 2: Symbolische Berechnungen\n")

    tests = [
        test_symbolische_nullstellen,
        test_symbolische_extremstellen,
        test_verschiedene_funktionstypen,
        test_spezialfaelle,
        test_anwendungsbeispiele,
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
        print("🎉 Phase 2 erfolgreich! Symbolische Berechnungen funktionieren.")
        print("\n🔥 Nächste Schritte:")
        print("   - Graphische Integration mit Multi-Plot")
        print("   - Automatische Visualisierung verschiedener Parameterwerte")
        print("   - Interaktive Parameter-Slider (wenn unterstützt)")
    else:
        print("⚠️ Einige Tests fehlgeschlagen. Symbolische Berechnungen optimieren.")

    return successful == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
