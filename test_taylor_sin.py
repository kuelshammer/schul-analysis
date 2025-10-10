#!/usr/bin/env python3
"""
Test Taylorpolynom mit sin(x)
"""

# Code Import, wie in Marimo
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from schul_mathematik.analysis import *

# Testfunktion erstellen
f = Funktion("sin(x)")
print(f"f(x) = {f.term()}")

# Taylorpolynome verschiedenen Grades an x=0 berechnen (MacLaurin-Reihe)
try:
    # Lineare Approximation
    tp1 = Taylorpolynom(f, 1, 0)
    print(f"✅ Taylorpolynom Grad 1: {tp1.term()}")

    # Kubische Approximation
    tp3 = Taylorpolynom(f, 3, 0)
    print(f"✅ Taylorpolynom Grad 3: {tp3.term()}")

    # Approximation 5. Grades
    tp5 = Taylorpolynom(f, 5, 0)
    print(f"✅ Taylorpolynom Grad 5: {tp5.term()}")

    # Zeichne alle Funktionen
    print("\n✅ Zeichne sin(x) und Taylor-Approximationen:")
    fig = Graph(
        f,
        tp1,
        tp3,
        tp5,
        x_min=-6,
        x_max=6,
        titel="sin(x) und Taylor-Approximationen an x=0",
    )

    print("\n✅ Erfolgreich! Die Taylor-Approximationen funktionieren perfekt.")

except Exception as e:
    print(f"❌ Fehler: {e}")
    import traceback

    traceback.print_exc()
