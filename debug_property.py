#!/usr/bin/env python3

import sys

sys.path.insert(0, "src")

# Test 1: Check if the property is in the file
with open("src/schul_analysis/funktion.py", "r") as f:
    content = f.read()
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if "def hat_polstellen" in line:
            print(f"Found hat_polstellen at line {i}: {line}")
            print(f"Context: {lines[i - 2 : i + 3]}")

# Test 2: Try to import and check the class
from schul_analysis.funktion import Funktion

print(f"Funktion class found: {Funktion}")

# Test 3: Check class attributes
print(
    f"Class attributes: {[attr for attr in dir(Funktion) if not attr.startswith('_') and 'pol' in attr.lower()]}"
)

# Test 4: Try to access the specific property
try:
    prop = getattr(Funktion, "hat_polstellen", None)
    print(f"Property object: {prop}")
    print(f"Property type: {type(prop)}")
except Exception as e:
    print(f"Error accessing property: {e}")
