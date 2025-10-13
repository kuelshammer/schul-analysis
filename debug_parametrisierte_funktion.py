#!/usr/bin/env python3
"""Debug script to understand parametrisierte function parameter extraction"""

from src.schul_mathematik.analysis.funktion import Funktion

# Test the parameter extraction
f = Funktion("a*x^2 + b*x + c")
print(f"Term: {f.term()}")
print(f"Parameter: {[str(p) for p in f.parameter]}")
print(f"Parameter length: {len(f.parameter)}")
print(f"Free symbols: {f.term_sympy.free_symbols}")
print(f"Term sympy: {f.term_sympy}")

# Check if a, b, c are in free symbols
for symbol in f.term_sympy.free_symbols:
    print(f"Symbol: {symbol}, Name: {str(symbol)}")
