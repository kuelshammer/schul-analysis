#!/usr/bin/env python3
"""
Demonstration der LaTeX-Darstellung in Marimo

Dieses Beispiel zeigt, wie man die neue Term() Funktion in Marimo-Notebooks
verwendet, um schöne mathematische Darstellungen zu erzeugen.
"""

import sys

sys.path.insert(0, "/Users/max/Python/Schul-Analysis/src")

from schul_analysis import Ableitung, Funktion, Nullstellen

# Beispiel 1: Einfache quadratische Funktion
print("=== Beispiel 1: Quadratische Funktion ===")
f = Funktion("x^2 - 4x + 3")

# Zeige die Funktion in schöner LaTeX-Darstellung
print("Funktion:")
print(f"f(x) = {f.term()}")
print(f"LaTeX-Darstellung: {f.latex_display()}")

# Berechne Nullstellen
nullstellen = Nullstellen(f)
print(f"Nullstellen: {nullstellen}")

# Beispiel 2: Ableitung
print("\n=== Beispiel 2: Ableitung ===")
f1 = Ableitung(f)
print(f"f'(x) = {f1.term()}")
print(f"LaTeX-Darstellung: {f1.latex_display()}")

# Beispiel 3: Komplexere Funktion
print("\n=== Beispiel 3: Komplexere Funktion ===")
g = Funktion("sin(x) + exp(x)")
print(f"g(x) = {g.term()}")
print(f"LaTeX-Darstellung: {g.latex_display()}")

# Beispiel 4: Gebrochen-rationale Funktion
print("\n=== Beispiel 4: Gebrochen-rationale Funktion ===")
h = Funktion("(x^2 - 1)/(x - 1)")
print(f"h(x) = {h.term()}")
print(f"LaTeX-Darstellung: {h.latex_display()}")

print("\n=== Verwendung in Marimo ===")
print("In einem Marimo-Notebook könntest du schreiben:")
print("```python")
print("import marimo as mo")
print("from schul_analysis import Funktion, Term")
print("")
print("f = Funktion('x^2 - 4x + 3')")
print("Term(f)  # Zeigt schöne LaTeX-Darstellung")
print("")
print("# Und trotzdem funktioniert noch:")
print("g = Funktion('2*x + 1')")
print("h = f + g  # Dies gibt einen SymPy-Ausdruck zurück")
print("Term(h)  # Zeigt das Ergebnis in LaTeX")
print("```")

print("\n=== Vorteile dieser Lösung ===")
print("✅ Schöne LaTeX-Darstellung mit Term(f)")
print("✅ Funktionen geben SymPy-Ausdrücke zurück (für Arithmetik)")
print("✅ Keine Konflikte mit bestehendem Code")
print("✅ Einfache Integration in Marimo-Notebooks")
print("✅ Fallback für Nicht-Marimo-Umgebungen")
