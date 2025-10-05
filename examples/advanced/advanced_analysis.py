"""
Advanced Analysis Examples

Dieses Beispiel zeigt fortgeschrittene Analysetechniken des Schul-Analysis Frameworks.
"""

import numpy as np

from schul_analysis import (
    Ableitung,
    AsymptotischesVerhalten,
    Extremstellen,
    Funktion,
    Grenzwert,
    Integral,
    Nullstellen,
    Polstellen,
    Wendepunkte,
)

# 1. Komplexe ganzrationale Funktion
print("=== 1. Komplexe ganzrationale Funktion ===")
f = Funktion("x^3 - 6x^2 + 11x - 6")
print(f"Funktion: f(x) = {f.term()}")

# Nullstellen analysieren
nullstellen = Nullstellen(f)
print(f"Nullstellen: {nullstellen}")

# Ableitungen und Extremstellen
f_strich = Ableitung(f)
f_doppelt = Ableitung(f, ordnung=2)

print(f"f'(x) = {f_strich.term()}")
print(f"f''(x) = {f_doppelt.term()}")

extremstellen = Extremstellen(f)
print(f"Extremstellen: {extremstellen}")

wendepunkte = Wendepunkte(f)
print(f"Wendepunkte: {wendepunkte}")

# 2. Gebrochen-rationale Funktion mit Asymptoten
print("\n=== 2. Gebrochen-rationale Funktion ===")
g = Funktion("(x^2 - 4)/(x^2 - 1)")
print(f"Funktion: g(x) = {g.term()}")

# Polstellen finden
polstellen = Polstellen(g)
print(f"Polstellen: {polstellen}")

# Asymptotisches Verhalten
try:
    asympt_verhalten = AsymptotischesVerhalten(g)
    print(f"Asymptotisches Verhalten: {asympt_verhalten}")
except Exception as e:
    print(f"Asymptotisches Verhalten konnte nicht berechnet werden: {e}")

# Grenzwerte analysieren
print("\nGrenzwerte:")
grenzwerte = [
    ("x->∞", Grenzwert(g, "oo")),
    ("x->-∞", Grenzwert(g, "-oo")),
    ("x->1+", Grenzwert(g, 1, seite="+")),
    ("x->1-", Grenzwert(g, 1, seite="-")),
]

for beschreibung, wert in grenzwerte:
    print(f"  {beschreibung}: {wert}")

# 3. Integralberechnung
print("\n=== 3. Integralberechnung ===")
h = Funktion("x^2 + 2x + 1")
print(f"Funktion: h(x) = {h.term()}")

# Unbestimmtes Integral
integral_h = Integral(h)
print(f"∫h(x)dx = {integral_h.term()}")

# Bestimmtes Integral (numerisch)
try:
    x_vals = np.linspace(0, 2, 100)
    y_vals = [h.wert(x) for x in x_vals]
    # Trapezregel für numerische Integration
    integral_numeric = np.trapz(y_vals, x_vals)
    print(f"∫₀² h(x)dx ≈ {integral_numeric:.6f}")
except Exception as e:
    print(f"Numerische Integration fehlgeschlagen: {e}")

# 4. Kurvendiskussion
print("\n=== 4. Vollständige Kurvendiskussion ===")


def kurvendiskussion(funktion, name="f"):
    """Führt eine vollständige Kurvendiskussion durch"""
    print(f"\nKurvendiskussion für {name}(x) = {funktion.term()}")

    # Definitionsbereich
    try:
        polstellen = Polstellen(funktion)
        if polstellen:
            print(f"Definitionsbereich: ℝ \\ {polstellen}")
        else:
            print("Definitionsbereich: ℝ")
    except:
        print("Definitionsbereich: ℝ")

    # Nullstellen
    try:
        nullst = Nullstellen(funktion)
        print(f"Nullstellen: {nullst}")
    except Exception as e:
        print(f"Nullstellen: Fehler - {e}")

    # Extremstellen
    try:
        ext = Extremstellen(funktion)
        print(f"Extremstellen: {ext}")
    except Exception as e:
        print(f"Extremstellen: Fehler - {e}")

    # Wendepunkte
    try:
        wp = Wendepunkte(funktion)
        print(f"Wendepunkte: {wp}")
    except Exception as e:
        print(f"Wendepunkte: Fehler - {e}")

    # Asymptoten
    try:
        asympt = AsymptotischesVerhalten(funktion)
        if asympt:
            print(f"Asymptoten: {asympt}")
    except:
        pass


# Teste mit verschiedenen Funktionen
test_funktionen = [
    ("x^3 - 3x^2 + 2", "f"),
    ("1/(x^2 + 1)", "g"),
    ("(x^2 - 4)/(x - 2)", "h"),
]

for func_str, name in test_funktionen:
    try:
        func = Funktion(func_str)
        kurvendiskussion(func, name)
        print("-" * 50)
    except Exception as e:
        print(f"Fehler bei {name}(x) = {func_str}: {e}")

print("\n=== 5. Zusammenfassung ===")
print("Fortgeschrittene Techniken:")
print("- Mehrfache Ableitungen")
print("- Asymptotisches Verhalten")
print("- Integralberechnung")
print("- Vollständige Kurvendiskussion")
print("- Grenzwertanalyse")
