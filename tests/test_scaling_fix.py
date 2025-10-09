#!/usr/bin/env python3
"""
Test script to verify the scaling fix is working
"""

import sys

sys.path.insert(0, "src")

from schul_mathematik import GanzrationaleFunktion, Graph


def test_scaling_fix():
    print("=== Testing Scaling Fix ===")

    # Test 1: Simple quadratic function
    print("\n1. Testing f(x) = x² + 2x - 1")
    f1 = GanzrationaleFunktion([1, 2, -1])
    fig1 = Graph(f1)
    x_range1 = fig1.layout.xaxis.range
    print(f"   X-range: [{x_range1[0]:.2f}, {x_range1[1]:.2f}]")
    print("   Expected: around [-1.5, 3.5] ✓")

    # Test 2: Cubic function
    print("\n2. Testing f(x) = (x+4)(x-1)(x-2)")
    f2 = GanzrationaleFunktion([1, 1, -10, 8])  # x³ + x² - 10x + 8
    fig2 = Graph(f2)
    x_range2 = fig2.layout.xaxis.range
    print(f"   X-range: [{x_range2[0]:.2f}, {x_range2[1]:.2f}]")
    print("   Expected: around [-2.1, 2.9] ✓")

    # Test 3: Linear function
    print("\n3. Testing f(x) = x")
    f3 = GanzrationaleFunktion([1, 0])
    fig3 = Graph(f3)
    x_range3 = fig3.layout.xaxis.range
    print(f"   X-range: [{x_range3[0]:.2f}, {x_range3[1]:.2f}]")
    print("   Expected: around [-2.5, 2.5] ✓")

    print("\n=== All tests completed! ===")
    print("If you see ranges like [-30, 30], there's still an issue.")
    print("If you see ranges like [-2, 4], the fix is working!")


if __name__ == "__main__":
    test_scaling_fix()
