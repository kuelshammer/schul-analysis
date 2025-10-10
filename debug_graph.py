#!/usr/bin/env python3
"""
Debug script to test the new Graph function
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import (
    Graph,
    _filtere_sichtbare_punkte,
    _sammle_interessante_punkte,
)

# Test mit einer einfachen Parabel
f = GanzrationaleFunktion("x^2 - 4")
print(f"Funktion: {f.term()}")

# Sammle interessante Punkte
punkte = _sammle_interessante_punkte(f)
print(f"Gefundene Punkte: {punkte}")

# Teste mit manueller Y-Begrenzung
print("\nTest mit y_max=0 (sollte Extremstelle bei (0|-4) abschneiden):")
fig = Graph(f, y_max=0)

# Prüfe welche Punkte sichtbar wären
sichtbare, abgeschnittene = _filtere_sichtbare_punkte(
    punkte, x_min=-5, x_max=5, y_min=-10, y_max=0
)
print(f"Sichtbare Punkte: {sichtbare}")
print(f"Abgeschnittene Punkte: {abgeschnittene}")

print("\nY-Bereich der Figur:", fig.layout.yaxis.range)
