#!/usr/bin/env python3
"""
Anleitung: Parametrische Funktionen im Schul-Analysis Framework

Dieses Skript zeigt alle Möglichkeiten, parametrische Funktionen zu definieren und zu verwenden.
"""

import sys

sys.path.insert(0, "src")

# =============================================================================
# MÖGLICHKEIT 1: Einfachster Weg (vordefinierte Objekte nutzen)
# =============================================================================

print("=== MÖGLICHKEIT 1: Vordefinierte Objekte nutzen ===")

# Importiere vordefinierte Variablen und Parameter
from schul_analysis import ParametrischeFunktion, a, k, t, x

# Definition: f_a(x) = a*x^2 + x
f1 = ParametrischeFunktion([0, 1, a], [x])  # Koeffizienten: [0, 1, a] = 0 + 1*x + a*x^2
print(f"f1(x) = {f1.term()}")

# Definition: g_k(t) = k*t^3 + 2*t
g1 = ParametrischeFunktion([0, 2, 0, k], [t])  # [0, 2, 0, k] = 0 + 2*t + 0*t^2 + k*t^3
print(f"g1(t) = {g1.term()}")

# =============================================================================
# MÖGLICHKEIT 2: Eigene Variablen/Parameter definieren
# =============================================================================

print("\n=== MÖGLICHKEIT 2: Eigene Variablen/Parameter definieren ===")

# Importiere die Klassen
from schul_analysis import Parameter, ParametrischeFunktion, Variable

# Definiere eigene Variablen und Parameter
mein_x = Variable("x")
mein_a = Parameter("alpha")  # Griechische Buchstaben sind auch möglich
mein_b = Parameter("beta")

# Definition: h_α,β(x) = α*x^2 + β*x + 1
h1 = ParametrischeFunktion([1, mein_b, mein_a], [mein_x])  # [1, β, α] = 1 + β*x + α*x^2
print(f"h1(x) = {h1.term()}")

# =============================================================================
# MÖGLICHKEIT 3: Kombination mit konkreten Funktionen
# =============================================================================

print("\n=== MÖGLICHKEIT 3: Konkrete Funktionen ableiten ===")

# Erstelle konkrete Funktionen mit bestimmten Parameterwerten
f_konkret_a2 = f1.mit_wert(a=2)  # f_2(x) = 2x^2 + x
f_konkret_a_minus1 = f1.mit_wert(a=-1)  # f_-1(x) = -x^2 + x

print(f"f_a=2(x) = {f_konkret_a2.term()}")
print(f"f_a=-1(x) = {f_konkret_a_minus1.term()}")

# Greife auf alle Methoden der konkreten Funktionen zu
print(f"Nullstellen von f_2(x): {f_konkret_a2.nullstellen()}")
print(f"Wert von f_2(3): {f_konkret_a2.wert(3)}")

# =============================================================================
# GLEICHUNGSLOESER - Die neuen Funktionen
# =============================================================================

print("\n=== GLEICHUNGSLOESER ===")

# 1. Löse f_c(x) = ziel_wert für konkrete Parameter
print("1. löse_für_x() - Konkrete Parameter:")
for a_wert in [1, 2, -1]:
    loesungen = f1.löse_für_x(a_wert, 5)  # f_a(x) = 5
    print(f"   f_{a_wert}(x) = 5 → x = {loesungen}")

# 2. Löse f_a(x_wert) = ziel_wert für Parameter a
print("\n2. löse_für_parameter() - Parameter gesucht:")
loesungen_a = f1.löse_für_parameter("a/2", 1)  # f_a(a/2) = 1
print(f"   f_a(a/2) = 1 → a = {loesungen_a}")

loesungen_b = f1.löse_für_parameter(3, 10)  # f_a(3) = 10
print(f"   f_a(3) = 10 → a = {loesungen_b}")

# =============================================================================
# VISUALISIERUNG
# =============================================================================

print("\n=== VISUALISIERUNG ===")

from schul_analysis import Graph_parametrisiert

# Erzeuge multiple Graphen für verschiedene Parameterwerte
fig = Graph_parametrisiert(f1, a=[-2, -1, 0, 1, 2])
print("   Graph für f_a(x) mit a = [-2, -1, 0, 1, 2] erstellt")
print(f"   Titel: {fig.layout.title.text}")

# =============================================================================
# WAS ALLES IMPORTIEREN?
# =============================================================================

print("\n=== IMPORT-ÜBERSICHT ===")

print("Für vordefinierte Objekte (empfohlen):")
print("   from schul_analysis import x, t, a, k, ParametrischeFunktion")
print("")
print("Für volle Flexibilität:")
print("   from schul_analysis import Variable, Parameter, ParametrischeFunktion")
print("")
print("Für Visualisierung:")
print("   from schul_analysis import Graph_parametrisiert")
print("")
print("Alles auf einmal:")
print("   from schul_analysis import *  # nicht empfohlen, aber möglich")

print("\n=== ZUSAMMENFASSUNG ===")

print("""
1. KLEINSTE IMPORT-VARIANTE (für die meisten Fälle ausreichend):
   from schul_analysis import x, a, ParametrischeFunktion

2. DEFINITION einer parametrischen Funktion:
   f = ParametrischeFunktion([konstante, linear_koeff, quadratisch_koeff], [x])
   Beispiel: f_a(x) = a*x^2 + x → ParametrischeFunktion([0, 1, a], [x])

3. KONKRETE FUNKTIONEN:
   f_konkret = f.mit_wert(a=2)  # f_2(x) = 2x^2 + x

4. GLEICHUNGEN LÖSEN:
   f.löse_für_x(2, 5)      # f_2(x) = 5
   f.löse_für_parameter(3, 10)  # f_a(3) = 10

5. VISUALISIEREN:
   from schul_analysis import Graph_parametrisiert
   Graph_parametrisiert(f, a=[-2, -1, 0, 1, 2])
""")

# Demonstration der korrekten Koeffizienten-Reihenfolge
print("\n=== KOEFFIZIENTEN-REIHENFOLGE ERKLÄRT ===")

print("Die Koeffizienten-Liste [c0, c1, c2, ...] entspricht:")
print("   c0 + c1*x + c2*x^2 + c3*x^3 + ...")
print("")
print("Beispiele:")
print("   [0, 1, a]    → 0 + 1*x + a*x^2     → ax² + x")
print("   [1, b, 0]    → 1 + b*x + 0*x^2     → bx + 1")
print("   [0, 0, 1, k] → 0 + 0*x + 1*x^2 + k*x^3 → x^2 + kx^3")
print("")
print("Wichtig: Der Index entspricht der Potenz von x!")
