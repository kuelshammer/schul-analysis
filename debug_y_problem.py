#!/usr/bin/env python3
"""
Detailliertes Debug des Y-Bereichsproblems
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph, _berechne_y_bereich_mehrfach


def debug_y_bereich():
    """Debuggt warum der Y-Bereich so extrem ist"""
    print("=== Debug Y-Bereichsproblem ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3
    g = GanzrationaleFunktion("(x-10)^2")  # Nullstelle bei x=10

    # X-Bereich sollte [-4, 11] sein
    x_min, x_max = -4, 11

    # Was berechnet die Y-Bereichsfunktion?
    y_min, y_max = _berechne_y_bereich_mehrfach([f, g], x_min, x_max)

    print(f"X-Bereich: [{x_min}, {x_max}]")
    print(f"Berechneter Y-Bereich: [{y_min:.3f}, {y_max:.3f}]")

    # Teste manuelle Y-Werte an den Grenzen
    print(f"\nFunktionswerte an den Grenzen:")
    print(f"f({x_min}) = {f.wert(x_min)}")
    print(f"f({x_max}) = {f.wert(x_max)}")
    print(f"g({x_min}) = {g.wert(x_min)}")
    print(f"g({x_max}) = {g.wert(x_max)}")

    # Teste Werte in der Mitte
    mitte = (x_min + x_max) / 2
    print(f"f({mitte:.1f}) = {f.wert(mitte)}")
    print(f"g({mitte:.1f}) = {g.wert(mitte)}")

    # Erstelle Graph und vergleiche
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range
    print(f"\nTatsächlicher Graph-Bereich:")
    print(f"x=[{x_range[0]:.3f}, {x_range[1]:.3f}]")
    print(f"y=[{y_range[0]:.3f}, {y_range[1]:.3f}]")


if __name__ == "__main__":
    debug_y_bereich()
