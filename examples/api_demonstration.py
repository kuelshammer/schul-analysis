"""
Komprehensive Demonstration der modernen Magic Factory API

Dieses Beispiel zeigt alle Funktionen der neuen API mit automatischer Funktionserkennung
und wie sie im Unterricht eingesetzt werden können.
"""

import numpy as np
from schul_analysis import (
    Funktion,
    Nullstellen,
    Ableitung,
    Extrema,
    Zeichne,
    LGS,
    Parameter,
    Variable,
)

print("🎯 Schul-Analysis Framework - Komprehensive API Demonstration")
print("=" * 70)

# =============================================================================
# 1. BEISPIEL: Quadratische Funktion (Magic Factory)
# =============================================================================

print("\n📐 BEISPIEL 1: Quadratische Funktion mit Magic Factory")
print("-" * 55)

# Automatische Funktionserkennung
f = Funktion("3x^2 - 4x + 1")
print(f"f(x) = {f.term()}")
print(f"Erkannter Typ: {f.funktionstyp}")

# Natürliche mathematische Syntax
print(f"\nFunktionswerte:")
print(f"f(0) = {f(0)}")
print(f"f(1) = {f(1)}")
print(f"f(2) = {f(2)}")

# Analysen mit pädagogischer API
print(f"\nAnalyse:")
print(f"Nullstellen: {Nullstellen(f)}")
print(f"1. Ableitung f'(x) = {Ableitung(f).term()}")
print(f"2. Ableitung f''(x) = {Ableitung(f, 2).term()}")
print(f"Extrema: {Extrema(f)}")
print(f"Symmetrie: {f.symmetrie()}")

# =============================================================================
# 2. BEISPIEL: Kubische Funktion mit erweiterter Analyse
# =============================================================================

print("\n📊 BEISPIEL 2: Kubische Funktion - Volle Analyse")
print("-" * 50)

g = Funktion("x^3 - 3x^2 - 4x + 12")
print(f"g(x) = {g.term()}")
print(f"Typ: {g.funktionstyp}")

# Umfassende Analyse
print(f"\nEigenschaften:")
print(f"Definitionsbereich: {g.definitionsbereich()}")
print(f"Wertebereich: {g.wertebereich()}")
print(f"Nullstellen: {Nullstellen(g)}")
print(f"Extremstellen: {Extrema(g)}")
print(f"Wendepunkte: {g.wendepunkte()}")
print(f"Monotonie: {g.monotonie()}")
print(f"Krümmung: {g.kruemmung()}")

# =============================================================================
# 3. BEISPIEL: Lineare Funktionen und Schnittpunkte
# =============================================================================

print("\n📏 BEISPIEL 3: Lineare Funktionen - Schnittpunkte")
print("-" * 48)

# Automatische Erkennung linearer Funktionen
f1 = Funktion("2x + 3")
f2 = Funktion("-x + 5")

print(f"f1(x) = {f1.term()} (Typ: {f1.funktionstyp})")
print(f"f2(x) = {f2.term()} (Typ: {f2.funktionstyp})")

# Eigenschaften linearer Funktionen
print(f"\nEigenschaften:")
print(f"f1: Steigung = {f1.steigung()}, y-Achsenabschnitt = {f1.y_achsenabschnitt()}")
print(f"f2: Steigung = {f2.steigung()}, y-Achsenabschnitt = {f2.y_achsenabschnitt()}")

# Schnittpunkt berechnen
print(f"\nSchnittpunktberechnung:")
# Methode 1: Differenzfunktion
differenz = Funktion("(2x + 3) - (-x + 5)")  # 3x - 2
schnittpunkt_x = Nullstellen(differenz)[0]
schnittpunkt_y = f1(schnittpunkt_x)
print(f"Schnittpunkt: ({schnittpunkt_x}, {schnittpunkt_y})")

# Methode 2: Direktes Lösen
print(f"Überprüfung f1({schnittpunkt_x}) = {f1(schnittpunkt_x)}")
print(f"Überprüfung f2({schnittpunkt_x}) = {f2(schnittpunkt_x)}")

# =============================================================================
# 4. BEISPIEL: Parametrisierte Funktionen mit setze_parameter()
# =============================================================================

print("\n🔍 BEISPIEL 4: Parametrisierte Funktionen - Neue setze_parameter() API")
print("-" * 62)

# Parametrische Funktion erstellen
f_param = Funktion("a*x^2 + b*x + c")
print(f"Parametrisch: f(x) = {f_param.term()}")
print(f"Parameter: {f_param.parameter}")

# Parameter setzen und analysieren
print(f"\nParameter-Substitution:")
f2 = f_param.setze_parameter(a=2, b=3)
print(f"Mit a=2, b=3: f(x) = {f2.term()}")

f3 = f_param.setze_parameter(a=1, b=-4, c=3)
print(f"Mit a=1, b=-4, c=3: f(x) = {f3.term()}")

# Kombinierte Nutzung: f[parameter](x)
result = f_param.setze_parameter(a=3)(2)
print(f"f[3](2) = {result}")  # 3*4 + b*2 + c = 12 + 2b + c

# =============================================================================
# 5. BEISPIEL: Lineare Gleichungssysteme (LGS) mit Funktionen
# =============================================================================

print("\n⚖️ BEISPIEL 5: Lineare Gleichungssysteme mit Funktionen")
print("-" * 54)

# LGS für Parabel durch drei Punkte
a, b, c = Parameter("a"), Parameter("b"), Parameter("c")
x = Variable("x")
f_lgs = Funktion([a, b, c], [x])  # ax² + bx + c

print("Finde Parabel durch P(1|2), Q(2|3), R(3|6)")

# Bedingungen als Gleichungen aufstellen
bedingungen = [
    f_lgs(1) == 2,  # a + b + c = 2
    f_lgs(2) == 3,  # 4a + 2b + c = 3
    f_lgs(3) == 6,  # 9a + 3b + c = 6
]

# LGS erstellen und lösen
lgs = LGS(*bedingungen)
try:
    loesung = lgs.löse()
    print(f"Lösung: {loesung}")

    # Ergebnis als konkrete Funktion
    if loesung:
        ergebnis_funktion = Funktion(
            f"{loesung[a]}*x^2 + {loesung[b]}*x + {loesung[c]}"
        )
        print(f"Gefundene Parabel: f(x) = {ergebnis_funktion.term()}")

        # Verifizierung
        print(f"Verifizierung:")
        print(f"  f(1) = {ergebnis_funktion(1)} (sollte 2 sein)")
        print(f"  f(2) = {ergebnis_funktion(2)} (sollte 3 sein)")
        print(f"  f(3) = {ergebnis_funktion(3)} (sollte 6 sein)")

except Exception as e:
    print(f"Fehler bei LGS-Lösung: {e}")

# =============================================================================
# 6. BEISPIEL: Wertetabelle mit verschiedenen Funktionstypen
# =============================================================================

print("\n📋 BEISPIEL 6: Wertetabelle mit verschiedenen Funktionstypen")
print("-" * 52)

# Verschiedene Funktionstypen
funktionen = [
    ("Linear", "2x + 1"),
    ("Quadratisch", "x^2 - 2x - 3"),
    ("Kubisch", "0.5x^3 - x"),
    ("Exponentiell", "e^x"),
    ("Trigonometrisch", "sin(x)"),
]

x_werte = np.linspace(-2, 2, 9)  # 9 Punkte von -2 bis 2

print(f"{'Funktion':<15} | {'Typ':<15} | {'Werte':<40}")
print("-" * 75)

for name, term in funktionen:
    try:
        f = Funktion(term)
        y_werte = [f(x) for x in x_werte]
        werte_str = ", ".join([f"{y:.2f}" for y in y_werte])
        print(f"{name:<15} | {f.funktionstyp:<15} | {werte_str}")
    except Exception as e:
        print(f"{name:<15} | Fehler: {e}")

# =============================================================================
# 7. BEISPIEL: Praktische Anwendung - Physik
# =============================================================================

print("\n🚀 BEISPIEL 7: Praktische Anwendung - Physik")
print("-" * 48)

print("Problem: Ein Ball wird mit v₀ = 20 m/s senkrecht nach oben geworfen")
print("g ≈ 10 m/s², Luftvernachlässigung vernachlässigt")

# Höhenfunktion: h(t) = -5t² + 20t
h = Funktion("-5t^2 + 20t")
print(f"Höhenfunktion: h(t) = {h.term()} m")

# Physikalische Analyse
print(f"\nPhysikalische Analyse:")
geschwindigkeit = Ableitung(h)
beschleunigung = Ableitung(geschwindigkeit)

print(f"Geschwindigkeit: v(t) = {geschwindigkeit.term()} m/s")
print(f"Beschleunigung: a(t) = {beschleunigung.term()} m/s²")

# Maximale Höhe
extremstellen = Extrema(h)
if extremstellen:
    max_zeit = extremstellen[0][0]
    max_hoehe = h(max_zeit)
    print(f"Maximale Höhe: {max_hoehe:.1f} m nach {max_zeit:.1f} s")

# Landezeit
nullstellen = Nullstellen(h)
if len(nullstellen) >= 2:
    landezeit = nullstellen[1]  # Zweite Nullstelle (t > 0)
    print(f"Landezeit: {landezeit:.1f} s")
    print(f"Landegeschwindigkeit: {geschwindigkeit(landezeit):.1f} m/s")

# =============================================================================
# 8. BEISPIEL: Erweiterte Funktionstypen
# =============================================================================

print("\n🏗️ BEISPIEL 8: Magic Factory - Verschiedene Funktionstypen")
print("-" * 55)

# Teste die automatische Erkennung mit komplexen Funktionen
test_funktionen = [
    ("Rationale Funktion", "(x^2 + 1)/(x - 1)"),
    ("Gemischt", "sin(x) + x^2"),
    ("Produkt", "x * sin(x)"),
    ("Summe", "e^x + x^3"),
    ("Bruch", "1/(x^2 + 1)"),
    ("Wurzel", "sqrt(x^2 + 1)"),
    ("Logarithmus", "ln(x + 1)"),
]

print(f"{'Eingabe':<25} | {'Erkannter Typ':<20} | {'Erfolg'}")
print("-" * 60)

for beschreibung, term in test_funktionen:
    try:
        f = Funktion(term)
        print(f"{beschreibung:<25} | {f.funktionstyp:<20} | ✅")
    except Exception as e:
        print(f"{beschreibung:<25} | Fehler: {str(e):<18} | ❌")

# =============================================================================
# 9. BEISPIEL: Taylor-Reihenentwicklung
# =============================================================================

print("\n📐 BEISPIEL 9: Taylor-Reihenentwicklung")
print("-" * 40)

from schul_analysis import Taylorpolynom

# Funktion für Taylor-Entwicklung
f_taylor = Funktion("sin(x)")
print(f"Original: f(x) = {f_taylor.term()}")

# Taylor-Polynome verschiedenen Grades
for grad in [1, 3, 5, 7]:
    taylor = Taylorpolynom(f_taylor, entwicklungspunkt=0, grad=grad)
    print(f"Taylor {grad}. Ordnung: {taylor.term()}")

# Vergleich an einem Punkt
x_test = 1.0
print(f"\nVergleich bei x = {x_test}:")
print(f"f({x_test}) = {f_taylor(x_test):.6f}")
for grad in [1, 3, 5, 7]:
    taylor = Taylorpolynom(f_taylor, entwicklungspunkt=0, grad=grad)
    approx = taylor(x_test)
    fehler = abs(approx - f_taylor(x_test))
    print(f"Taylor {grad}: {approx:.6f} (Fehler: {fehler:.2e})")

# =============================================================================
# 10. BEISPIEL: Visualisierungs-Strategien
# =============================================================================

print("\n📊 BEISPIEL 10: Visualisierungs-Strategien")
print("-" * 45)

f_vis = Funktion("x^3 - 3x^2 - 9x + 5")

print("Visualisierungsmöglichkeiten:")
print("1. Plotly (mathematisch korrekt)")
print("2. Altair (statistisch)")
print("3. Matplotlib (statisch)")

try:
    # Plotly-Visualisierung (empfohlen)
    graph_plotly = Zeichne(f_vis, x_bereich=(-3, 5))
    print("✅ Plotly-Graph erstellt (mathematisch korrekt)")
    print("   Features: Aspect Ratio Control, Interaktivität")

    # In interaktiven Umgebungen:
    # graph_plotly.show()

except Exception as e:
    print(f"⚠️  Plotly nicht verfügbar: {e}")

print("\n" + "=" * 70)
print("🎉 ZUSAMMENFASSUNG: Magic Factory API Vorteile")
print("=" * 70)

print("✨ Automatische Funktionserkennung - Eine API für alle Typen")
print("📐 Natürliche mathematische Syntax - f(x), f'(x)")
print("🎓 Deutsche pädagogische API - Nullstellen(f), Ableitung(f)")
print("🔍 setze_parameter() - Intuitive Parameter-Substitution")
print("📊 Mathematisch korrekte Visualisierung")
print("⚖️ LGS-Löser mit Funktionsbedingungen")
print("🧮 Symbolische Exaktheit mit SymPy")
print("🚀 Modernes uv-basiertes Dependency Management")

print(f"\n📈 Framework-Statistik:")
print(f"• Unterstützte Funktionstypen: 6+ Hauptkategorien")
print(f"• Mathematische Methoden: 50+ Funktionen")
print(f"• Visualisierungs-Backends: Plotly, Altair, Matplotlib")
print(f"• Test-Coverage: >80%")
print(f"• Python-Version: 3.11+")

print("\n🎯 Einsatzbereiche:")
print("• Mittelstufe: Lineare/quadratische Funktionen")
print("• Oberstufe: Kurvendiskussion, Analysis")
print("• Studienvorbereitung: Symbolische Mathematik")
print("• Lehrer: Unterrichtsvorbereitung, Demonstration")

print("\n🔧 Nächste Schritte:")
print("• uv sync --group viz-math    # Für Visualisierung")
print("• siehe examples/advanced/     # Weitere Beispiele")
print("• siehe docs/                  # Methoden-Dokumentation")
