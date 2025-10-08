#!/usr/bin/env python3
"""
Teste die finale Darstellung nach dem Aspect Ratio Fix
"""

from schul_analysis.ganzrationale import GanzrationaleFunktion
from schul_analysis.visualisierung import Graph


def test_finale_darstellung():
    """Testet ob die Darstellung jetzt korrekt ist"""
    print("=== Test: Finale Darstellung nach Aspect Ratio Fix ===")

    f = GanzrationaleFunktion("2x+6")  # Nullstelle bei x=-3
    g = GanzrationaleFunktion("(x-10)^2")  # Minimum bei x=10

    print(f"Funktionen:")
    print(f"  f(x) = {f.term()}")
    print(f"  g(x) = {g.term()}")

    # Erstelle Graph
    fig = Graph(f, g)
    x_range = fig.layout.xaxis.range
    y_range = fig.layout.yaxis.range

    print(f"\nBereiche:")
    print(
        f"  X-Bereich: [{x_range[0]:.3f}, {x_range[1]:.3f}] (Spanne: {x_range[1] - x_range[0]:.3f})"
    )
    print(
        f"  Y-Bereich: [{y_range[0]:.3f}, {y_range[1]:.3f}] (Spanne: {y_range[1] - y_range[0]:.3f})"
    )

    # Aspect Ratio Verhältnis
    x_spanne = x_range[1] - x_range[0]
    y_spanne = y_range[1] - y_range[0]
    verhaeltnis = y_spanne / x_spanne
    print(
        f"  Y/X Verhältnis: {verhaeltnis:.3f} (sollte > 1 sein, keine 1:1 Aspect Ratio)"
    )

    # Prüfe wichtige Punkte
    print(f"\nWichtige Punkte Sichtbarkeit:")
    print(f"  f-Nullstelle (x=-3): {'✅' if x_range[0] <= -3 <= x_range[1] else '❌'}")
    print(f"  g-Minimum (x=10): {'✅' if x_range[0] <= 10 <= x_range[1] else '❌'}")

    # Prüfe, ob der Graph vernünftig aussieht
    print(f"\nBewertung:")
    x_ok = x_range[0] <= -4 and x_range[1] >= 11  # Erwarteter Bereich
    y_vernuenftig = y_spanne < 200  # Y-Spanne sollte nicht absurd sein
    aspect_ok = verhaeltnis > 1.5  # Deutlich keine 1:1 Aspect Ratio

    print(f"  X-Bereich korrekt: {'✅' if x_ok else '❌'}")
    print(f"  Y-Bereich vernünftig: {'✅' if y_vernuenftig else '❌'}")
    print(f"  Keine 1:1 Aspect Ratio: {'✅' if aspect_ok else '❌'}")

    if x_ok and y_vernuenftig and aspect_ok:
        print(f"\n🎉 ERGEBNIS: Die Darstellung ist jetzt KORREKT!")
        print(f"   - X-Bereich zeigt alle wichtigen Punkte")
        print(f"   - Y-Bereich hat angemessene Skalierung")
        print(f"   - Keine verzerrte 1:1 Aspect Ratio mehr")
    else:
        print(f"\n❌ Es gibt noch Probleme:")
        if not x_ok:
            print(f"   - X-Bereich nicht korrekt")
        if not y_vernuenftig:
            print(f"   - Y-Bereich nicht vernünftig")
        if not aspect_ok:
            print(f"   - Aspect Ratio noch problematisch")

    return fig


if __name__ == "__main__":
    test_finale_darstellung()
