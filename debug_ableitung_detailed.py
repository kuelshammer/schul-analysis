#!/usr/bin/env python3
"""Debug script to understand Ableitungsstrategie behavior"""

from src.schul_mathematik.analysis.debugger import FunktionsDebugger
import sympy as sp
import traceback

# Test the berechne_ableitung method with debugging
debugger = FunktionsDebugger()

print("=== Debugging Ableitungsstrategie ===")
try:
    session = debugger.berechne_ableitung("x**3 + 2*x**2 + x + 1", ordnung=2)

    print(f"Session titel: {session.titel}")
    print(f"Anzahl schritte: {len(session.schritte)}")
    print(f"Schritte:")
    for i, schritt in enumerate(session.schritte):
        print(f"  {i + 1}. {schritt.typ}: {schritt.beschreibung}")
        if schritt.ergebnis:
            print(f"     Ergebnis: {schritt.ergebnis}")

    print(f"Letztes Ergebnis: {session.get_letzte_ergebnis()}")

except Exception as e:
    print(f"Exception occurred: {e}")
    traceback.print_exc()

# Test strategy detection manually
print("\n=== Testing strategy detection ===")
x = sp.Symbol("x")
funktion = sp.sympify("x**3 + 2*x**2 + x + 1")
kontext = {"operation": "ableitung", "ordnung": 2, "variable": x}

print(f"Function: {funktion}")
print(f"Context: {kontext}")

for i, strategie in enumerate(debugger.strategien):
    print(f"Strategy {i}: {type(strategie).__name__}")
    try:
        kann_anwenden = strategie.kann_anwenden(funktion, kontext)
        print(f"  kann_anwenden: {kann_anwenden}")
        if kann_anwenden:
            print("  Trying to apply...")
            session = debugger.start_session("Test", funktion)
            result = strategie.wende_an(funktion, session, kontext)
            print(f"  Result: {result}")
            print(f"  Session steps: {len(session.schritte)}")
    except Exception as e:
        print(f"  Exception: {e}")
        traceback.print_exc()
