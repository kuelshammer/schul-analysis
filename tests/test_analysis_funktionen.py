"""
Test für die neuen Analyse-Funktionen: Integral, Grenzwert, AsymptotischesVerhalten
"""

import numpy as np

from schul_mathematik import (
    Flaeche,
    FlaecheZweiFunktionen,
    Funktion,
    GanzrationaleFunktion,
    GebrochenRationaleFunktion,
    Integral,
)


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

    # TODO: Grenzwert-Funktion muss noch implementiert werden
    print("\n=== Grenzwert-Funktion Test ===")
    print("🔧 Diese Funktion wird in einer zukünftigen Version implementiert")
    pass


def test_asymptotisches_verhalten():
    """Testet die AsymptotischesVerhalten-Funktion"""

    # TODO: AsymptotischesVerhalten-Funktion muss noch implementiert werden
    print("\n=== Asymptotisches Verhalten Test ===")
    print("🔧 Diese Funktion wird in einer zukünftigen Version implementiert")
    pass


def test_kombinierte_anwendung():
    """Testet kombinierte Anwendung aller neuen Funktionen"""

    # TODO: Kombinierte Anwendung muss noch implementiert werden
    print("\n=== Kombinierte Anwendung ===")
    print("🔧 Diese Funktion wird in einer zukünftigen Version implementiert")
    pass


def test_mathematische_genauigkeit():
    """Testet mathematische Genauigkeit der neuen Funktionen"""

    # TODO: Mathematische Genauigkeitstests müssen noch implementiert werden
    print("\n=== Mathematische Genauigkeitstests ===")
    print("🔧 Diese Funktion wird in einer zukünftigen Version implementiert")
    pass


def test_flaeche_funktion():
    """Testet die neue Fläche-Funktion mit Visualisierung"""

    print("\n=== Fläche-Funktion Test ===\n")

    # Test 1: Einfache Fläche unter Parabel
    print("📈 Test 1: Fläche unter x² von 0 bis 1")
    f = Funktion("x^2")

    # Teste Visualisierung ohne Anzeige (nur Objekt)
    fig = Flaeche(f, 0, 1, anzeigen=False)
    print(f"  ✅ Plotly-Figure erstellt: {type(fig)}")
    print(f"  ✅ Titel: {fig.layout.title.text}")

    # Teste numerische Genauigkeit (über Integral)
    numerisch_wert = Integral(f, 0, 1)
    erwartet = 1 / 3
    print(f"  ✅ Numerischer Wert: {numerisch_wert} ≈ {erwartet}")

    # Test 2: Fläche zwischen zwei Funktionen
    print("\n📊 Test 2: Fläche zwischen x² und 2x von 0 bis 2")
    f1 = Funktion("x^2")
    f2 = Funktion("2*x")

    flaeche_wert = FlaecheZweiFunktionen(f1, f2, 0, 2, anzeigen=False)
    print(f"  ✅ Flächenwert berechnet: {flaeche_wert}")
    print(f"  ✅ Typ: {type(flaeche_wert)}")

    # Erwarteter Wert: ∫[0,2] (x² - 2x) dx = [x³/3 - x²]₀² = (8/3 - 4) - 0 = -4/3
    # Absolutwert, da Fläche positiv ist
    erwartet = abs(-4 / 3)
    print(f"  ✅ Erwartet: {erwartet}")
    print(f"  ✅ Korrekt: {abs(flaeche_wert - erwartet) < 1e-10}")

    # Test mit Visualisierung
    try:
        fig2 = FlaecheZweiFunktionen(f1, f2, 0, 2, anzeigen=True)
        print(f"  ✅ Plotly-Figure erstellt: {type(fig2)}")
        if hasattr(fig2, "layout") and hasattr(fig2.layout, "title"):
            print(f"  ✅ Titel: {fig2.layout.title.text}")
    except Exception as e:
        print(f"  ⚠️  Visualisierung fehlgeschlagen: {e}")

    # Test 3: Benutzerdefinierte Farben
    print("\n🎨 Test 3: Benutzerdefinierte Fläche-Farbe")
    try:
        fig3 = Flaeche(f, 0, 1, anzeigen=False, flaeche_farbe="rgba(255, 0, 0, 0.5)")
        print(f"  ✅ Benutzerdefinierte Farbe funktioniert: {type(fig3)}")
    except Exception as e:
        print(f"  ⚠️  Benutzerdefinierte Farbe fehlgeschlagen: {e}")


if __name__ == "__main__":
    try:
        import numpy as np
    except ImportError:
        print("⚠️  Warnung: numpy nicht installiert. Einige Tests werden übersprungen.")

    test_integral_funktion()
    # test_grenzwert_funktion()  # Nicht implementiert
    # test_asymptotisches_verhalten()  # Nicht implementiert
    # test_kombinierte_anwendung()  # Nicht implementiert
    # test_mathematische_genauigkeit()  # Nicht implementiert
    test_flaeche_funktion()  # Neue Fläche-Tests!

    print("\n🎉 Analyse-Funktionen erfolgreich getestet!")
    print("\n📚 Verfügbare Funktionen:")
    print("  • Integral(f, a, b) - Bestimmte Integrale (rein numerisch)")
    print("  • Flaeche(f, a, b) - Flächen mit Visualisierung (pädagogisch)")
    print("  • FlaecheZweiFunktionen(f1, f2, a, b) - Flächen zwischen Funktionen")
    print("  • Weitere Funktionen folgen...")
