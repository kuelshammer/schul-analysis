#!/usr/bin/env python3
"""
Debug-Skript für Tangente-Funktion
"""

# Code Import, wie in Marimo
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from schul_mathematik.analysis import *

# Testfunktion erstellen
f = Funktion("x**2")
print(f"f(x) = {f.term()}")

# Tangente an x = 1 berechnen
try:
    t = Tangente(f, 1)
    print(f"Tangente an x=1: {t.term()}")
    print(f"Typ: {type(t)}")

    # Testen, ob wir die Tangente zeichnen können
    print("\nZeichne Funktion und Tangente:")
    Zeichne(f, t, x_bereich=(-2, 4))

except Exception as e:
    print(f"Fehler: {e}")
    import traceback

    traceback.print_exc()
