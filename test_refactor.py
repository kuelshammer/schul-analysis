#!/usr/bin/env python3
"""Test script to verify the refactored Funktion.__init__ works correctly"""

from src.schul_analysis.funktion import Funktion, erstelle_funktion_automatisch
import sympy as sp


def test_wrapper_functionality():
    """Test that wrapper functionality is preserved"""

    print("=== Testing Wrapper Functionality ===")

    # Test 1: Basic string input (should work as before)
    print("\n1. Basic string input:")
    try:
        f = Funktion("x^2 + 1")
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Test 2: Tuple input (should work as before)
    print("\n2. Tuple input:")
    try:
        f = Funktion(("x^2 + 1", "x - 1"))
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Test 3: Separate nenner parameter (new functionality)
    print("\n3. Separate nenner parameter:")
    try:
        f = Funktion("x^2 + 1", nenner="x - 1")
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Test 4: Function copy (should work as before)
    print("\n4. Function copy:")
    try:
        f1 = Funktion("x^2 + 1")
        f2 = Funktion(f1)
        print(f"✓ Success: {f2.term()} (Type: {type(f2).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Test 5: Exponential function delegation (wrapper functionality)
    print("\n5. Exponential function delegation:")
    try:
        f = Funktion("exp(x) + 1")
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
        print(
            f"  Should be ExponentialRationaleFunktion: {'ExponentialRationaleFunktion' in str(type(f))}"
        )
    except Exception as e:
        print(f"✗ Failed: {e}")


def test_input_validation():
    """Test that input validation still works"""

    print("\n=== Testing Input Validation ===")

    # Test 1: Invalid mathematical expression
    print("\n1. Invalid mathematical expression:")
    try:
        f = Funktion("x^2 + + 1")
        print(f"✗ Should have failed but got: {f.term()}")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Test 2: Empty string
    print("\n2. Empty string:")
    try:
        f = Funktion("")
        print(f"✗ Should have failed but got: {f.term()}")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

    # Test 3: Invalid nenner parameter type
    print("\n3. Invalid nenner parameter type:")
    try:
        f = Funktion("x^2 + 1", nenner=123)
        print(f"✗ Should have failed but got: {f.term()}")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def test_erstelle_funktion_automatisch():
    """Test that erstelle_funktion_automatisch still works"""

    print("\n=== Testing erstelle_funktion_automatisch ===")

    # Test 1: Basic usage
    print("\n1. Basic usage:")
    try:
        f = erstelle_funktion_automatisch("x^2 + 1")
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")

    # Test 2: With nenner parameter (the fix we implemented)
    print("\n2. With nenner parameter:")
    try:
        f = erstelle_funktion_automatisch("x^2 + 1", nenner="x - 1")
        print(f"✓ Success: {f.term()} (Type: {type(f).__name__})")
    except Exception as e:
        print(f"✗ Failed: {e}")


if __name__ == "__main__":
    test_wrapper_functionality()
    test_input_validation()
    test_erstelle_funktion_automatisch()
