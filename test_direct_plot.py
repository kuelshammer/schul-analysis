#!/usr/bin/env python3
"""
Create a direct visualization test to see the actual plot
"""

from src.schul_analysis.ganzrationale import GanzrationaleFunktion
from src.schul_analysis.visualisierung import Graph


def test_direct_plot():
    """Create and inspect the actual plot"""
    print("=== Direct Plot Test ===")

    # Create the function
    f = GanzrationaleFunktion("(x+3)(x+1)(x-10)")
    print(f"Function: {f.term()}")
    print(f"Nullstellen: {f.nullstellen}")

    # Create the graph
    fig = Graph(f)

    # Check the layout
    print(f"X-axis range: {fig.layout.xaxis.range}")
    print(f"Y-axis range: {fig.layout.yaxis.range}")

    # Check if this is a plotly figure and try to show it
    try:
        # Try to save as HTML to inspect
        fig.write_html("test_plot.html")
        print("Plot saved as test_plot.html")

        # Also try to show the figure structure
        print(f"Figure type: {type(fig)}")
        print(f"Layout keys: {list(fig.layout.keys())}")

        # Check the actual data points
        if hasattr(fig, "data") and fig.data:
            for i, trace in enumerate(fig.data):
                print(f"Trace {i}: {trace.type}")
                if hasattr(trace, "x") and hasattr(trace, "y"):
                    x_data = trace.x
                    y_data = trace.y
                    if x_data and len(x_data) > 0:
                        print(f"  X range: [{min(x_data):.3f}, {max(x_data):.3f}]")
                        print(f"  Y range: [{min(y_data):.3f}, {max(y_data):.3f}]")

                        # Check if any point is near x=-3
                        for j, (x, y) in enumerate(zip(x_data, y_data, strict=False)):
                            if abs(x - (-3)) < 0.1:
                                print(f"  Point near x=-3: ({x:.3f}, {y:.3f})")

    except Exception as e:
        print(f"Error inspecting plot: {e}")

    # Try a more direct approach - check what the actual visual boundaries are
    print("\n=== Boundary Analysis ===")
    x_range = fig.layout.xaxis.range
    x_min, x_max = x_range

    print(f"Theoretical boundaries: [{x_min}, {x_max}]")
    print(f"Width: {x_max - x_min}")

    # Check if -3 is too close to the edge visually
    distance_to_left = abs(-3 - x_min)
    distance_to_right = abs(x_max - (-3))

    print(f"Distance from x=-3 to left edge: {distance_to_left}")
    print(f"Distance from x=-3 to right edge: {distance_to_right}")

    # Maybe the issue is that 1.0 unit is not enough visually
    percentage_of_range = distance_to_left / (x_max - x_min) * 100
    print(f"Left distance as % of total range: {percentage_of_range:.1f}%")

    if percentage_of_range < 5:  # Less than 5% of the range
        print("⚠️  The point might appear too close to the edge visually!")

    # Test with increased buffer
    print("\n=== Testing with Increased Buffer ===")
    fig2 = Graph(f, x_min=-5, x_max=12)  # Manual specification
    print(f"Manual range: [{fig2.layout.xaxis.range}]")
    fig2.write_html("test_plot_manual.html")
    print("Manual plot saved as test_plot_manual.html")


if __name__ == "__main__":
    test_direct_plot()
