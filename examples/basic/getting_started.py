"""
Getting Started mit dem Schul-Analysis Framework

Dieses Beispiel zeigt die grundlegende Verwendung des modernen Schul-Analysis Frameworks
mit Magic Factory Pattern für die mathematische Analyse von Funktionen.
"""

import os
import sys

# Add src directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

from schul_analysis import Funktion, Nullstellen, Ableitung, Extrema, Zeichne

print("🎯 Schul-Analysis Framework - Erste Schritte")
print("=" * 50)

# 1. Magic Factory: Automatische Funktionserkennung
print("\n🔧 1. Magic Factory - Automatische Typ-Erkennung")
print("-" * 45)

# Verschiedene Wege zur Funktionserstellung
f1 = Funktion("x^2 - 4x + 3")  # String-Eingabe (intuitiv)
f2 = Funktion([1, -4, 3])  # Liste (traditionell)
f3 = Funktion({2: 1, 1: -4, 0: 3})  # Dictionary (experten-modus)

print(f"String-Eingabe:  f(x) = {f1.term()}")
print(f"Listen-Eingabe:   f(x) = {f2.term()}")
print(f"Dict-Eingabe:     f(x) = {f3.term()}")
print(f"Erkannter Typ:    {type(f1).__name__}")

# 2. Natürliche mathematische Syntax
print("\n📐 2. Natürliche mathematische Syntax")
print("-" * 40)

# Funktionswerte berechnen
print(f"f(0) = {f1(0)}")  # f(0) statt f1.wert(0)
print(f"f(2) = {f1(2)}")  # f(2) statt f1.wert(2)

# Ableitungen mit Prime-Notation
f_strich = Ableitung(f1)  # f' = df/dx
print(f"f'(x) = {f_strich.term()}")
print(f"f'(2) = {f_strich(2)}")  # f'(2) statt f1.ableitung().wert(2)

# Zweite Ableitung
f_zwei_strich = Ableitung(f_strich)  # f'' = d²f/dx²
print(f"f''(x) = {f_zwei_strich.term()}")
print(f"f''(2) = {f_zwei_strich(2)}")

# 3. Pädagogische Wrapper-API
print("\n🎓 3. Pädagogische Wrapper-API (deutsch)")
print("-" * 45)

# Funktion statt Methodenaufrufe
xs = Nullstellen(f1)  # statt f1.nullstellen()
ext = Extrema(f1)  # statt f1.extremstellen()

print(f"Nullstellen: {xs}")
print(f"Extremstellen: {ext}")

# 4. Umfassende Funktionsanalyse
print("\n📊 4. Umfassende Funktionsanalyse")
print("-" * 38)

print(f"Funktionstyp:     {f1.funktionstyp}")
print(f"Definitionsbereich: {f1.definitionsbereich()}")
print(f"Wertebereich:     {f1.wertebereich()}")
print(f"Symmetrie:        {f1.symmetrie()}")

# 5. Parametrisierte Funktionen
print("\n🔍 5. Parametrisierte Funktionen")
print("-" * 35)

f_param = Funktion("a*x^2 + b*x + c")
print(f"Parametrisch: f(x) = {f_param.term()}")
print(f"Parameter:      {f_param.parameter}")
print(f"Freie Symbole:  {f_param.term_sympy.free_symbols}")

# Parameter setzen und analysieren
f_spezial = f_param.setze_parameter(a=2, b=3)
print(f"Mit a=2, b=3:  f(x) = {f_spezial.term()}")

# Kombinierte Nutzung: f[parameter_werte](x)
result = f_param.setze_parameter(a=2, b=1, c=0)(3)
print(f"f[2,1,0](3) = {result}")  # 2*9 + 1*3 + 0 = 21

# 6. Erweiterte Funktionstypen
print("\n🏗️ 6. Erweiterte Funktionstypen")
print("-" * 35)

# Verschiedene Funktionstypen werden automatisch erkannt
funktionen = [
    ("Linear", "2x + 3"),
    ("Quadratisch", "x^2 - 4x + 3"),
    ("Kubisch", "x^3 - 2x^2 - x + 2"),
    ("Rational", "(x^2 + 1)/(x - 1)"),
    ("Exponentiell", "e^x"),
    ("Trigonometrisch", "sin(x) + cos(x)"),
]

for name, term in funktionen:
    try:
        f = Funktion(term)
        print(f"{name:15} → {f.funktionstyp:20} | {term}")
    except Exception as e:
        print(f"{name:15} → Fehler: {e}")

# 7. Visualisierung (Plotly)
print("\n📈 7. Mathematisch korrekte Visualisierung")
print("-" * 42)

try:
    # Perfekte Parabel-Darstellung mit Plotly
    print("Erstelle perfekte Parabel-Darstellung...")

    # Zeige Funktion (mathematisch korrekt)
    graph = Zeichne(f1, x_bereich=(-1, 5))
    print("✅ Graph erfolgreich erstellt!")
    print(f"   Typ: {type(graph).__name__}")
    print(f"   Bereich: x ∈ [-1, 5]")
    print(f"   Nullstellen: bei {xs}")

    # In interaktiven Umgebungen (Jupyter, Marimo):
    # graph.show()  # Zeigt den interaktiven Graph

except ImportError as e:
    print(f"⚠️  Visualisierung nicht verfügbar: {e}")
    print("   Installieren Sie mit: uv sync --group viz-math")
except Exception as e:
    print(f"⚠️  Fehler bei Visualisierung: {e}")

# 8. Praktische Anwendungsbeispiele
print("\n🎯 8. Praktische Anwendungsbeispiele")
print("-" * 40)

# Beispiel: Parabel durch drei Punkte finden
print("Beispiel: Parabel durch Punkte P(1|2), Q(2|3), R(3|6)")
from schul_analysis import LGS, Parameter, Variable

a, b, c = Parameter("a"), Parameter("b"), Parameter("c")
x = Variable("x")
f_pts = Funktion([a, b, c], [x])  # ax² + bx + c

# Lineares Gleichungssystem aufstellen
gl1 = f_pts(1) == 2  # a + b + c = 2
gl2 = f_pts(2) == 3  # 4a + 2b + c = 3
gl3 = f_pts(3) == 6  # 9a + 3b + c = 6

lgs = LGS(gl1, gl2, gl3)
loesung = lgs.löse()

print(f"Lösung: {loesung}")
if loesung:
    final_f = Funktion(f"{loesung[a]}*x^2 + {loesung[b]}*x + {loesung[c]}")
    print(f"Ergebnis: f(x) = {final_f.term()}")

print("\n" + "=" * 50)
print("✨ Zusammenfassung: Magic Factory Vorteile")
print("=" * 50)
print("🔥 Automatische Funktionserkennung")
print("📐 Natürliche mathematische Syntax (f(x), f')")
print("🎓 Deutsche pädagogische API")
print("🔍 Parametrische Funktionen mit setze_parameter()")
print("📊 Mathematisch korrekte Visualisierung")
print("🧮 Symbolische Exaktheit mit SymPy")
print("🎯 Intuitiv für Schüler und Lehrer")

print("\n🚀 Nächste Schritte:")
print("• uv sync --group viz-math  # Für Visualisierung")
print("• siehe examples/advanced/  # Fortgeschrittene Beispiele")
print("• siehe docs/               # Methoden-Dokumentation")
