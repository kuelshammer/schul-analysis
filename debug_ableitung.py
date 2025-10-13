#!/usr/bin/env python3
"""Debug script to understand Ableitungsstrategie behavior"""

from src.schul_mathematik.analysis.debugger import FunktionsDebugger
import sympy as sp

# Test the berechne_ableitung method
debugger = FunktionsDebugger()
session = debugger.berechne_ableitung("x**3 + 2*x**2 + x + 1", ordnung=2)

print(f"Session titel: {session.titel}")
print(f"Anzahl schritte: {len(session.schritte)}")
print(f"Schritte:")
for i, schritt in enumerate(session.schritte):
    print(f"  {i + 1}. {schritt.typ}: {schritt.beschreibung}")
    if schritt.ergebnis:
        print(f"     Ergebnis: {schritt.ergebnis}")

print(f"Letztes Ergebnis: {session.get_letzte_ergebnis()}")
