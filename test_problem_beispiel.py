#!/usr/bin/env python3
"""
Teste das spezifische Problembeispiel
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph


def test_problem_beispiel():
    """Teste das Problem mit f=2x+6 und g=(x-10)^2"""
    print("=== Test: Problembeispiel f=2x+6, g=(x-10)^2 ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3
    g = GanzrationaleFunktion("(x-10)^2")  # Minimum bei x=10

    print(f"Funktion f: {f.term()}")
    print(f"Funktion g: {g.term()}")

    # Erstelle Graph
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range

    print(
        f"X-Bereich: [{x_range[0]:.3f}, {x_range[1]:.3f}] (Spanne: {x_range[1] - x_range[0]:.3f})"
    )
    print(
        f"Y-Bereich: [{y_range[0]:.3f}, {y_range[1]:.3f}] (Spanne: {y_range[1] - y_range[0]:.3f})"
    )

    # Erwarteter X-Bereich: ca. -3 bis 10 + Puffer
    print(f"Erwarteter X-Bereich: ca. -4 bis 11")
    print(f"X-Bereich akzeptabel: {x_range[0] <= -4 and x_range[1] >= 11}")

    # Prüfe wichtige Punkte
    print(
        f"Nullstelle f (x=-3): {'sichtbar' if x_range[0] <= -3 <= x_range[1] else 'nicht sichtbar'}"
    )
    print(
        f"Minimum g (x=10): {'sichtbar' if x_range[0] <= 10 <= x_range[1] else 'nicht sichtbar'}"
    )

    # Ist der Y-Bereich jetzt vernünftig?
    if y_range[1] - y_range[0] < 100:
        print("✅ Y-Bereich ist jetzt vernünftig (< 100)")
    else:
        print(f"❌ Y-Bereich ist immer noch zu groß: {y_range[1] - y_range[0]:.3f}")


if __name__ == "__main__":
    test_problem_beispiel()
