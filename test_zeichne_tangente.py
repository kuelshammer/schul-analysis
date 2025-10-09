#!/usr/bin/env python3
"""
Test Zeichne() mit Tangente und Taylorpolynom
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
    print(f"✅ Tangente an x=1: {t.term()}")

    # Taylorpolynom Grad 3 an x=0 berechnen
    tp = Taylorpolynom(f, 3, 0)
    print(f"✅ Taylorpolynom Grad 3 an x=0: {tp.term()}")

    # Zeichne Funktion und Tangente
    print("\n✅ Zeichne Funktion und Tangente:")
    fig = Graph(f, t, x_min=-3, x_max=3, titel="Funktion f(x)=x² und Tangente bei x=1")

    # Zeichne Funktion und Taylorpolynom
    print("\n✅ Zeichne Funktion und Taylorpolynom:")
    fig2 = Graph(
        f, tp, x_min=-3, x_max=3, titel="Funktion f(x)=x² und Taylorpolynom Grad 3"
    )

    print(
        "\n✅ Alles erfolgreich! Die Funktionen können mit Zeichne() verwendet werden."
    )

except Exception as e:
    print(f"❌ Fehler: {e}")
    import traceback

    traceback.print_exc()
