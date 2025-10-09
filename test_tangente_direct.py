#!/usr/bin/env python3
"""
Direkter Test der Tangente-Funktion
"""

# Code Import, wie in Marimo
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from schul_mathematik.analysis.taylor import tangente
from schul_mathematik.analysis import Funktion

# Testfunktion erstellen
f = Funktion("x**2")
print(f"f(x) = {f.term()}")

# Tangente an x = 1 berechnen
try:
    t = tangente(f, 1)
    print(f"Tangente an x=1: {t.term()}")
    print(f"Typ: {type(t)}")
    print(f"Wert bei x=0: {t(0)}")
    print(f"Wert bei x=1: {t(1)}")
    print(f"Wert bei x=2: {t(2)}")

except Exception as e:
    print(f"Fehler: {e}")
    import traceback

    traceback.print_exc()
