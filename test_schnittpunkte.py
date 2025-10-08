#!/usr/bin/env python3
"""
Teste die neue Schnittpunkt-Funktionalität
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph


def test_schnittpunkt_funktionalitaet():
    """Testet die Schnittpunkt-Darstellung in Graph(f, g)"""
    print("=== Test: Schnittpunkt-Funktionalität ===")

    # Beispiel 1: f=2x+6 und g=(x-10)^2
    print("Beispiel 1: Lineare und quadratische Funktion")
    f = GanzrationaleFunktion("2x+6")
    g = GanzrationaleFunktion("(x-10)^2")

    print(f"f(x) = {f.term()}")
    print(f"g(x) = {g.term()}")

    # Erstelle Graph - sollte Schnittpunkte finden und anzeigen
    fig = Graph(f, g, titel="Schnittpunkte: f(x)=2x+6 und g(x)=(x-10)²")

    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range

    print(f"X-Bereich: [{x_range[0]:.3f}, {x_range[1]:.3f}]")
    print(f"Y-Bereich: [{y_range[0]:.3f}, {y_range[1]:.3f}]")

    # Prüfe Anzahl der Traces (sollten 3 sein: 2 Funktionen + 1 Schnittpunkte)
    print(f"Anzahl Traces: {len(fig.data)}")
    for i, trace in enumerate(fig.data):
        print(f"  {i + 1}. {trace.name}: {len(trace.x)} Punkte")

    print(f"\n{'=' * 50}")

    # Beispiel 2: Zwei Parabeln
    print("Beispiel 2: Zwei Parabeln")
    f2 = GanzrationaleFunktion("x^2")
    g2 = GanzrationaleFunktion("(x-2)^2 + 1")  # Verschobene Parabel

    print(f"f(x) = {f2.term()}")
    print(f"g(x) = {g2.term()}")

    fig2 = Graph(f2, g2, titel="Schnittpunkte: Zwei Parabeln")

    x_range2 = fig2.layout.xaxis.range
    y_range2 = fig2.layout.yaxis.range

    print(f"X-Bereich: [{x_range2[0]:.3f}, {x_range2[1]:.3f}]")
    print(f"Y-Bereich: [{y_range2[0]:.3f}, {y_range2[1]:.3f}]")

    print(f"Anzahl Traces: {len(fig2.data)}")
    for i, trace in enumerate(fig2.data):
        print(f"  {i + 1}. {trace.name}: {len(trace.x)} Punkte")

    print(f"\n{'=' * 50}")

    # Beispiel 3: Drei Funktionen
    print("Beispiel 3: Drei Funktionen")
    f3 = GanzrationaleFunktion("x^2")
    g3 = GanzrationaleFunktion("2*x")
    h3 = GanzrationaleFunktion("4")

    print(f"f(x) = {f3.term()}")
    print(f"g(x) = {g3.term()}")
    print(f"h(x) = {h3.term()}")

    fig3 = Graph(f3, g3, h3, titel="Schnittpunkte: Drei Funktionen")

    print(f"Anzahl Traces: {len(fig3.data)}")
    for i, trace in enumerate(fig3.data):
        print(f"  {i + 1}. {trace.name}: {len(trace.x)} Punkte")


if __name__ == "__main__":
    test_schnittpunkt_funktionalitaet()
