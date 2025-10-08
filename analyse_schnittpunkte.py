#!/usr/bin/env python3
"""
Analyse der Schnittpunkt-Berechnung für mehrere Funktionen
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from sympy import solve, Eq, Symbol


def test_schnittpunkte():
    """Teste die Berechnung von Schnittpunkten"""
    print("=== Analyse: Schnittpunkte zwischen Funktionen ===")

    # Beispiel 1: f=2x+6 und g=(x-10)^2
    f = GanzrationaleFunktion("2x+6")
    g = GanzrationaleFunktion("(x-10)^2")

    print(f"Funktionen:")
    print(f"  f(x) = {f.term()}")
    print(f"  g(x) = {g.term()}")

    # Berechne Schnittpunkte symbolisch
    x = Symbol("x")
    f_expr = f.term_sympy
    g_expr = g.term_sympy

    print(f"\nSymbolische Berechnung:")
    print(f"  f(x) = {f_expr}")
    print(f"  g(x) = {g_expr}")

    # Löse die Gleichung f(x) = g(x)
    gleichung = Eq(f_expr, g_expr)
    print(f"\nGleichung: {gleichung}")

    schnittpunkte = solve(gleichung, x)
    print(f"Schnittpunkte (x-Werte): {schnittpunkte}")

    # Berechne y-Werte und validiere
    gueltige_schnittpunkte = []
    for x_val in schnittpunkte:
        try:
            # Prüfe ob x-Wert reell ist
            if x_val.is_real:
                x_float = float(x_val)
                y_float = float(f_expr.subs(x, x_val))

                # Prüfe ob y-Wert endlich ist
                if not (abs(y_float) == float("inf")):
                    gueltige_schnittpunkte.append((x_float, y_float))
                    print(f"  Schnittpunkt bei ({x_float:.3f}, {y_float:.3f})")
                else:
                    print(f"  Ungültiger Schnittpunkt bei x={x_float:.3f} (y=∞)")
            else:
                print(f"  Komplexer Schnittpunkt: x={x_val}")
        except Exception as e:
            print(f"  Fehler bei x={x_val}: {e}")

    print(f"\nGefundene gültige Schnittpunkte: {len(gueltige_schnittpunkte)}")

    # Beispiel 2: Zwei Parabeln
    print(f"\n{'=' * 50}")
    print("Beispiel 2: Zwei Parabeln")

    f2 = GanzrationaleFunktion("x^2")
    g2 = GanzrationaleFunktion("(x-2)^2")

    print(f"f(x) = {f2.term()}")
    print(f"g(x) = {g2.term()}")

    f2_expr = f2.term_sympy
    g2_expr = g2.term_sympy

    gleichung2 = Eq(f2_expr, g2_expr)
    schnittpunkte2 = solve(gleichung2, x)

    print(f"Gleichung: {gleichung2}")
    print(f"Schnittpunkte: {schnittpunkte2}")

    for x_val in schnittpunkte2:
        try:
            if x_val.is_real:
                x_float = float(x_val)
                y_float = float(f2_expr.subs(x, x_float))
                print(f"  Schnittpunkt bei ({x_float:.3f}, {y_float:.3f})")
        except Exception as e:
            print(f"  Fehler bei x={x_val}: {e}")


if __name__ == "__main__":
    test_schnittpunkte()
