#!/usr/bin/env python3
"""
Debug the current sorting issue
"""

import sys

sys.path.insert(0, "src")

from schul_analysis.ganzrationale import GanzrationaleFunktion


def test_current_sorting():
    """Test the current sorting to see the exact problem"""

    print("Debugging Current Sorting Issue")
    print("=" * 35)

    # Create the function
    h = GanzrationaleFunktion("(x-a)^2*(x+b)^2")

    print(f"Current h.term(): {h.term()}")
    print()

    print("Expected: x^4 + x^3*(...) + x^2*(...) + x*(...) + constant")
    print("But we're getting wrong order!")
    print()

    # Let's also test derivatives
    h1 = h.ableitung()
    print(f"Current h'.term(): {h1.term()}")
    print("Expected: 4*x^3 + ... + constant")


if __name__ == "__main__":
    test_current_sorting()
