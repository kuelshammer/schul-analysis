#!/usr/bin/env python3
"""
Finale Lösung für das Y-Bereichsproblem
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph, _berechne_y_bereich_mehrfach


def test_finale_loesung():
    """Testet die finale Lösung"""
    print("=== Test: Finale Lösung für Y-Bereich ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3, y=0
    g = GanzrationaleFunktion("(x-10)^2")  # Minimum bei x=10, y=0

    # X-Bereich
    x_min, x_max = -4, 11

    # Manuelle Logik für diesen speziellen Fall
    print("Manuelle Berechnung:")
    print("Wichtige y-Werte:")

    wichtige_y_werte = []

    # Sammle wichtige Punkte von f
    wichtige_y_werte.append(f.wert(-3))  # Nullstelle bei x=-3

    # Sammle wichtige Punkte von g
    if hasattr(g, "extremstellen"):
        for extremstelle in g.extremstellen:
            if isinstance(extremstelle, tuple) and len(extremstelle) >= 2:
                y_val = extremstelle[1]
                if isinstance(y_val, (int, float)):
                    wichtige_y_werte.append(y_val)

    print(f"  Gesammelte y-Werte: {wichtige_y_werte}")

    if wichtige_y_werte:
        y_min_wichtig = min(wichtige_y_werte)
        y_max_wichtig = max(wichtige_y_werte)
        print(f"  Y-Min (wichtig): {y_min_wichtig}")
        print(f"  Y-Max (wichtig): {y_max_wichtig}")

        # Wenn alle wichtigen y-Werte 0 sind, nutze eine feste Spanne
        if y_min_wichtig == y_max_wichtig == 0:
            print("  Alle wichtigen y-Werte sind 0 - verwende feste Spanne")
            y_min_final = -10  # Feste untere Grenze
            y_max_final = 20  # Feste obere Grenze (zeigt den Anstieg)
        else:
            # Normale Logik
            spanne = y_max_wichtig - y_min_wichtig
            puffer = max(spanne * 0.5, 5.0)
            y_min_final = y_min_wichtig - puffer
            y_max_final = y_max_wichtig + puffer

        print(f"  Vorgeschlagener Y-Bereich: [{y_min_final}, {y_max_final}]")
        print(f"  Y-Spanne: {y_max_final - y_min_final}")

    # Vergleiche mit aktueller Implementierung
    y_min_current, y_max_current = _berechne_y_bereich_mehrfach([f, g], x_min, x_max)
    print(f"\nAktuelle Implementierung: [{y_min_current:.3f}, {y_max_current:.3f}]")
    print(f"Aktuelle Y-Spanne: {y_max_current - y_min_current:.3f}")

    # Teste Graph
    fig = Graph(f, g)
    y_range = fig.layout.yaxis.range
    print(f"Graph Y-Bereich: [{y_range[0]:.3f}, {y_range[1]:.3f}]")


if __name__ == "__main__":
    test_finale_loesung()
