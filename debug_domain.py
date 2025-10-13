#!/usr/bin/env python3
"""Debug script to understand definitionsbereich behavior"""

from src.schul_mathematik.analysis.funktion import Funktion

# Test the definitionsbereich
f = Funktion("x^2 + 1")
print(f"Term: {f.term()}")
print(f"Definitionsbereich type: {type(f.definitionsbereich)}")
print(f"Definitionsbereich value: {f.definitionsbereich}")

if callable(f.definitionsbereich):
    print("Definitionsbereich is callable")
    print(f"Definitionsbereich() result: {f.definitionsbereich()}")
else:
    print("Definitionsbereich is not callable")
    print(f"Definitionsbereich directly: {f.definitionsbereich}")
