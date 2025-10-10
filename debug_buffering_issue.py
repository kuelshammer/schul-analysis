#!/usr/bin/env python3
"""
Debug the buffering issue with (x+3)(x+1)(x-10)
"""

from src.schul_analysis.ganzrationale import GanzrationaleFunktion
from src.schul_analysis.visualisierung import Graph


def debug_buffering():
    """Debug the specific buffering issue"""
    print("=== Debug Buffering Issue ===")

    # Test the specific function
    f = GanzrationaleFunktion("(x+3)(x+1)(x-10)")
    print(f"Function: {f.term()}")
    print(f"Nullstellen: {f.nullstellen}")

    # Create graph and check the range
    fig = Graph(f)
    x_range = fig.layout.xaxis.range
    print(f"X-range: {x_range}")

    # Check buffering for each nullstelle
    nullstellen = f.nullstellen
    if nullstellen:
        print("\nBuffer analysis:")
        for i, nullstelle in enumerate(nullstellen):
            print(f"Nullstelle {i + 1}: x = {nullstelle}")
            left_distance = abs(nullstelle - x_range[0])
            right_distance = abs(x_range[1] - nullstelle)
            print(f"  Distance to left edge: {left_distance:.3f}")
            print(f"  Distance to right edge: {right_distance:.3f}")

            # Check if it's too close to edge
            if min(left_distance, right_distance) < 1.0:
                print("  ❌ TOO CLOSE to edge!")
            else:
                print("  ✅ Good buffering")

    # Check what the actual important points are
    print("\n=== Checking important points ===")
    from src.schul_analysis.visualisierung import _sammle_interessante_punkte

    wichtige_punkte = _sammle_interessante_punkte(f)
    print(f"Wichtige Punkte: {wichtige_punkte}")

    # Check the optimization logic directly
    print("\n=== Checking optimization logic ===")
    # Get initial range
    from src.schul_analysis.visualisierung import _berechne_intervalle, _optimiere_achse

    x_intervall = _berechne_intervalle(f, x_bereich=None)
    print(f"Initial interval: {x_intervall}")

    # Apply optimization
    wichtiger_punkte_x = wichtige_punkte.get("x_werte", [])
    print(f"Wichtige x-Werte: {wichtiger_punkte_x}")

    optimiertes_intervall = _optimiere_achse(
        x_intervall[0], x_intervall[1], wichtiger_punkte_x
    )
    print(f"Optimized interval: {optimiertes_intervall}")


if __name__ == "__main__":
    debug_buffering()
