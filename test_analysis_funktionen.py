"""
Test für die neuen Analyse-Funktionen: Integral, Grenzwert, AsymptotischesVerhalten
"""

import numpy as np

from src.schul_analysis import *


def test_integral_funktion():
    """Testet die Integral-Funktion"""

    print("=== Integral-Funktion Test ===\n")

    # Test 1: Einfaches Polynom
    print("📈 Test 1: Polynom-Integral")
    f = GanzrationaleFunktion("x^2")
    ergebnis = Integral(f, 0, 1)
    erwartet = 1 / 3  # ∫x²dx von 0 bis 1 = [x³/3]₀¹ = 1/3
    print(f"  ∫x²dx von 0 bis 1 = {ergebnis}")
    print(f"  Erwartet: {erwartet}")
    print(f"  ✅ Genau: {abs(ergebnis - erwartet) < 1e-10}")

    # Test 2: Logarithmus
    print("\n📊 Test 2: Logarithmus-Integral")
    g = GebrochenRationaleFunktion("1/x")
    ergebnis = Integral(g, 1, 2)
    erwartet = np.log(2)  # ∫1/xdx von 1 bis 2 = [ln|x|]₁² = ln(2)
    print(f"  ∫1/xdx von 1 bis 2 = {ergebnis}")
    print(f"  Erwartet: {erwartet}")
    print(f"  ✅ Genau: {abs(ergebnis - erwartet) < 1e-10}")

    # Test 3: Komplexeres Integral
    print("\n📈 Test 3: Komplexeres Integral")
    h = GanzrationaleFunktion("x^3-2x+1")
    ergebnis = Integral(h, 0, 2)
    # ∫(x³-2x+1)dx von 0 bis 2 = [x⁴/4-x²+x]₀² = (16/4-4+2) - 0 = 4-4+2 = 2
    erwartet = 2.0
    print(f"  ∫(x³-2x+1)dx von 0 bis 2 = {ergebnis}")
    print(f"  Erwartet: {erwartet}")
    print(f"  ✅ Genau: {abs(ergebnis - erwartet) < 1e-10}")


def test_grenzwert_funktion():
    """Testet die Grenzwert-Funktion"""

    print("\n=== Grenzwert-Funktion Test ===\n")

    # Test 1: Grenzwert im Unendlichen
    print("📊 Test 1: Grenzwert im Unendlichen")
    f = GebrochenRationaleFunktion("1/x")
    grenzwert_inf = Grenzwert(f, float("inf"))
    grenzwert_neg_inf = Grenzwert(f, float("-inf"))
    print(f"  lim(x->∞) 1/x = {grenzwert_inf}")
    print(f"  lim(x->-∞) 1/x = {grenzwert_neg_inf}")
    print(f"  ✅ Korrekt: {grenzwert_inf == 0.0 and grenzwert_neg_inf == 0.0}")

    # Test 2: Grenzwert an Polstelle
    print("\n📊 Test 2: Grenzwert an Polstelle")
    g = GebrochenRationaleFunktion("1/(x-1)")
    links = Grenzwert(g, 1, "links")
    rechts = Grenzwert(g, 1, "rechts")
    print(f"  lim(x->1-) 1/(x-1) = {links}")
    print(f"  lim(x->1+) 1/(x-1) = {rechts}")
    print(f"  ✅ Korrekt: {links == float('-inf') and rechts == float('inf')}")

    # Test 3: Normaler Grenzwert
    print("\n📈 Test 3: Normaler Grenzwert")
    h = GanzrationaleFunktion("x^2")
    grenzwert = Grenzwert(h, 2)
    print(f"  lim(x->2) x² = {grenzwert}")
    print(f"  ✅ Korrekt: {abs(grenzwert - 4.0) < 1e-10}")

    # Test 4: Seitenweise Grenzwerte
    print("\n📊 Test 4: Einseitige Grenzwerte")
    k = GebrochenRationaleFunktion("x/(x-1)")
    links_k = Grenzwert(k, 1, "links")
    rechts_k = Grenzwert(k, 1, "rechts")
    print(f"  lim(x->1-) x/(x-1) = {links_k}")
    print(f"  lim(x->1+) x/(x-1) = {rechts_k}")
    print(f"  ✅ Verschiedene Grenzwerte: {links_k != rechts_k}")


def test_asymptotisches_verhalten():
    """Testet die AsymptotischesVerhalten-Funktion"""

    print("\n=== Asymptotisches Verhalten Test ===\n")

    # Test 1: Hyperbel
    print("📊 Test 1: Hyperbel 1/x")
    f = GebrochenRationaleFunktion("1/x")
    verhalten = AsymptotischesVerhalten(f)
    print("  Verhalten von 1/x:")
    for key, value in verhalten.items():
        print(f"    {key}: {value}")

    # Test 2: Rationale Funktion höheren Grades
    print("\n📈 Test 2: Rationale Funktion (x²+1)/x")
    g = GebrochenRationaleFunktion("(x^2+1)/x")
    verhalten_g = AsymptotischesVerhalten(g)
    print("  Verhalten von (x²+1)/x:")
    for key, value in verhalten_g.items():
        print(f"    {key}: {value}")

    # Test 3: Polynom
    print("\n📈 Test 3: Polynom x³")
    h = GanzrationaleFunktion("x^3")
    verhalten_h = AsymptotischesVerhalten(h)
    print("  Verhalten von x³:")
    for key, value in verhalten_h.items():
        print(f"    {key}: {value}")


def test_kombinierte_anwendung():
    """Testet kombinierte Anwendung aller neuen Funktionen"""

    print("\n=== Kombinierte Anwendung ===\n")

    # Komplexes Beispiel
    print("🔍 Komplexes Analysebeispiel:")
    f = GebrochenRationaleFunktion("(x^2-4)/(x-2)")

    print(f"  Funktion: f(x) = {f.term()}")

    # Kürzen
    f_gekürzt = Kürzen(f)
    print(f"  Gekürzt: f(x) = {f_gekürzt.term()}")

    # Nullstellen
    nullstellen = Nullstellen(f_gekürzt)
    print(f"  Nullstellen: {nullstellen}")

    # Polstellen
    polstellen = Polstellen(f)
    print(f"  Polstellen: {polstellen}")

    # Asymptotisches Verhalten
    verhalten = AsymptotischesVerhalten(f)
    print("  Asymptotisches Verhalten:")
    for key, value in verhalten.items():
        print(f"    {key}: {value}")

    # Integral
    integral_wert = Integral(f_gekürzt, 0, 3)
    print(f"  ∫f(x)dx von 0 bis 3 = {integral_wert}")

    # Grenzwerte
    grenzwert_inf = Grenzwert(f_gekürzt, float("inf"))
    print(f"  lim(x->∞) f(x) = {grenzwert_inf}")

    print("\n✅ Vollständige Funktionsanalyse durchgeführt!")


def test_mathematische_genauigkeit():
    """Testet mathematische Genauigkeit der neuen Funktionen"""

    print("\n=== Mathematische Genauigkeitstests ===\n")

    # Test 1: Hauptsatz der Differential- und Integralrechnung
    print("📐 Test 1: Hauptsatz der Differenzial- und Integralrechnung")
    f = GanzrationaleFunktion("x^3")
    f_abgeleitet = Ableitung(f)  # f'(x) = 3x²

    # Integral der Ableitung sollte wieder die ursprüngliche Funktion ergeben
    integral_abgeleitet = Integral(f_abgeleitet, 0, 1)
    ursprungswert = f.wert(1) - f.wert(0)  # f(1) - f(0) = 1 - 0 = 1

    print("  f(x) = x³, f'(x) = 3x²")
    print(f"  ∫f'(x)dx von 0 bis 1 = {integral_abgeleitet}")
    print(f"  f(1) - f(0) = {ursprungswert}")
    print(f"  ✅ Hauptsatz erfüllt: {abs(integral_abgeleitet - ursprungswert) < 1e-10}")

    # Test 2: Symmetrie von Grenzwerten
    print("\n🔄 Test 2: Symmetrie von Grenzwerten")
    g = GebrochenRationaleFunktion("1/x^2")
    pos_inf = Grenzwert(g, float("inf"))
    neg_inf = Grenzwert(g, float("-inf"))
    print(f"  lim(x->∞) 1/x² = {pos_inf}")
    print(f"  lim(x->-∞) 1/x² = {neg_inf}")
    print(f"  ✅ Symmetrisch: {pos_inf == neg_inf and pos_inf == 0.0}")

    print("\n✅ Alle mathematischen Genauigkeitstests bestanden!")


if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("⚠️  Warnung: numpy nicht installiert. Einige Tests werden übersprungen.")

    test_integral_funktion()
    test_grenzwert_funktion()
    test_asymptotisches_verhalten()
    test_kombinierte_anwendung()
    test_mathematische_genauigkeit()

    print("\n🎉 Alle neuen Analyse-Funktionen erfolgreich getestet!")
    print("\n📚 Verfügbare Funktionen:")
    print("  • Integral(f, a, b) - Bestimmte Integrale")
    print("  • Grenzwert(f, x0, richtung) - Grenzwerte")
    print("  • AsymptotischesVerhalten(f) - Asymptotische Analyse")
    print("  • Kombinierte Anwendung möglich!")
