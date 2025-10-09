#!/usr/bin/env python3
"""
Test Import von API-Funktionen
"""

# Code Import, wie in Marimo
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Importe testen
try:
    from schul_mathematik.analysis.api import Tangente, Taylorpolynom

    print("✅ Tangente und Taylorpolynom aus API importiert")
except ImportError as e:
    print(f"❌ Fehler beim Import aus API: {e}")

try:
    from schul_mathematik.analysis import Tangente, Taylorpolynom

    print("✅ Tangente und Taylorpolynom aus Modul importiert")
except ImportError as e:
    print(f"❌ Fehler beim Import aus Modul: {e}")

# Testfunktion erstellen
from schul_mathematik.analysis import Funktion

f = Funktion("x**2")
print(f"f(x) = {f.term()}")

# Tangente testen
try:
    t = Tangente(f, 1)
    print(f"✅ Tangente an x=1: {t.term()}")
except Exception as e:
    print(f"❌ Fehler bei Tangente: {e}")

# Taylorpolynom testen
try:
    tp = Taylorpolynom(f, 2, 1)
    print(f"✅ Taylorpolynom Grad 2 an x=1: {tp.term()}")
except Exception as e:
    print(f"❌ Fehler bei Taylorpolynom: {e}")
