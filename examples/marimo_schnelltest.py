"""
Marimo Schnelltest für Schul-Analysis Framework

Einfaches Notebook mit den grundlegendsten Features.
Kopiere diesen Code einfach in dein leeres Marimo-Notebook.
"""

import marimo as mo

# =============================================================================
# 🎯 GRUNDLEGENDE IMPORTS
# =============================================================================
from schul_analysis import Ableitung, Funktion, Nullstellen

# =============================================================================
# 🔧 ZWEI FUNKTIONEN DEFINIEREN
# =============================================================================

# Erste Funktion: Quadratisch
f = Funktion("x^2")

# Zweite Funktion: Linear
g = Funktion("3x + 5")

# =============================================================================
# 📋 KURZE DEMONSTRATION
# =============================================================================

# Ableitungen berechnen
f_strich = Ableitung(f)
g_strich = Ableitung(g)

# Nullstellen berechnen
f_Nullstellen = Nullstellen(f)
g_Nullstellen = Nullstellen(g)

# =============================================================================
# 📊 AUSGABE ZUR ÜBERPRÜFUNG
# =============================================================================

mo.md("## 🎯 Schul-Analysis Framework - Schnelltest")
mo.md(f"**Funktion f:** f(x) = {f.term()}")
mo.md(f"**Ableitung f':** f'(x) = {f_strich.term()}")
mo.md(f"**Nullstellen f:** x = {f_Nullstellen}")

mo.md("---")

mo.md(f"**Funktion g:** g(x) = {g.term()}")
mo.md(f"**Ableitung g':** g'(x) = {g_strich.term()}")
mo.md(f"**Nullstellen g:** x = {g_Nullstellen}")

# =============================================================================
# 🧪 EINFACHE TESTS
# =============================================================================

mo.md("---")
mo.md("## 🧪 Teste die Funktionen:")

# Teste einige Werte
test_werte = [-2, -1, 0, 1, 2]

for x in test_werte:
    f_wert = f(x)
    g_wert = g(x)
    mo.md(f"f({x}) = {f_wert}, g({x}) = {g_wert}")

mo.md("---")
mo.md("✅ **Fertig zum Experimentieren!**")
mo.md(
    "Du kannst jetzt mit `f` und `g` arbeiten sowie deren Ableitungen `f_strich` und `g_strich`"
)

# =============================================================================
# 🔍 VERFÜGBARE OBJEKTE
# =============================================================================

mo.md("---")
mo.md("## 🔍 Verfügbare Objekte:")
mo.md("- `f` - Quadratische Funktion (x²)")
mo.md("- `g` - Lineare Funktion (3x + 5)")
mo.md("- `f_strich` - Ableitung von f (2x)")
mo.md("- `g_strich` - Ableitung von g (3)")
mo.md("- `f_nullstellen` - Nullstellen von f ([0])")
mo.md("- `g_nullstellen` - Nullstellen von g ([-5/3])")
