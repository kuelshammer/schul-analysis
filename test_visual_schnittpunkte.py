#!/usr/bin/env python3
"""
Visual test script to verify that intersection points are correctly displayed in graphs
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import ErstellePolynom, Graph


def test_visual_schnittpunkte():
    print("=== Visual Test: Schnittpunkte in Graphen ===")

    # Test 1: Lineare und quadratische Funktion
    print("\n1. Test: Lineare und quadratische Funktion")
    print("   f(x) = 2x + 6")
    print("   g(x) = (x - 10)²")
    print("   Erwartete Schnittpunkte: ca. x=5.8 und x=16.2")

    f = ErstellePolynom([6, 2])  # 6 + 2x = 2x + 6
    g = ErstellePolynom([100, -20, 1])  # 100 - 20x + x² = (x-10)² = x²-20x+100

    # Graph mit Schnittpunkten
    fig = Graph(f, g)
    fig.show()

    print("\n2. Test: Zwei Parabeln")
    print("   f(x) = x²")
    print("   g(x) = (x - 2)² + 1")
    print("   Erwarteter Schnittpunkt: ca. x=1.25")

    f = ErstellePolynom([0, 0, 1])  # 0 + 0x + 1x² = x²
    g = ErstellePolynom([5, -4, 1])  # 5 - 4x + x² = (x-2)²+1 = x²-4x+5

    fig = Graph(f, g)
    fig.show()

    print("\n3. Test: Drei Funktionen")
    print("   f(x) = x²")
    print("   g(x) = 2x")
    print("   h(x) = 4")
    print("   Erwartete Schnittpunkte: x=-2, x=0, x=2")

    f = ErstellePolynom([0, 0, 1])  # 0 + 0x + 1x² = x²
    g = ErstellePolynom([0, 2])  # 0 + 2x = 2x
    h = ErstellePolynom([4])  # 4

    fig = Graph(f, g, h)
    fig.show()


if __name__ == "__main__":
    test_visual_schnittpunkte()
