#!/usr/bin/env python3
"""
Test der verbesserten Y-Berechnung
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph, _berechne_y_bereich_mehrfach


def test_verbesserte_y_berechnung():
    """Testet die verbesserte Y-Berechnung"""
    print("=== Test verbesserte Y-Berechnung ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3
    g = GanzrationaleFunktion("(x-10)^2")  # Nullstelle bei x=10

    # X-Bereich
    x_min, x_max = -4, 11

    # Debug: Was sind die wichtigen Punkte?
    print("Wichtige Punkte:")
    if hasattr(f, "extremstellen"):
        print(f"f.extremstellen: {f.extremstellen}")
    if hasattr(g, "extremstellen"):
        print(f"g.extremstellen: {g.extremstellen}")

    # Teste die neue Y-Berechnung
    y_min, y_max = _berechne_y_bereich_mehrfach([f, g], x_min, x_max)

    print(f"\nX-Bereich: [{x_min}, {x_max}]")
    print(f"Verbesserter Y-Bereich: [{y_min:.3f}, {y_max:.3f}]")
    print(f"Y-Spanne: {y_max - y_min:.3f}")

    # Erstelle Graph und vergleiche
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range
    print("\nTatsächlicher Graph-Bereich:")
    print(f"x=[{x_range[0]:.3f}, {x_range[1]:.3f}]")
    print(f"y=[{y_range[0]:.3f}, {y_range[1]:.3f}]")
    print(f"Y-Spanne: {y_range[1] - y_range[0]:.3f}")

    # Ist es besser geworden?
    if y_range[1] - y_range[0] < 200:
        print("\n✅ Verbesserung: Y-Spanne < 200")
    else:
        print("\n❌ Immer noch zu große Y-Spanne")


if __name__ == "__main__":
    test_verbesserte_y_berechnung()
