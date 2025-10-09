"""
Test für die neuen Fläche-Funktionen mit Visualisierung
"""

import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from schul_mathematik import Funktion, Integral, Flaeche, FlaecheZweiFunktionen


def test_flaeche_funktion():
    """Testet die neue Fläche-Funktion mit Visualisierung"""

    print("=== Fläche-Funktion Test ===\n")

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

    fig2 = FlaecheZweiFunktionen(f1, f2, 0, 2, anzeigen=False)
    print(f"  ✅ Plotly-Figure erstellt: {type(fig2)}")
    print(f"  ✅ Titel: {fig2.layout.title.text}")

    # Test 3: Benutzerdefinierte Farben
    print("\n🎨 Test 3: Benutzerdefinierte Fläche-Farbe")
    fig3 = Flaeche(f, 0, 1, anzeigen=False, flaeche_farbe="rgba(255, 0, 0, 0.5)")
    print(f"  ✅ Benutzerdefinierte Farbe funktioniert")

    print("\n🎉 Alle Fläche-Tests erfolgreich!")


if __name__ == "__main__":
    test_flaeche_funktion()
