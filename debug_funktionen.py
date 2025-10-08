#!/usr/bin/env python3
"""
Debug script to understand how functions are being created and their intersection points
"""

import sys

sys.path.insert(0, "src")

from schul_analysis import ErstellePolynom, Graph


def debug_funktionen():
    print("=== Debug: Funktions-Erstellung und Schnittpunkte ===")

    # Test 1: Lineare und quadratische Funktion
    print("\n1. Test: Lineare und quadratische Funktion")
    f = ErstellePolynom([6, 2])  # 6 + 2x = 2x + 6
    g = ErstellePolynom([100, -20, 1])  # 100 - 20x + x² = (x-10)² = x²-20x+100

    print(f"f(x) = {f.term()}")
    print(f"g(x) = {g.term()}")

    # Manuelles Testen der erwarteten Schnittpunkte
    x_werte = [5.8, 16.2]
    for x in x_werte:
        f_y = f.wert(x)
        g_y = g.wert(x)
        print(
            f"Bei x={x}: f(x)={f_y:.3f}, g(x)={g_y:.3f}, Differenz={abs(f_y - g_y):.3f}"
        )

    # Test 2: Zwei Parabeln
    print("\n2. Test: Zwei Parabeln")
    f = ErstellePolynom([0, 0, 1])  # 0 + 0x + 1x² = x²
    g = ErstellePolynom([5, -4, 1])  # 5 - 4x + x² = (x-2)²+1 = x²-4x+5

    print(f"f(x) = {f.term()}")
    print(f"g(x) = {g.term()}")

    # Manuelles Testen des erwarteten Schnittpunkts
    x_werte = [1.25]
    for x in x_werte:
        f_y = f.wert(x)
        g_y = g.wert(x)
        print(
            f"Bei x={x}: f(x)={f_y:.3f}, g(x)={g_y:.3f}, Differenz={abs(f_y - g_y):.3f}"
        )

    # Test 3: Drei Funktionen
    print("\n3. Test: Drei Funktionen")
    f = ErstellePolynom([0, 0, 1])  # 0 + 0x + 1x² = x²
    g = ErstellePolynom([0, 2])  # 0 + 2x = 2x
    h = ErstellePolynom([4])  # 4

    print(f"f(x) = {f.term()}")
    print(f"g(x) = {g.term()}")
    print(f"h(x) = {h.term()}")

    # Manuelles Testen der erwarteten Schnittpunkte
    x_werte = [-2, 0, 2]
    for x in x_werte:
        f_y = f.wert(x)
        g_y = g.wert(x)
        h_y = h.wert(x)
        print(f"Bei x={x}: f(x)={f_y:.3f}, g(x)={g_y:.3f}, h(x)={h_y:.3f}")
        print(
            f"  f-g={abs(f_y - g_y):.3f}, f-h={abs(f_y - h_y):.3f}, g-h={abs(g_y - h_y):.3f}"
        )


if __name__ == "__main__":
    debug_funktionen()
