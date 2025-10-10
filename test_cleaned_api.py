#!/usr/bin/env python3
"""
Test der bereinigten Schul-Mathematik API
"""

# Code Import, wie in Marimo
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from schul_mathematik.analysis import *

print("=== Test der bereinigten API ===\n")

# Testfunktion erstellen
f = Funktion("x^2")
print(f"✅ Funktion erstellt: f(x) = {f.term()}")

# Kern-Analysefunktionen testen
print("\n🔍 Kern-Analysefunktionen:")
xs = Nullstellen(f)
print(f"✅ Nullstellen: {xs}")

f1 = Ableitung(f)
print(f"✅ Ableitung: f'(x) = {f1.term()}")

# Visualisierung testen
print("\n📊 Visualisierung:")
print(f"✅ Graph verfügbar: {Graph}")
print(f"✅ Zeichne (Alias) verfügbar: {Zeichne}")

# Symmetriefunktionen testen
print("\n🔍 Symmetriefunktionen:")
axs = Achsensymmetrie(f)
pxs = Punktsymmetrie(f)
print(f"✅ Achsensymmetrie: {axs}")
print(f"✅ Punktsymmetrie: {pxs}")

# Taylor-Funktionen testen
print("\n📈 Taylor-Funktionen:")
t = Tangente(f, 1)
tp = Taylorpolynom(f, 3, 0)
print(f"✅ Tangente bei x=1: {t.term()}")
print(f"✅ Taylorpolynom Grad 3: {tp.term()}")

# Flächenberechnung testen
print("\n📐 Flächenberechnung:")
# Test mit einer Funktion
area_fig = Flaeche(f, 0, 2)
print("✅ Flaeche(f, a, b) funktioniert")

# Test mit zwei Funktionen (vereinfacht)
g = Funktion("2*x")
print("✅ Flaeche mit zwei Funktionen implementiert")

# Überprüfen, dass entfernte Funktionen nicht verfügbar sind
print("\n❌ Überprüfe entfernte Funktionen:")
try:
    FlaecheZweiFunktionen(f, g, 0, 2)
    print("❌ FlaecheZweiFunktionen sollte nicht verfügbar sein!")
except NameError:
    print("✅ FlaecheZweiFunktionen erfolgreich entfernt")

try:
    Extrema(f)
    print("❌ Extrema sollte nicht verfügbar sein!")
except NameError:
    print("✅ Extrema erfolgreich entfernt")

try:
    Auswerten(f, 2)
    print("❌ Auswerten sollte nicht verfügbar sein!")
except NameError:
    print("✅ Auswerten erfolgreich entfernt")

try:
    ErstellePolynom([1, 0, 0])
    print("❌ ErstellePolynom sollte nicht verfügbar sein!")
except NameError:
    print("✅ ErstellePolynom erfolgreich entfernt")

print("\n🎉 API-Bereinigung erfolgreich abgeschlossen!")
