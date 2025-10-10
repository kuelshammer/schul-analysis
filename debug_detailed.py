#!/usr/bin/env python3
"""
Detailed debugging of the _optimiere_achse function
"""

import math

from src.schul_analysis.ganzrationale import GanzrationaleFunktion
from src.schul_analysis.visualisierung import Graph, _sammle_interessante_punkte


def debug_optimierung():
    """Debug the _optimiere_achse function step by step"""
    print("=== Detailed Debugging ===")

    # Test the specific function
    f = GanzrationaleFunktion("(x+3)(x+1)(x-10)")
    print(f"Function: {f.term()}")
    print(f"Nullstellen: {f.nullstellen}")

    # Get important points
    wichtige_punkte = _sammle_interessante_punkte(f)
    print(f"Important x-values: {wichtige_punkte['x_werte']}")

    # Create graph to see what happens internally
    fig = Graph(f)
    x_range = fig.layout.xaxis.range
    print(f"Final X-range: {x_range}")

    # Now let's manually trace through the optimization
    print("\n=== Manual Optimization Trace ===")

    # First, let's find the initial range
    import numpy as np

    x_sample = np.linspace(-5, 12, 1000)
    y_sample = [f.wert(x) for x in x_sample]

    # Filter out problematic values
    valid_indices = [
        i
        for i, y in enumerate(y_sample)
        if isinstance(y, (int, float)) and not math.isnan(y) and not math.isinf(y)
    ]

    if valid_indices:
        x_valid = [x_sample[i] for i in valid_indices]
        y_valid = [y_sample[i] for i in valid_indices]

        # Calculate initial range
        y_min = min(y_valid)
        y_max = max(y_valid)
        x_min = min(x_valid)
        x_max = max(x_valid)

        print(
            f"Initial data range: x=[{x_min:.3f}, {x_max:.3f}], y=[{y_min:.3f}, {y_max:.3f}]"
        )

        # Calculate range with some default extension
        x_span = x_max - x_min
        x_min_initial = x_min - x_span * 0.1
        x_max_initial = x_max + x_span * 0.1

        print(f"Extended initial range: [{x_min_initial:.3f}, {x_max_initial:.3f}]")

        # Check if we're in the special case (bounds close to integers)
        min_near_int = abs(x_min_initial - round(x_min_initial)) < 0.2
        max_near_int = abs(x_max_initial - round(x_max_initial)) < 0.2
        print(
            f"Min near integer: {min_near_int} (diff: {abs(x_min_initial - round(x_min_initial)):.3f})"
        )
        print(
            f"Max near integer: {max_near_int} (diff: {abs(x_max_initial - round(x_max_initial)):.3f})"
        )

        if min_near_int and max_near_int:
            print("✓ Using special case logic with integer bounds")
            # Simulate the special case logic

            min_rounded = round(x_min_initial)
            max_rounded = round(x_max_initial)
            span = max_rounded - min_rounded

            print(f"Rounded bounds: [{min_rounded}, {max_rounded}], span: {span}")

            # This should trigger the important points buffering
            rand_puffer = 1.0
            new_min = min_rounded
            new_max = max_rounded

            print(f"Before buffering: [{new_min}, {new_max}]")

            # Apply buffering logic
            for punkt_x in wichtige_punkte["x_werte"]:
                print(f"Checking point x={punkt_x}")
                if punkt_x is not None:
                    # Left edge
                    dist_left = abs(punkt_x - new_min)
                    print(f"  Distance to left edge: {dist_left:.3f}")
                    if dist_left <= rand_puffer:
                        old_min = new_min
                        new_min = math.floor(punkt_x - rand_puffer)
                        print(f"  Expanding left: {old_min} -> {new_min}")

                    # Right edge
                    dist_right = abs(punkt_x - new_max)
                    print(f"  Distance to right edge: {dist_right:.3f}")
                    if dist_right <= rand_puffer:
                        old_max = new_max
                        new_max = math.ceil(punkt_x + rand_puffer)
                        print(f"  Expanding right: {old_max} -> {new_max}")

            print(f"After buffering: [{new_min}, {new_max}]")
        else:
            print("✗ Using normal logic (not the special case)")

    print("\n=== Comparison ===")
    print("Expected range with proper buffering: [-4.0, 11.0]")
    print(f"Actual range from Graph: {x_range}")

    # Check each nullstelle distance
    for ns in f.nullstellen:
        left_dist = ns - x_range[0]
        right_dist = x_range[1] - ns
        print(
            f"Nullstelle x={ns}: left_dist={left_dist:.3f}, right_dist={right_dist:.3f}"
        )
        if min(left_dist, right_dist) < 1.0:
            print("  ❌ TOO CLOSE!")
        else:
            print("  ✅ OK")


if __name__ == "__main__":
    debug_optimierung()
