"""
Getting Started mit dem Schul-Analysis Framework

Dieses Beispiel zeigt die grundlegende Verwendung des modernen Schul-Analysis Frameworks
mit Magic Factory Pattern für die mathematische Analyse von Funktionen.
"""

# Moderne Importe - kein manuelles Pfad-Management mehr nötig!
from schul_analysis import Funktion, ableitung, extrema, nullstellen

# 1. Funktion mit Magic Factory erstellen
print("=== 1. Funktion mit Magic Factory ===")
f = Funktion("x^2 - 4x + 3")  # Automatische Erkennung als quadratische Funktion
print(f"Funktion: f(x) = {f.term()}")
print(f"Funktionstyp: {f.funktionstyp}")
print(f"Nullstellen: {nullstellen(f)}")

# 2. Ableitungen berechnen
print("\n=== 2. Ableitungen ===")
f_strich = ableitung(f)  # Automatische Namensgebung: f'
print(f"f'(x) = {f_strich.term()}")
print(f"Name der Ableitung: {f_strich.name}")
print(f"Nullstellen der Ableitung: {nullstellen(f_strich)}")

# 3. Extremstellen finden
print("\n=== 3. Extremstellen ===")
extremstellen = extrema(f)
print(f"Extremstellen: {extremstellen}")

# 4. Werteberechnung
print("\n=== 4. Funktionswerte ===")
print(f"f(0) = {f(0)}")
print(f"f(2) = {f(2)}")
print(f"f(4) = {f(4)}")

# 5. Zweite Ableitung
print("\n=== 5. Zweite Ableitung ===")
f_strich_strich = ableitung(f_strich)  # Automatische Namensgebung: f''
print(f"f''(x) = {f_strich_strich.term()}")
print(f"Name der zweiten Ableitung: {f_strich_strich.name}")

# 6. Visualisierung (funktioniert nur mit Plotly)
print("\n=== 6. Visualisierung ===")
try:
    graph = f.zeige_funktion_plotly(x_bereich=(-1, 5))
    print("Graph erfolgreich erstellt!")
    print(f"Graph-Typ: {type(graph)}")
    # In einem interaktiven Environment:
    # graph.show()
except ImportError:
    print("Plotly nicht installiert - für Visualisierung: uv sync --group viz-math")
except Exception as e:
    print(f"Fehler bei der Visualisierung: {e}")

print("\n=== 7. Zusammenfassung ===")
print("Das moderne Schul-Analysis Framework bietet:")
print("- ✅ Magic Factory: Funktion('x^2 - 4x + 3') - einfache Erstellung")
print("- ✅ Automatische Typenerkennung: erkennt quadratische Funktionen automatisch")
print("- ✅ Intuitive API: nullstellen(f), ableitung(f), extrema(f)")
print("- ✅ Automatische Namensgebung: f -> f' -> f''")
print("- ✅ LaTeX-Darstellung: f zeigt automatisch f(x) = x^2 - 4x + 3 an")
print("- ✅ Plotly-Integration für mathematisch korrekte Graphen")
print("- ✅ Perfekt für den Matheunterricht und wissenschaftliche Arbeiten")
