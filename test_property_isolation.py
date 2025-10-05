#!/usr/bin/env python3

# Test to isolate the property definition issue

# Test 1: Extract just the relevant part of the class
test_code = """
class TestFunktion:
    def __init__(self):
        self.nenner = None
        self.zaehler = None

    @property
    def ist_ganzrational(self):
        return hasattr(self, 'nenner') and self.nenner == 1

    @property
    def hat_polstellen(self):
        return not self.ist_ganzrational
"""

# Execute the test code
exec(test_code)

# Test the class
f = TestFunktion()
print(f"Test class has hat_polstellen: {hasattr(f, 'hat_polstellen')}")
print(f"hat_polstellen value: {f.hat_polstellen}")

# Now test the actual class
import sys

sys.path.insert(0, "src")
from schul_analysis.funktion import Funktion

f2 = Funktion("(x+1)/(x-1)")
print(f"Actual class has hat_polstellen: {hasattr(f2, 'hat_polstellen')}")
