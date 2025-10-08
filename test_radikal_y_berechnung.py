#!/usr/bin/env python3
"""
Testet radikal verbesserte Y-Berechnung nur mit wichtigen Punkten
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph


def test_radikal_verbessert():
    """Testet radikal verbesserte Logik"""
    print("=== Test: Radikal verbesserte Y-Berechnung ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3, y=0
    g = GanzrationaleFunktion("(x-10)^2")  # Minimum bei x=10, y=0

    print(f"Wichtige Punkte für f:")
    print(f"  Nullstelle: x=-3, y={f.wert(-3)}")
    if hasattr(f, "extremstellen"):
        print(f"  Extremstellen: {f.extremstellen}")

    print(f"Wichtige Punkte für g:")
    print(f"  Minimum: x=10, y={g.wert(10)}")
    if hasattr(g, "extremstellen"):
        print(f"  Extremstellen: {g.extremstellen}")

    # Manuelle Berechnung: nur wichtige Punkte
    wichtige_y_werte = []

    # Füge wichtige Punkte von f hinzu
    wichtige_y_werte.append(f.wert(-3))  # Nullstelle

    # Füge wichtige Punkte von g hinzu
    if hasattr(g, "extremstellen"):
        for extremstelle in g.extremstellen:
            if isinstance(extremstelle, tuple) and len(extremstelle) >= 2:
                y_val = extremstelle[1]
                if isinstance(y_val, (int, float)):
                    wichtige_y_werte.append(y_val)

    print(f"\nGesammelte wichtige y-Werte: {wichtige_y_werte}")

    if wichtige_y_werte:
        y_min = min(wichtige_y_werte)
        y_max = max(wichtige_y_werte)

        print(f"Min wichtiger y-Wert: {y_min}")
        print(f"Max wichtiger y-Wert: {y_max}")

        # Intelligenter Puffer basierend auf den wichtigen Punkten
        spanne = y_max - y_min
        if spanne == 0:  # Alle Punkte haben gleichen y-Wert
            # Füge symmetrischen Puffer hinzu
            puffer = 5.0  # Standardpuffer
            y_min_final = y_min - puffer
            y_max_final = y_max + puffer
        else:
            # Puffer basierend auf der Spanne der wichtigen Punkte
            puffer = max(spanne * 0.5, 2.0)  # 50% Puffer, min. 2 Einheiten
            y_min_final = y_min - puffer
            y_max_final = y_max + puffer

        print(f"Intelligenter Puffer: {puffer}")
        print(f"Finaler Y-Bereich: [{y_min_final:.3f}, {y_max_final:.3f}]")
        print(f"Y-Spanne: {y_max_final - y_min_final:.3f}")

        # Teste mit der aktuellen Implementierung
        fig = Graph(f, g)
        x_range = fig.layout.xaxis.range
        y_range = fig.layout.yaxis.range

        print(f"\nAktuelle Implementierung:")
        print(f"y=[{y_range[0]:.3f}, {y_range[1]:.3f}]")
        print(f"Y-Spanne: {y_range[1] - y_range[0]:.3f}")

        # Vergleich
        if (y_max_final - y_min_final) < (y_range[1] - y_range[0]):
            print(
                f"\n✅ Die neue Logik wäre besser: {(y_max_final - y_min_final):.3f} vs {(y_range[1] - y_range[0]):.3f}"
            )
        else:
            print(f"\n❌ Aktuelle Implementierung ist besser")


if __name__ == "__main__":
    test_radikal_verbessert()
