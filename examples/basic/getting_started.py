"""
Getting Started with Schul-Analysis Framework

Dieses Beispiel zeigt die grundlegende Verwendung des Schul-Analysis Frameworks
für die mathematische Analyse von Funktionen.
"""

import os
import sys

# Add src directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

from schul_analysis import (
    Ableitung,
    Extremstellen,
    GanzrationaleFunktion,
    Graph,
    Nullstellen,
)

# 1. Einfache ganzrationale Funktion erstellen
print("=== 1. Einfache ganzrationale Funktion ===")
f1 = GanzrationaleFunktion([1, -4, 3])  # x^2 - 4x + 3
print(f"Funktion: f(x) = {f1.term()}")
print(f"Nullstellen: {Nullstellen(f1)}")

# 2. Ableitungen berechnen
print("\n=== 2. Ableitungen ===")
f1_strich = Ableitung(f1)
print(f"f'(x) = {f1_strich.term()}")
print(f"Nullstellen der Ableitung: {Nullstellen(f1_strich)}")

# 3. Extremstellen finden
print("\n=== 3. Extremstellen ===")
extremstellen = Extremstellen(f1)
print(f"Extremstellen: {extremstellen}")

# 4. Visualisierung (funktioniert nur in interaktiven Umgebungen)
print("\n=== 4. Visualisierung ===")
print("Erstelle Graph...")
try:
    # Note: Graph function works with Funktion class, not GanzrationaleFunktion
    from schul_analysis import Funktion as UnifiedFunktion

    f_unified = UnifiedFunktion("x^2 - 4x + 3")
    graph = Graph(f_unified, x_bereich=(-1, 5))
    print("Graph erfolgreich erstellt!")
    print(f"Graph-Typ: {type(graph)}")
    # In einem interaktiven Environment:
    # graph.show()
except Exception as e:
    print(f"Fehler bei der Visualisierung: {e}")

print("\n=== 6. Zusammenfassung ===")
print("Das Schul-Analysis Framework bietet:")
print("- Vereinheitlichte API für ganzrationale und gebrochen-rationale Funktionen")
print("- Automatische Berechnung von Nullstellen, Ableitungen, Extremstellen")
print("- Intelligente Visualisierung mit Plotly")
print("- Perfekt für den Matheunterricht und wissenschaftliche Arbeiten")
