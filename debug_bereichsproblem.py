#!/usr/bin/env python3
"""
Debug Script für das Problem mit f=2x+6 und g=(x-10)^2
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import (
    Graph,
    _berechne_kombinierten_intelligenten_bereich,
)


def debug_problem():
    """Debuggt das Problem mit den extremen Bereichen"""
    print("=== Debug: f=2x+6 und g=(x-10)^2 ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3
    g = GanzrationaleFunktion("(x-10)^2")  # Nullstelle bei x=10

    print(f"Funktion f: {f.term()}")
    print(f"Funktion g: {g.term()}")

    # Debug: Was findet die Punktesammlung?
    from schul_analysis.visualisierung import _sammle_interessante_punkte

    punkte_f = _sammle_interessante_punkte(f)
    punkte_g = _sammle_interessante_punkte(g)

    print(f"\nPunkte f: x_werte = {punkte_f['x_werte']}")
    print(f"Punkte g: x_werte = {punkte_g['x_werte']}")

    # Debug: Was berechnet die kombinierte Funktion?
    x_min, x_max, x_step = _berechne_kombinierten_intelligenten_bereich([f, g])
    print(f"\nKombinierter Bereich: [{x_min}, {x_max}], Schrittweite: {x_step}")

    # Debug: Was zeigt der eigentliche Graph?
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range
    print(
        f"Tatsächlicher Graph-Bereich: x=[{x_range[0]:.3f}, {x_range[1]:.3f}], y=[{y_range[0]:.3f}, {y_range[1]:.3f}]"
    )

    print("\nErwartet: ca. -3 bis 10 (mit Puffer)")
    print("Problem: Der Bereich ist viel zu groß!")


if __name__ == "__main__":
    debug_problem()
