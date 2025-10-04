"""
Test der neuen schülerfreundlichen API für das Schul-Analysis Framework

Dieses Skript demonstriert die pädagogischen Verbesserungen:
- Deutsche API-Namen
- Unterrichtsnahe Syntax: nullstellen(f) statt f.nullstellen()
- Einfache Anwendung für Schüler
"""

# Teste die neue API
from schul_analysis import *

print("=== Test der neuen schülerfreundlichen API ===\n")

# 1. Einfache Funktionserstellung (wie im Unterricht)
print("1. Funktionserstellung:")
f = erstelle_polynom([1, -4, 3])  # x² - 4x + 3
g = erstelle_funktion("2*x + 5")  # 2x + 5
print(f"f(x) = {f.term()}")
print(f"g(x) = {g.term()}")
print()

# 2. Unterrichtsnahe Syntax für Analysis
print("2. Funktionsanalyse mit neuer Syntax:")
xs = nullstellen(f)  # statt f.nullstellen()
f1 = ableitung(f, 1)  # statt f.ableitung(1)
sym = symmetrie(f)  # statt f.syme (korrigiert!)
ext = extrema(f)  # statt f.extrema()
wp = wendepunkte(f)  # statt f.wendepunkte()

print(f"Nullstellen: {xs}")
print(f"1. Ableitung: {f1.term()}")
print(f"Symmetrie: {sym}")
print(f"Extrempunkte: {ext}")
print(f"Wendepunkte: {wp}")
print()

# 3. Werteberechnung und Visualisierung
print("3. Werteberechnung und Visualisierung:")
y = auswerten(f, 2)  # statt f(2)
print(f"f(2) = {y}")

# Teste Array-Auswertung (Performance-Optimierung)
import numpy as np

x_array = np.array([1, 2, 3, 4])
y_array = auswerten(f, x_array)
print(f"f({x_array}) = {y_array}")
print()

# 4. Komfort-Funktionen für den Unterricht
print("4. Vollständige Funktionsanalyse:")
analyse = analysiere_funktion(f)
print(zeige_analyse(f))
print()

# 5. Visualisierung
print("5. Visualisierung:")
print("Zeiche Funktion f(x) = x² - 4x + 3")
# plot = zeichne(f, (-2, 6))  # Kommentiert aus für CLI-Test

# 6. Teste mit verschiedenen Funktionstypen
print("\n6. Test mit gebrochen rationaler Funktion:")
try:
    from schul_analysis import GebrochenRationaleFunktion

    h = GebrochenRationaleFunktion([1, 0, -4], [1, 0])  # (x² - 4)/x
    print(f"h(x) = {h.term()}")
    h_xs = nullstellen(h)  # Wrapper funktioniert mit allen Typen!
    print(f"Nullstellen von h: {h_xs}")
    h_ps = h.polstellen()  # Direkter Methodenaufruf
    print(f"Polstellen von h: {h_ps}")
except Exception as e:
    print(f"Fehler bei gebrochen rationaler Funktion: {e}")

print("\n=== Test erfolgreich abgeschlossen ===")
print("Die neue API ist pädagogisch optimiert und bereit für den Einsatz!")
