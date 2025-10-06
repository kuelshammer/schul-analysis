"""
Komprehensive Demonstration der modernen Magic Factory API

Dieses Beispiel zeigt alle Funktionen der neuen API mit automatischer Funktionserkennung
und wie sie im Unterricht eingesetzt werden können.
"""

import numpy as np

from schul_analysis import *

# =============================================================================
# 1. BEISPIEL: Quadratische Funktion (Magic Factory)
# =============================================================================

print("\n📐 BEISPIEL 1: Quadratische Funktion mit Magic Factory")
print("-" * 55)

# Automatische Funktionserkennung
f = Funktion("3x^2 - 4x + 1")
print(f"f(x) = {f.term()}")

# Analysiere die Funktion mit der neuen Syntax
print(f"Nullstellen: {nullstellen(f)}")
print(f"1. Ableitung: {ableitung(f).term()}")
print(f"2. Ableitung: {ableitung(f, 2).term()}")
print(f"Extrema: {extrema(f)}")
print(f"Symmetrie: {symmetrie(f)}")

# Werteberechnung
print(f"f(0) = {auswerten(f, 0)}")
print(f"f(1) = {auswerten(f, 1)}")

# =============================================================================
# 2. BEISPIEL: Kubische Funktion
# =============================================================================

print("\n=== BEISPIEL 2: Kubische Funktion ===")
print("Kurvendiskussion einer kubischen Funktion")

# Erstelle kubische Funktion
g = erstelle_funktion("x^3 - 3x^2 - 4x + 12")
print(f"g(x) = {g.term()}")

# Volle Analyse
analyse = analysiere_funktion(g)
print(zeige_analyse(g))

# =============================================================================
# 3. BEISPIEL: Lineare Funktionen und Schnittpunkte
# =============================================================================

print("\n=== BEISPIEL 3: Lineare Funktionen ===")

# Zwei lineare Funktionen
f1 = erstelle_polynom([2, 3])  # 2x + 3
f2 = erstelle_polynom([-1, 5])  # -x + 5

print(f"f1(x) = {f1.term()}")
print(f"f2(x) = {f2.term()}")

# Schnittpunkt berechnen (Nullstellen der Differenz)
differenz = erstelle_polynom([3, -2])  # (2x+3) - (-x+5) = 3x - 2
schnittpunkt = nullstellen(differenz)
print(f"Schnittpunkt bei x = {schnittpunkt}")

# =============================================================================
# 4. BEISPIEL: Lineares Gleichungssystem
# =============================================================================

print("\n=== BEISPIEL 4: Lineares Gleichungssystem ===")

# Erstelle LGS: 2x + 3y = 8, x - 2y = -3
lgs = erstelle_lineares_gleichungssystem([[2, 3], [1, -2]], [8, -3])

# Löse das System
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

print("Wertetabelle für f(x) = x² - 2x - 3:")
for x, y in zip(x_werte, y_werte, strict=False):
    print(f"f({x:4.1f}) = {y:6.2f}")

# =============================================================================
# 6. BEISPIEL: Funktion mit Parameter
# =============================================================================

print("\n=== BEISPIEL 6: Funktion mit Parameter ===")


# Normalparabel mit Parameter
def normale_parabel(a=1, b=0, c=0):
    """Erstellt eine Normalparabel f(x) = ax² + bx + c"""
    return erstelle_polynom([c, b, a])


# Verschiedene Parabeln
parabel1 = normale_parabel(1, 0, 0)  # x²
parabel2 = normale_parabel(-1, 0, 0)  # -x²
parabel3 = normale_parabel(2, -4, 3)  # 2x² - 4x + 3

print("Verschiedene Parabeln:")
print(f"f1(x) = {parabel1.term()}")
print(f"f2(x) = {parabel2.term()}")
print(f"f3(x) = {parabel3.term()}")

print("Analysen:")
for i, p in enumerate([parabel1, parabel2, parabel3], 1):
    print(f"  Parabel {i}: Nullstellen bei {nullstellen(p)}, Extremum bei {extrema(p)}")

# =============================================================================
# 7. BEISPIEL: Praktische Anwendung
# =============================================================================

print("\n=== BEISPIEL 7: Praktische Anwendung ===")
print("Ein Ball wird mit v₀ = 20 m/s senkrecht nach oben geworfen")

# Höhenfunktion: h(t) = -5t² + 20t (g ≈ 10 m/s²)
h = erstelle_polynom([0, 20, -5])  # -5t² + 20t

print(f" Höhe: h(t) = {h.term()} m")

# Wann erreicht der Ball die maximale Höhe?
max_zeit = extrema(h)[0][0]  # x-Koordinate des Maximums
max_hoehe = auswerten(h, max_zeit)
print(f"  Maximale Höhe von {max_hoehe} m nach {max_zeit} s")

# Wann landet der Ball wieder?
landezeiten = nullstellen(h)
print(f"  Landung nach {landezeiten[1]} s")

# Geschwindigkeit als 1. Ableitung
v = ableitung(h)
print(f"  Geschwindigkeit: v(t) = {v.term()} m/s")

# =============================================================================
# 8. BEISPIEL: Vergleich von Funktionen
# =============================================================================

print("\n=== BEISPIEL 8: Funktionsvergleich ===")

# Zwei ähnliche Funktionen vergleichen
f_a = erstelle_polynom([1, -3, 2])  # x² - 3x + 2 = (x-1)(x-2)
f_b = erstelle_polynom([1, -4, 4])  # x² - 4x + 4 = (x-2)²

print("Vergleich zweier quadratischer Funktionen:")
print(f"  f_A(x) = {f_a.term()}")
print(f"  f_B(x) = {f_b.term()}")

print("Eigenschaften:")
for name, func in [("f_A", f_a), ("f_B", f_b)]:
    print(f"  {name}:")
    print(f"    Nullstellen: {nullstellen(func)}")
    print(f"    Extrema: {extrema(func)}")
    print(f"    Symmetrie: {symmetrie(func)}")

print("\n=== ENDE DER DEMONSTRATION ===")
print("Die neue API ermöglicht eine intuitive und pädagogisch wertvolle")
print("Arbeit mit mathematischen Funktionen im Schulunterricht.")
